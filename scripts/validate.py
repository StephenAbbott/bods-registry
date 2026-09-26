#!/usr/bin/env python3
"""Validate the contents of bods-registry.

Checks:
  * extensions/registry.json validates against extensions/registry.schema.json
  * every extensions/<slug>/extension.json validates against extensions/extension.schema.json,
    its slug matches its directory, it is listed in registry.json (TEMPLATE excepted), and the
    fields shared with the registry entry agree
  * every extension directory has README.md with the required headings and a schema/ dir whose
    files are named after BODS schema files and parse as JSON
  * every implementations/<slug>.md has complete YAML front matter with valid closed-list values,
    a slug equal to its filename, and the six required sections in order
  * every learnings/YYYY-MM-DD-<slug>.md has complete front matter, a date matching its filename,
    valid closed-list values, and the four required sections
  * cross-references resolve: profile `extensions` -> registry slugs, profile `learnings` ->
    learning files, learning `source` -> profile slugs, registry `used_by` -> profile slugs
  * slugs are unique
  * optionally, with --bods-schema <dir> pointing at a checkout of the BODS schema/ directory
    (for example the 0.4.0 branch of openownership/data-standard), each extension's JSON Merge
    Patches are applied to the core schema and every file in its examples/ is validated against
    the patched statement schema

Exit status is non-zero if any check fails. Run from the repository root:

    python scripts/validate.py
    python scripts/validate.py --bods-schema ../data-standard/schema
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
EXT_DIR = ROOT / "extensions"
IMPL_DIR = ROOT / "implementations"
LEARN_DIR = ROOT / "learnings"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LEARNING_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(-[a-z0-9]+)*)\.md$")

BODS_SCHEMA_FILES = {
    "statement.json",
    "components.json",
    "entity-record.json",
    "person-record.json",
    "relationship-record.json",
}

PROFILE_REQUIRED = [
    "name", "slug", "type", "organisation", "bods_versions", "roles", "status",
    "author_relationship", "last_reviewed",
]
PROFILE_TYPES = {
    "national-register", "register-software", "data-publisher", "data-republisher",
    "data-user", "standard-or-spec", "tool",
}
PROFILE_ROLES = {"collect", "store", "publish", "republish", "consume", "reference"}
PROFILE_STATUS = {"live", "pilot", "paused", "planned", "historic"}
PROFILE_RELATIONSHIP = {"implementer", "third-party"}
PROFILE_SECTIONS = [
    "Summary",
    "How BODS is used",
    "What was extended or adapted",
    "What could not be modelled",
    "Learnings for the standard",
    "Sources",
]

LEARNING_REQUIRED = ["title", "date", "area", "status", "summary"]
LEARNING_AREAS = {
    "schema", "codelist", "guidance", "documentation", "tooling", "governance", "serialisation",
}
LEARNING_STATUS = {"observed", "needs-issue", "raised", "resolved", "declined"}
LEARNING_SECTIONS = [
    "What was observed",
    "Why it matters for the standard",
    "Suggested change",
    "Evidence",
]

EXTENSION_README_SECTIONS = ["Purpose", "Fields", "Codelists", "Example"]

# Keys that must agree between extension.json and the registry entry.
SHARED_EXTENSION_KEYS = ["name", "description", "bods_versions", "category", "status"]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checked = 0

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path, report: Report) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.error(rel(path), f"cannot parse JSON: {exc}")
        return None


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def split_front_matter(path: Path, report: Report) -> tuple[dict | None, str]:
    """Return (front_matter, body). Front matter must be the first thing in the file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        report.error(rel(path), "missing YAML front matter (file must start with ---)")
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        report.error(rel(path), "front matter not terminated by --- on its own line")
        return None, text
    raw = text[4:end]
    body = text[end + 5:]
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        report.error(rel(path), f"front matter is not valid YAML: {exc}")
        return None, body
    if not isinstance(data, dict):
        report.error(rel(path), "front matter must be a mapping")
        return None, body
    return data, body


def headings(body: str, level: int = 2) -> list[str]:
    prefix = "#" * level + " "
    return [line[len(prefix):].strip() for line in body.splitlines() if line.startswith(prefix)]


def check_sections(path: Path, body: str, required: list[str], report: Report) -> None:
    found = headings(body)
    missing = [h for h in required if h not in found]
    for h in missing:
        report.error(rel(path), f"missing section '## {h}'")
    if not missing:
        order = [h for h in found if h in required]
        if order != required:
            report.error(rel(path), f"sections out of order; expected {required}, found {order}")


def check_closed(path: Path, data: dict, key: str, allowed: set[str], report: Report, many: bool = False) -> None:
    value = data.get(key)
    if value in (None, "", []):
        return
    values = value if many else [value]
    if not isinstance(values, list):
        report.error(rel(path), f"'{key}' must be a list")
        return
    for v in values:
        if v not in allowed:
            report.error(rel(path), f"'{key}' value {v!r} not in {sorted(allowed)}")


