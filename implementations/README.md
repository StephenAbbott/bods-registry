# Implementation profiles

One Markdown file per implementation of BODS, with YAML front matter for the structured facts and prose sections for the rest. `TEMPLATE.md` is the starting point; `opencheck.md` is a filled-in example.

## What counts as an implementation

Anything that produces, collects, transforms, republishes or consumes BODS data and is documented publicly:

| `type` | Examples |
|---|---|
| `national-register` | A government register publishing or collecting data in BODS (Latvia, Nigeria CAC, Armenia) |
| `register-software` | A register product that uses BODS internally or as an output (Foster Moore Verne, NRD BOREG) |
| `data-publisher` | An organisation publishing its own dataset in or aligned with BODS (Global Energy Monitor, EITI) |
| `data-republisher` | An aggregator that re-emits others' data as BODS or converts BODS onward (OpenSanctions, Open Ownership Register) |
| `data-user` | An analysis, research or investigation use of BODS data (Government Transparency Institute, GraphAware) |
| `standard-or-spec` | Another standard or specification that adopts BODS terms or codelists (European Business Wallet / WE BUILD) |
| `tool` | Software that reads, writes, validates or visualises BODS (OpenCheck, bods-validator, bods-dagre) |

## Roles

An implementation can play several `roles`, drawn from: `collect` (uses BODS to structure data collection, e.g. forms), `store` (uses BODS as an internal data model), `publish` (emits BODS data as an original publisher), `republish` (emits BODS derived from others' data), `consume` (reads BODS data), `reference` (uses BODS definitions or codelists without emitting BODS data).

## Status

`live`, `pilot`, `paused`, `planned`, `historic`. Use `historic` for implementations that no longer operate but remain documented (they are often the most instructive).

## Required sections

The validator checks that every profile has these second-level headings, in this order:

1. Summary
2. How BODS is used
3. What was extended or adapted
4. What could not be modelled
5. Learnings for the standard
6. Sources

An empty section should say "Nothing recorded yet" rather than be omitted, so a reader can tell the difference between "nothing" and "not looked at".
