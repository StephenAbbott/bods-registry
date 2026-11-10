---
title: "BODS 0.4 data in circulation still uses the 0.3 unspecifiedReason idiom and 0.3 field names"
date: "2026-11-10"
area: "documentation"
source: ["opencheck"]
bods_versions: ["0.3", "0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/389"
status: "observed"
summary: "Published datasets stamped 0.4 still carry 0.3's unspecifiedReason key and incorporatedInJurisdiction, so consumers and validators need a migration note on how 0.3 missing-information idioms map to 0.4's unspecified record."
---

## What was observed

To read real-world 0.4 data, OpenCheck's validator has to accept both the 0.4 `reason` key and the 0.3 `unspecifiedReason` key on an unspecified relationship party. The GLEIF Level 2 Reporting Exceptions, as republished in BODS, carry the 0.3 idiom under a 0.4 version stamp. Separately, two of OpenCheck's own adapters wrote 0.3's `incorporatedInJurisdiction` into 0.4 statements. As a result, the risk engine never saw the jurisdiction of 225 of BP's entities. A guard now refuses 0.3 field names under a 0.4 stamp ([PR #307](https://github.com/StephenAbbott/opencheck/pull/307), `jurisdiction_input_issues`).

Ukraine's register shows the other side. Its 117,266 absence records each carry a stated reason, and they map cleanly onto four 0.4 `reason` values (`noBeneficialOwners`, `subjectExemptFromDisclosure`, …) once the mapper knows which idiom to use.

## Why it matters for the standard

The changelog lists the 0.3 → 0.4 renames, but there is no migration table for the missing-information idioms specifically. Those are where the shape changed most: `unspecifiedEntityDetails` and `unspecifiedPersonDetails` on parties, and an `unspecified` object in place of a reference. Data that mixes the two validates partly or not at all. Each consumer then writes its own tolerance code, and silent misreadings follow.

## Suggested change

Add a short "Migrating missing-information data from 0.3" table to the #389 guidance, mapping each 0.3 key and code to its 0.4 equivalent. Lib-cove-bods could also give a named warning for 0.3 keys under a 0.4 stamp, instead of a generic schema error.

## Evidence

- OpenCheck validator, `_is_unspecified_record` and the comment on GLEIF Reporting Exceptions — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/validator.py (accessed 2026-11-10)
- OpenCheck regimes registry, Ukraine entry (117,266 absence records, four reasons) — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/bo_regimes.py (accessed 2026-11-10)
- BODS changelog, 0.4 — https://standard.openownership.org/en/0.4.0/standard/changelog.html