def require_keys(path: Path, data: dict, keys: list[str], report: Report) -> None:
    for k in keys:
        if data.get(k) in (None, "", []):
            report.error(rel(path), f"required front-matter key '{k}' is missing or empty")


def schema_validator(schema_path: Path, report: Report) -> Draft202012Validator | None:
    schema = load_json(schema_path, report)
    if schema is None:
        return None
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001
        report.error(rel(schema_path), f"schema is itself invalid: {exc}")
        return None
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_against(validator: Draft202012Validator, instance: dict, where: str, report: Report) -> None:
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in err.path) or "(root)"
        report.error(where, f"{location}: {err.message}")


# ---------------------------------------------------------------------------
# Applying extensions to the BODS schema (optional deep check)
# ---------------------------------------------------------------------------

def merge_patch(target, patch):
    """RFC 7386 JSON Merge Patch."""
    if not isinstance(patch, dict):
        return patch
    if not isinstance(target, dict):
        target = {}
    for key, value in patch.items():
        if value is None:
            target.pop(key, None)
        else:
            target[key] = merge_patch(target.get(key), value)
    return target


def check_patch_rules(core: dict, patch: dict, where: str, report: Report, path: str = "") -> None:
    """Mechanical checks for the normative rules in extensions/README.md.

    Rule 1: a null in a merge patch deletes the key -> not allowed where the key exists in core.
    Rule 2: changing 'type' or 'required' of a core node is not allowed.
    Rule 4: setting 'enum', 'codelist' or 'openCodelist' where the core node already has an enum
            (i.e. a closed codelist) is not allowed; arrays are replaced wholesale by a merge patch,
            so this is how an extension would smuggle a code into a closed list.
    """
    if not isinstance(patch, dict) or not isinstance(core, dict):
        return
    for key, value in patch.items():
        here = f"{path}/{key}"
        in_core = key in core
        if value is None and in_core:
            report.error(where, f"rule 1: patch deletes core key {here}")
            continue
        if in_core and key in ("type", "required") and value != core[key]:
            report.error(where, f"rule 2: patch changes core '{key}' at {path or '/'}")
            continue
        if key in ("enum", "codelist", "openCodelist") and "enum" in core:
            report.error(where, f"rule 4: patch touches '{key}' of a closed codelist at {path or '/'}")
            continue
        if in_core:
            check_patch_rules(core[key], value, where, report, here)


def load_bods_schema(schema_dir: Path, report: Report) -> dict[str, dict] | None:
    schemas: dict[str, dict] = {}
    for name in BODS_SCHEMA_FILES:
        path = schema_dir / name
        if not path.exists():
            report.error(str(path), "BODS schema file not found in --bods-schema directory")
            return None
        data = load_json(path, report)
        if data is None:
            return None
        schemas[name] = data
    return schemas


