---
title: "beneficialOwnershipOrControl needs a 'not stated' reading, distinct from false"
date: "2026-11-10"
area: "guidance"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/389"
status: "observed"
summary: "Sources without a beneficial ownership regime publish legal ownership, and the only honest mapping is to omit beneficialOwnershipOrControl; the standard should say that omission means 'not stated' and that false is a positive finding."
---

## What was observed

OpenCheck maps around thirty sources. Some publish beneficial ownership declarations (UK PSC, Slovak RPVS, the Latvian and Nigerian registers). Most publish shareholders, officers or consolidation links with no beneficial ownership finding at all. Early mappers wrote `beneficialOwnershipOrControl: true` on every FtM-derived shareholding, or `false` on every director. Both claim something the source never said.

Two fixes followed:

- July 2026 ([PR #78](https://github.com/StephenAbbott/opencheck/pull/78)): the flag is asserted only where the dataset publishes beneficial ownership.
- August 2026 ([PR #187](https://github.com/StephenAbbott/opencheck/pull/187)): a per-jurisdiction regimes registry decides, per record kind, whether to assert `true`, assert `false` or omit.

Omitting the flag is now the default, and it means "the source does not say".

## Why it matters for the standard

The schema allows the flag to be omitted, but the documentation does not say what omission means. Consumers then treat absent and false alike, as "not an owner". A legal shareholder in a country with no beneficial ownership regime is then read as "checked, not a beneficial owner", which is a finding nobody made. This is the "not required" and "unknown" end of #389's typology, at the level of a single interest rather than a whole declaration.

## Suggested change

Add one sentence each to the schema reference and the beneficial ownership modelling page:

- `true` and `false` are findings
- an omitted `beneficialOwnershipOrControl` means the publisher does not state whether the interest makes the party a beneficial owner
- publishers of legal ownership data with no beneficial ownership regime SHOULD omit it

Guidance only. This belongs with the #389 work on missing information.

## Evidence

- OpenCheck PR #78, only assert the flag on FtM ownership when the dataset publishes beneficial ownership — https://github.com/StephenAbbott/opencheck/pull/78 (2026-07-23)
- OpenCheck PR #187, beneficial ownership regimes registry and the omit-not-false policy — https://github.com/StephenAbbott/opencheck/pull/187 (2026-08-30)
- OpenCheck regimes registry, generated — https://github.com/StephenAbbott/opencheck/blob/main/docs/bo-regimes.md (accessed 2026-11-10)
- Issue #389 — https://github.com/openownership/data-standard/issues/389
