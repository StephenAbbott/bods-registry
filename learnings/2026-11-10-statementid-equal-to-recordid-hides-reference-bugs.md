---
title: "Publishing statementId equal to recordId hides consumers that join relationships on the wrong id"
date: "2026-11-10"
area: "guidance"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues: []
status: "needs-issue"
summary: "A publisher that never versions records can make statementId equal recordId, and every consumer that joins relationship parties on statementId then works by accident until the first dataset that does not; the record-ids guidance should warn about this and give a test."
---

## What was observed

In BODS 0.4, a relationship's `subject` and `interestedParty` hold the party's `recordId`. OpenCheck never versions records, so for its first two hundred phases every mapper set `statementId == recordId`. Every consumer it built (the risk engine, the graph, the report diagrams, the Neo4j, FtM and Senzing exports) joined relationships to parties on `statementId`, and every one of them worked.

The first dataset with distinct ids was the OECD's MEIP release in BODS 0.4, which has hash `statementId`s and `meip-entity-N` `recordId`s. Its first production lookup drew A/S Norske Shell and SHELL PLC as two unlinked nodes.

The fix ([PR #270](https://github.com/StephenAbbott/opencheck/pull/270)) added one resolver per side. In October 2026 OpenCheck went further:

- [PR #479](https://github.com/StephenAbbott/opencheck/pull/479) added a "scramble" test harness that pulls every `statementId` apart from its `recordId` and runs every consumer on both shapes.
- [PR #480](https://github.com/StephenAbbott/opencheck/pull/480) made `statementId` content-addressed, so the two now differ everywhere.

## Why it matters for the standard

The [record identifiers](https://standard.openownership.org/en/0.4.0/standard/modelling/record-ids.html) page allows the equal-ids shortcut. It does not warn that the shortcut hides a whole class of consumer bug. Tools and analyses built against one publisher's data, which is how most are built, will break silently on the next publisher's.

## Suggested change

Add a note to the record identifiers page:

- consumers MUST resolve relationship parties by `recordId`
- test data SHOULD include statements whose `statementId` differs from their `recordId`

Ideally, also add an example in the repository's `examples/` with distinct ids and a relationship that references one by `recordId`. Needs a new upstream issue.

## Evidence

- OpenCheck PR #270, resolve relationship parties by recordId — https://github.com/StephenAbbott/opencheck/pull/270 (2026-09-15)
- OpenCheck PR #479, the scramble harness — https://github.com/StephenAbbott/opencheck/pull/479 (2026-10-23)
- OpenCheck PR #480, content-addressed statement ids — https://github.com/StephenAbbott/opencheck/pull/480 (2026-10-23)
- BODS record identifiers guidance — https://standard.openownership.org/en/0.4.0/standard/modelling/record-ids.html (accessed 2026-11-10)
