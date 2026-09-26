# Extensions registry

BODS permits extended data: an implementer may add fields the core schema does not describe, and is [asked to document them](https://standard.openownership.org/en/main/standard/system/conformance.html#extending-the-schema). This directory holds the registry of documented extensions (`registry.json`), the rules an extension must follow to be listed, and a template for the extension itself.

The design follows the [Open Contracting Data Standard](https://standard.open-contracting.org/latest/en/guidance/map/extensions/) approach, which the BODS extensions concept note identified as the closest fit: an extension is a JSON Merge Patch applied to the standard's JSON Schema, plus codelist additions, plus documentation, published at a stable URL.

## What an extension is

A collection of **documented additional fields and/or codes**, consisting of:

- `extension.json` — machine-readable metadata (name, description, maintainer, compatible BODS versions, dependencies, category). Schema: [`extension.schema.json`](extension.schema.json).
- `README.md` — human-readable documentation: purpose, the fields and codes added, and at least one worked example.
- `schema/` — one JSON Merge Patch ([RFC 7386](https://datatracker.ietf.org/doc/html/rfc7386)) per BODS schema file the extension changes, named identically to the file it patches: `statement.json`, `components.json`, `entity-record.json`, `person-record.json`, `relationship-record.json`.
- `codelists/` — CSV files for new codelists, or additions to open codelists, using the BODS codelist columns (`code,title,description,technical note`). Additions to an existing codelist are named `+<codelist>.csv`.
- `examples/` — at least one BODS statement array that uses the extension and validates against the patched schema.

The layout is in [`TEMPLATE/`](TEMPLATE/). An extension lives in its own repository or in a directory of the implementer's repository; the registry links to it. Copies may also be held here under `extensions/<slug>/`.

## Normative rules

An extension listed in this registry:

1. **MUST NOT remove** any field, object or codelist from the core schema.
2. **MUST NOT change** the type, required status, or meaning of any core field. Narrowing a core field (for example making an optional field required for a particular publisher) is a publisher's own conformance rule, not an extension, and belongs in the publisher's documentation.
3. **MUST NOT add** a field whose meaning duplicates a core field. If the core schema already has a way to say it, use that.
4. **MUST NOT add** codes to a closed codelist. Closed codelists (for example `interestType`, `entityType.subtype`, `unspecifiedReason`) can only be changed through the standard's own governance. An extension that needs a new code in a closed list should propose it upstream and, meanwhile, use the nearest core code with the local term in `details` or an equivalent free-text field.
5. **MUST name** new fields in lowerCamelCase, consistent with the core schema, and **MUST give** every new field a `title` and `description` in the schema patch.
6. **MUST declare** which BODS versions it is compatible with. A patch written against 0.4 does not automatically apply to a later version.
7. **MUST be** published at a stable URL from which `extension.json`, `README.md` and the `schema/` files can be retrieved by appending their paths.
8. **SHOULD** place new top-level properties under a namespace object named after the extension (for example `recordDetails.assets` or `recordDetails.ebwAttestation`) rather than scattering fields across existing objects, so that two extensions cannot collide.

The validator in this repository checks metadata and structure, and, when given a checkout of the BODS schema (`python scripts/validate.py --bods-schema <dir>`, which CI does against the 0.4.0 branch), applies each extension's patches to the core schema and validates the extension's examples against the result. In that mode it also checks the patches mechanically against rules 1, 2 and 4 (deleting a core key, changing a core `type` or `required`, or touching the `enum` of a closed codelist all fail CI). Rules 3, 5 and 8 are checked by review.

## Registry fields

`registry.json` lists every extension the registry knows about. Fields mirror `extension.json` so that the two can be checked against each other:

| Field | Meaning |
|---|---|
| `slug` | Stable identifier, lower-case with hyphens. Also the directory name if a copy is held here. |
| `name`, `description` | As in `extension.json`. |
| `url` | Base URL of the extension (the directory containing `extension.json`). |
| `documentation_url` | Where a human should start reading. |
| `maintainer` | `{name, url}` of the organisation or person responsible. |
| `bods_versions` | Versions the extension is compatible with, e.g. `["0.4"]`. |
| `category` | One of: `assets`, `documents`, `projects`, `payments`, `sanctions`, `agents`, `political-exposure`, `procurement`, `verification`, `identifiers`, `other`. Drawn from the collaboration areas named in the BODS extensions concept note; `other` is fine. |
| `status` | `draft` (still changing), `community` (stable, maintained by its author), `deprecated` (superseded or abandoned). |
| `dependencies` | Slugs of other extensions this one requires. |
| `used_by` | Implementation profile slugs that use it. |
| `first_registered` | YYYY-MM-DD. |

There is no "core" or "endorsed" status. The registry records what exists; it does not certify it.

## Proposing that an extension becomes part of BODS

An extension that several implementers adopt is the strongest kind of evidence that the standard should absorb it. When that happens, open a feature request on [openownership/data-standard](https://github.com/openownership/data-standard/issues/new/choose) linking the registry entry and the profiles that use it.