def validate_examples_against_bods(ext_path: Path, meta: dict, core: dict[str, dict], report: Report) -> None:
    """Apply the extension's patches to a copy of the core schema and validate its examples."""
    patched = copy.deepcopy(core)
    schema_dir = ext_path / "schema"
    if schema_dir.is_dir():
        for patch_path in sorted(schema_dir.glob("*.json")):
            if patch_path.name not in patched:
                continue
            patch = load_json(patch_path, report)
            if isinstance(patch, dict):
                check_patch_rules(core[patch_path.name], patch, rel(patch_path), report)
                patched[patch_path.name] = merge_patch(patched[patch_path.name], patch)
    resources = [
        (schema["$id"], Resource(contents=schema, specification=DRAFT202012))
        for schema in patched.values()
        if "$id" in schema
    ]
    registry = Registry().with_resources(resources)
    try:
        validator = Draft202012Validator(patched["statement.json"], registry=registry, format_checker=FormatChecker())
    except Exception as exc:  # noqa: BLE001
        report.error(rel(ext_path), f"patched BODS schema is not a valid JSON Schema: {exc}")
        return
    for example_path in sorted((ext_path / "examples").glob("*.json")):
        example = load_json(example_path, report)
        if example is None:
            continue
        report.checked += 1
        for err in sorted(validator.iter_errors(example), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(root)"
            report.error(rel(example_path), f"does not validate against patched BODS schema at {location}: {err.message[:200]}")


# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------

def check_extensions(report: Report, core: dict[str, dict] | None = None) -> tuple[set[str], dict[str, dict]]:
    registry_validator = schema_validator(EXT_DIR / "registry.schema.json", report)
    ext_validator = schema_validator(EXT_DIR / "extension.schema.json", report)

    registry_path = EXT_DIR / "registry.json"
    registry = load_json(registry_path, report)
    entries: dict[str, dict] = {}
    if registry is not None and registry_validator is not None:
        validate_against(registry_validator, registry, rel(registry_path), report)
        report.checked += 1
        for entry in registry.get("extensions", []):
            slug = entry.get("slug")
            if slug in entries:
                report.error(rel(registry_path), f"duplicate slug {slug!r}")
            entries[slug] = entry

    held_here: set[str] = set()
    for ext_path in sorted(EXT_DIR.iterdir()):
        if not ext_path.is_dir():
            continue
        meta_path = ext_path / "extension.json"
        if not meta_path.exists():
            report.error(rel(ext_path), "extension directory has no extension.json")
            continue
        meta = load_json(meta_path, report)
        if meta is None:
            continue
        report.checked += 1
        if ext_validator is not None:
            validate_against(ext_validator, meta, rel(meta_path), report)

        is_template = ext_path.name == "TEMPLATE"
        slug = meta.get("slug")
        if not is_template and slug != ext_path.name:
            report.error(rel(meta_path), f"slug {slug!r} does not match directory name {ext_path.name!r}")
        if not is_template:
            held_here.add(slug)
            entry = entries.get(slug)
            if entry is None:
                report.error(rel(meta_path), f"extension {slug!r} is not listed in extensions/registry.json")
            else:
                for key in SHARED_EXTENSION_KEYS:
                    if entry.get(key) != meta.get(key):
                        report.error(rel(meta_path), f"'{key}' differs from the registry entry")
                if not entry.get("copy_held_here"):
                    report.error(rel(registry_path), f"{slug!r}: copy_held_here should be true (a copy exists under extensions/{slug}/)")

        readme = ext_path / "README.md"
        if not readme.exists():
            report.error(rel(ext_path), "missing README.md")
        else:
            check_sections(readme, readme.read_text(encoding="utf-8"), EXTENSION_README_SECTIONS, report)

        schema_dir = ext_path / "schema"
        declared = set(meta.get("schemas", []))
        if schema_dir.is_dir():
            present = {p.name for p in schema_dir.iterdir() if p.is_file()}
            for name in present:
                if name not in BODS_SCHEMA_FILES:
                    report.error(rel(schema_dir / name), f"not a BODS schema file name; expected one of {sorted(BODS_SCHEMA_FILES)}")
                else:
                    patch = load_json(schema_dir / name, report)
                    if patch is not None and not isinstance(patch, dict):
                        report.error(rel(schema_dir / name), "a JSON Merge Patch must be a JSON object")
            if declared and declared != present:
                report.error(rel(meta_path), f"'schemas' {sorted(declared)} does not match files in schema/ {sorted(present)}")
        elif declared:
            report.error(rel(meta_path), "'schemas' declared but schema/ directory is missing")

        codelist_dir = ext_path / "codelists"
        declared_cl = set(meta.get("codelists", []))
        if codelist_dir.is_dir():
            present_cl = {p.name for p in codelist_dir.iterdir() if p.suffix == ".csv"}
            if declared_cl and declared_cl != present_cl:
                report.error(rel(meta_path), f"'codelists' {sorted(declared_cl)} does not match files in codelists/ {sorted(present_cl)}")
            for csv_path in codelist_dir.glob("*.csv"):
                header = csv_path.read_text(encoding="utf-8").splitlines()[0].strip() if csv_path.stat().st_size else ""
                if not header.startswith("code,title,description"):
                    report.error(rel(csv_path), "codelist header must start with 'code,title,description'")
        elif declared_cl:
            report.error(rel(meta_path), "'codelists' declared but codelists/ directory is missing")

        examples = ext_path / "examples"
        if not examples.is_dir() or not any(examples.glob("*.json")):
            report.error(rel(ext_path), "missing examples/ directory with at least one .json example")
        else:
            for ex in examples.glob("*.json"):
                data = load_json(ex, report)
                if data is not None and not isinstance(data, list):
                    report.error(rel(ex), "a BODS example must be a JSON array of statements")
            if core is not None:
                validate_examples_against_bods(ext_path, meta, core, report)

    for slug, entry in entries.items():
        if entry.get("copy_held_here") and slug not in held_here:
            report.error(rel(registry_path), f"{slug!r}: copy_held_here is true but extensions/{slug}/ does not exist")

    return set(entries), entries


# ---------------------------------------------------------------------------
# Implementation profiles
# ---------------------------------------------------------------------------

def check_profiles(report: Report) -> dict[str, dict]:
    profiles: dict[str, dict] = {}
    for path in sorted(IMPL_DIR.glob("*.md")):
        if path.name in {"README.md", "TEMPLATE.md"}:
            continue
        data, body = split_front_matter(path, report)
        if data is None:
            continue
        report.checked += 1
        require_keys(path, data, PROFILE_REQUIRED, report)
        slug = data.get("slug")
        if slug != path.stem:
            report.error(rel(path), f"slug {slug!r} must equal filename {path.stem!r}")
        if slug and not SLUG_RE.match(str(slug)):
            report.error(rel(path), f"slug {slug!r} is not lower-case-hyphenated")
        check_closed(path, data, "type", PROFILE_TYPES, report)
        check_closed(path, data, "roles", PROFILE_ROLES, report, many=True)
        check_closed(path, data, "status", PROFILE_STATUS, report)
        check_closed(path, data, "author_relationship", PROFILE_RELATIONSHIP, report)
        lr = data.get("last_reviewed")
        if lr and not DATE_RE.match(str(lr)):
            report.error(rel(path), f"last_reviewed {lr!r} must be YYYY-MM-DD")
        for key in ("bods_versions", "extensions", "upstream_issues", "learnings", "jurisdictions"):
            if key in data and data[key] is not None and not isinstance(data[key], list):
                report.error(rel(path), f"'{key}' must be a list")
        check_sections(path, body, PROFILE_SECTIONS, report)
        if slug in profiles:
            report.error(rel(path), f"duplicate profile slug {slug!r}")
        profiles[str(slug)] = data
    return profiles


# ---------------------------------------------------------------------------
# Learnings
# ---------------------------------------------------------------------------

def check_learnings(report: Report) -> dict[str, dict]:
    learnings: dict[str, dict] = {}
    for path in sorted(LEARN_DIR.glob("*.md")):
        if path.name in {"README.md", "TEMPLATE.md"}:
            continue
        m = LEARNING_FILE_RE.match(path.name)
        if not m:
            report.error(rel(path), "filename must be YYYY-MM-DD-<slug>.md")
        data, body = split_front_matter(path, report)
        if data is None:
            continue
        report.checked += 1
        require_keys(path, data, LEARNING_REQUIRED, report)
        date = str(data.get("date", ""))
        if m and date != m.group(1):
            report.error(rel(path), f"front-matter date {date!r} does not match filename date {m.group(1)!r}")
        check_closed(path, data, "area", LEARNING_AREAS, report)
        check_closed(path, data, "status", LEARNING_STATUS, report)
        if data.get("status") == "raised" and not data.get("upstream_issues"):
            report.error(rel(path), "status 'raised' requires at least one upstream_issues link")
        for key in ("source", "bods_versions", "upstream_issues"):
            if key in data and data[key] is not None and not isinstance(data[key], list):
                report.error(rel(path), f"'{key}' must be a list")
        check_sections(path, body, LEARNING_SECTIONS, report)
        learnings[path.name] = data
    return learnings


# ---------------------------------------------------------------------------
# Cross-references
# ---------------------------------------------------------------------------

def check_cross_references(report: Report, ext_slugs: set[str], entries: dict[str, dict],
                           profiles: dict[str, dict], learnings: dict[str, dict]) -> None:
    for slug, data in profiles.items():
        where = rel(IMPL_DIR / f"{slug}.md")
        for ext in data.get("extensions") or []:
            if ext not in ext_slugs:
                report.error(where, f"extension {ext!r} is not in extensions/registry.json")
        for fname in data.get("learnings") or []:
            if fname not in learnings:
                report.error(where, f"learning {fname!r} not found in learnings/")
    for fname, data in learnings.items():
        for src in data.get("source") or []:
            if src not in profiles:
                report.error(rel(LEARN_DIR / fname), f"source {src!r} is not an implementation profile slug")
    for slug, entry in entries.items():
        for used in entry.get("used_by") or []:
            if used not in profiles:
                report.error(rel(EXT_DIR / "registry.json"), f"{slug!r}: used_by {used!r} is not an implementation profile slug")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bods-schema", type=Path, metavar="DIR",
                        help="path to a BODS schema/ directory; enables validation of extension examples "
                             "against the patched core schema")
    args = parser.parse_args()

    report = Report()
    core = None
    if args.bods_schema is not None:
        core = load_bods_schema(args.bods_schema, report)
    ext_slugs, entries = check_extensions(report, core)
    profiles = check_profiles(report)
    learnings = check_learnings(report)
    check_cross_references(report, ext_slugs, entries, profiles, learnings)

    if report.ok():
        deep = " (extension examples validated against the BODS schema)" if core else ""
        print(f"OK{deep}: {report.checked} files checked, "
              f"{len(entries)} extension(s) registered, {len(profiles)} profile(s), {len(learnings)} learning(s).")
        return 0
    print(f"FAILED: {len(report.errors)} problem(s)", file=sys.stderr)
    for e in report.errors:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
