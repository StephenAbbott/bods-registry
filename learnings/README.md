# Learnings

Dated notes recording something an implementation revealed about BODS itself. A learning is smaller than a feature request and more specific than a profile: one observation, its evidence, why it matters for the standard, and the upstream issue it feeds.

File names are `YYYY-MM-DD-<slug>.md`, dated when the learning was first written up. `TEMPLATE.md` is the starting point.

## What makes a good learning

- It is **about the standard**, not about the implementation. "Our mapper had a bug" is not a learning; "three independent mappers made the same mistake, so the documentation is unclear" is.
- It is **evidenced**: a link to the data, code, issue or document where the observation can be checked.
- It is **actionable**: it names a documentation page, schema field, codelist or guidance topic, and says what change (if any) it suggests. "No change, but worth knowing" is a valid conclusion.
- It **points upstream**: to an existing issue on [openownership/data-standard](https://github.com/openownership/data-standard/issues), or is marked `needs-issue`.

## Areas

`area` in the front matter is one of: `schema` (fields, types, structure), `codelist`, `guidance` (modelling and implementation guidance pages), `documentation` (reference and primer), `tooling` (validators, libraries), `governance`, `serialisation` (JSON, JSON Lines, XML, RDF).

## Status

- `observed` — written up, not yet raised upstream.
- `needs-issue` — no upstream issue exists yet.
- `raised` — posted as a comment or issue upstream (link it in `upstream_issues`).
- `resolved` — the standard or its documentation has changed in response.
- `declined` — raised upstream and not taken forward; keep the entry, record why.
