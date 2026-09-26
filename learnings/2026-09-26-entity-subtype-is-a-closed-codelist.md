---
title: "entityType.subtype is a closed codelist; local entity-type wording belongs in entityType.details"
date: "2026-09-26"
area: "documentation"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/472"
status: "observed"
summary: "Three independent register mappers put the register's own entity-type wording into the closed entityType.subtype codelist and failed schema validation; the reference should state, next to subtype, that free text goes in details, with a wrong/right example."
---

## What was observed

In September 2026, while adding a Singapore ACRA adapter to OpenCheck, four source mappers (ACRA Singapore, Cyprus DRCOR, Australian ABR, Indian MCA) were found to be writing the register's own entity-type label (for example "Local Company", "Commonwealth Government Entity", "Public") into `recordDetails.entityType.subtype`. In BODS 0.4 `subtype` is a closed codelist (`governmentDepartment`, `stateAgency`, `other`, `trust`, `nomination`) whose value must also align with `entityType.type`, so every such statement failed JSON Schema validation. The correct field, `entityType.details`, is described in the schema as a place for "a local name for this type of entity". The fix moved the wording to `details` and added a registry-wide test guard; see [PR #278](https://github.com/StephenAbbott/opencheck/pull/278).

The mistake was not caught earlier because the adapters' schema tests validated fixtures that never exercised the field. That is an implementation problem. The standard-level observation is that four mappers written at different times by the same team all made the same wrong guess, which suggests the reference documentation invites it.

## Why it matters for the standard

`entityType` is one of the first objects every implementer maps, and most registers publish a local legal-form label. The reference lists `subtype`'s enum and says the value must align with `type`, but the existence of `details` as the home for local wording is easy to miss, and the two fields sit close enough together that `subtype` reads as "the more specific type". Implementers who do not run schema validation on real data (many do not) will publish invalid statements without knowing. This is also evidence for [#472](https://github.com/openownership/data-standard/issues/472) (entity classification): the demand for "precise local legal form" is real, and today it can only be met with free text.

## Suggested change

A documentation fix, non-breaking: in the schema reference entry for `entityType` and on the entity-statement modelling page, add one sentence and a paired wrong/right JSON example showing a register's own label in `details` alongside a codelist value in `subtype`. Optionally, mention in `subtype`'s description that it is closed and that `details` exists. A candidate PR is tracked in the maintainer's backlog; the longer-term answer (a legal-form codelist, for example ISO 20275 entity legal forms) belongs to #472.

## Evidence

- OpenCheck PR #278, "entityType.subtype fix and registry-wide guard" — https://github.com/StephenAbbott/opencheck/pull/278 (2026-09-16)
- BODS 0.4 schema, `entity-record.json`, `entityType.subtype` enum and `details` description — https://github.com/openownership/data-standard/blob/main/schema/entity-record.json (accessed 2026-09-26)
- BODS schema reference, Entity Type / Entity Subtype — https://standard.openownership.org/en/main/standard/reference.html (accessed 2026-09-26)
- Issue #472, Feature: update to the entity classification system — https://github.com/openownership/data-standard/issues/472 (accessed 2026-09-26)
