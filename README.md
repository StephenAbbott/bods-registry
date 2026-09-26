# bods-registry

A community record of the [Beneficial Ownership Data Standard (BODS)](https://standard.openownership.org/) in use: who has implemented it, how they extended it, and what those implementations have taught us about the standard itself.

This repository is **not** the standard. BODS is stewarded by [Open Ownership](https://www.openownership.org/) and maintained by [Open Data Services](https://opendataservices.coop/); the schema, codelists and documentation live in [openownership/data-standard](https://github.com/openownership/data-standard). The registry sits alongside it, in the space the standard deliberately leaves open: BODS [permits extended data](https://standard.openownership.org/en/main/standard/system/conformance.html#extending-the-schema) and asks implementers to document their extensions, but provides no registry, template or validator for doing so. This repository provides those three things, and a place to record implementation experience so that it can feed back into the standard's [feature tracker](https://github.com/orgs/openownership/projects/9/views/1).

## What is here

| Folder | What it holds | Add one when… |
|---|---|---|
| [`implementations/`](implementations/) | One profile per implementation of BODS: national registers, register software, data publishers and republishers, analysis tools. Each profile records the BODS version, the role BODS plays, what was extended, what could not be modelled, and links to public evidence. | You know of a live, piloted or historic use of BODS that is documented publicly. |
| [`extensions/`](extensions/) | A registry of documented extensions to the BODS schema and codelists (`registry.json`), the normative rules an extension must follow, and a template repository layout. | An implementer has added fields or codes beyond the core schema and is willing to document them. |
| [`learnings/`](learnings/) | Dated notes recording something an implementation revealed about the standard: an ambiguity, a documentation gap, a modelling pattern worth generalising, a codelist that did not fit. Each entry points at the upstream issue it feeds. | Working with BODS data surfaced something the standard's maintainers should know. |
| [`scripts/`](scripts/) | `validate.py`, which checks every file above against its schema or template. Runs in CI on every push and pull request. | — |

## Ground rules

**Public evidence only.** Every claim in a profile or learning must be supported by a link to something public: a register, a repository, a published mapping, a blog post, a GitHub issue, a conference talk. Private correspondence, internal documents and hearsay do not go in this repository, however informative. If the only evidence is private, ask the implementer to publish something first.

**Describe, do not judge.** A profile records what an implementation does and where it departs from the standard. It is not a compliance score. Departures are often reasonable, and recording them is how the standard learns.

**Feed upstream.** The point of a learning is to reach the standard's maintainers. Each entry names the [openownership/data-standard](https://github.com/openownership/data-standard/issues) issue it relates to, or proposes one. The registry is a staging area, not a destination.

**One implementer, one profile.** A product deployed in several jurisdictions gets one profile for the product and, where a deployment is itself documented, one for each deployment that cross-references it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a profile, register an extension or record a learning, and for the review process. You can also open an issue using one of the [issue forms](https://github.com/StephenAbbott/bods-registry/issues/new/choose) and a maintainer will draft the entry with you.

## Validation

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py
```

The same command runs in [GitHub Actions](.github/workflows/validate.yml). It checks that `extensions/registry.json` matches its schema, that every extension directory carries valid `extension.json` metadata and is listed in the registry, that every implementation profile and learning has complete front matter and the required sections, and that slugs and cross-references resolve. CI additionally checks out the BODS 0.4 schema and runs `validate.py --bods-schema`, which applies each extension's JSON Merge Patches to the core schema and validates the extension's example data against the result.

## Licence

Code in this repository (`scripts/`, workflows, JSON schemas) is released under the [MIT Licence](LICENSE). Content (implementation profiles, learnings, extension documentation and the templates for them) is released under [Creative Commons Attribution 4.0 International](LICENSE-CONTENT) — reuse it freely with attribution to "bods-registry contributors".

The BODS schema and documentation referenced here are © Open Ownership and released under their own licences; nothing in this repository changes that.

## Maintainer

[Stephen Abbott Pugh](https://www.beneficialownership.co.uk/) — former product owner of BODS at Open Ownership. The registry is maintained in a personal capacity as part of an effort to keep BODS maintained while it has no funded team. Issues and pull requests welcome.
