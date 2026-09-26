---
# Copy this file to implementations/<slug>.md and fill it in.
# Keys marked (required) are checked by scripts/validate.py.
name: ""                        # (required) Display name, e.g. "Foster Moore Verne Beneficial Ownership"
slug: ""                        # (required) Must equal the filename without .md; lower-case, hyphens only
type: ""                        # (required) One of: national-register | register-software | data-publisher | data-republisher | data-user | standard-or-spec | tool
organisation: ""                # (required) Who runs it
organisation_url: ""            # Homepage
jurisdictions: []               # ISO 3166-1 alpha-2 codes, or ["global"]
bods_versions: []               # (required) e.g. ["0.2", "0.4"]; use "aligned" for BODS-shaped data that is not published as BODS
roles: []                       # (required) Any of: collect | store | publish | republish | consume | reference
status: ""                      # (required) One of: live | pilot | paused | planned | historic
since: ""                       # Year or YYYY-MM when BODS use began
data_url: ""                    # Where BODS data (or a sample) can be obtained, if anywhere
repository_url: ""              # Source code, if open
extensions: []                  # Slugs from extensions/registry.json used by this implementation
upstream_issues: []             # openownership/data-standard issue URLs this implementation's experience bears on
learnings: []                   # Filenames in learnings/ that came from this implementation
author_relationship: ""         # (required) One of: implementer | third-party
last_reviewed: ""               # (required) YYYY-MM-DD
---

## Summary

Two or three sentences: what the implementation is, what BODS does for it, and how much of the standard it uses.

## How BODS is used

Which statement types are produced or consumed; whether data is collected, stored, published or transformed in BODS; which serialisation (JSON array, JSON Lines, other); how identifiers are handled; how change over time is represented (or not). Link to the mapping, schema or documentation that shows this.

## What was extended or adapted

Additional fields, codes or objects beyond the core schema, with a link to where they are defined. Deviations in structure (flattening, mandatory fields the standard makes optional, renamed codes). If an extension is registered, link its slug.

## What could not be modelled

Concepts in the source data or business process that the implementer could not express in BODS, and what they did instead. Be concrete: the concept, the BODS field(s) considered, the workaround, and a link.

## Learnings for the standard

What this implementation tells the standard's maintainers. Link to entries in `learnings/` and to the upstream issues they feed.

## Sources

Every link used above, one per line, with a date. Public sources only.
