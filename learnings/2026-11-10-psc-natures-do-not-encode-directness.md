---
title: "UK PSC nature-of-control codes do not say whether an interest is direct or indirect, so directOrIndirect must be unknown"
date: "2026-11-10"
area: "guidance"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/466"
status: "observed"
summary: "Every Companies House PSC condition is met by holding an interest 'directly or indirectly' and the natures_of_control codes do not say which, so a mapping that writes directOrIndirect 'direct' over-asserts; the UK mapping guidance and #466 should say so."
---

## What was observed

OpenCheck's Companies House mapper first emitted `directOrIndirect: "direct"` for every PSC interest, because that is the natural reading of "a person with significant control". In September 2026 it was changed to `"unknown"` ([PR #233](https://github.com/StephenAbbott/opencheck/pull/233)). Each PSC condition in Schedule 1A to the Companies Act 2006 is met by holding the interest "directly or indirectly", and none of the 86 `natures_of_control` codes says which. The BODS modelling guidance says that where directness is not known, `directOrIndirect` MUST be `unknown`.

The same over-assertion is easy to make and easy to miss. On 10 Nov 2026 the shared [bods-mapper](https://github.com/StephenAbbott/bods-mapper) library, which another pipeline uses for the same mapping, still wrote `"direct"`. That is corrected in [bods-mapper PR #2](https://github.com/StephenAbbott/bods-mapper/pull/2).

## Why it matters for the standard

UK PSC data is the largest open source of BODS data, and anything that reads directness from it (layer counts, chain analysis, "held directly" summaries) gets a false answer. "Unknown" is also unsatisfying. In a chain the register itself documents, directness is in fact clear, and BODS has no way to say "unknown at the hop, known from the chain".

## Suggested change

Short term: the UK PSC mapping notes and any published PSC → BODS mapping should say `directOrIndirect: "unknown"` for nature-of-control codes. Longer term: #466 interest modelling should treat directness as a property that can be derived, and record whether it was asserted or derived.

## Evidence

- OpenCheck `_parse_nature`, with the reasoning in a comment — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/statements.py (accessed 2026-11-10)
- OpenCheck PR #233 — https://github.com/StephenAbbott/opencheck/pull/233 (2026-09-08)
- bods-mapper `parse_nature` writing "direct" — https://github.com/StephenAbbott/bods-mapper/blob/main/src/bods_mapper/natures.py (accessed 2026-11-10)
- Companies Act 2006, Schedule 1A — https://www.legislation.gov.uk/ukpga/2006/46/schedule/1A
- bods-mapper PR #2, directness set to unknown — https://github.com/StephenAbbott/bods-mapper/pull/2 (2026-11-10)
