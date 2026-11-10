---
title: "A republisher can synthesise the primary indirect relationship the guidance asks for, but the standard does not say how to mark it as derived"
date: "2026-11-10"
area: "guidance"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/464"
status: "observed"
summary: "Republishers that join register-sourced hops into a primary indirect relationship need guidance on how to flag it as their own derivation (source.type thirdParty, assertedBy, a transformation annotation) and when they may assert it at all."
---

## What was observed

UK Companies House publishes each corporate PSC hop separately: person → holding company, holding company → subject. Mapped one-to-one, a chain gives two register-sourced relationships and nothing linking the person to the subject. So the standard query for beneficial owners (subject = X, `beneficialOwnershipOrControl: true`) cannot answer "who owns X" from the export. The [modelling guidance](https://standard.openownership.org/en/0.4.0/standard/modelling/repr-beneficial-ownership.html) asks for a primary relationship with `isComponent: false` and `componentRecords` listing the hops, but it is written for a publisher that knows the chain first-hand.

In September 2026 OpenCheck began building that primary relationship itself ([PR #233](https://github.com/StephenAbbott/opencheck/pull/233)):

- `directOrIndirect: "indirect"`, `beneficialOwnershipOrControl: true`
- `source.type: ["thirdParty"]`, with `assertedBy` naming OpenCheck
- a `transformation` annotation on `/recordDetails/componentRecords`
- the register-sourced hops kept unchanged and marked `isComponent: true`

It only does this where the register's own rule makes the person a PSC of the subject. Under Companies Act 2006 Sch 1A paras 18–19, that means a majority stake at every hop. It never does it for a chain whose hops come from different registers.

## Why it matters for the standard

Every republisher of register data meets this, and each one has to invent its own answer to three questions:

- How do you show that a relationship is the republisher's inference and not the register's statement?
- Which fields carry that?
- When is the inference safe?

Without guidance, a consumer cannot tell a register-asserted primary relationship from a computed one. A naive roll-up (any chain, any share) asserts beneficial ownership the register never found.

## Suggested change

Add a worked example to the republishing and provenance guidance (#464), or to the beneficial ownership modelling page, showing a synthesised primary relationship with the fields above. Add one sentence saying a republisher SHOULD only roll up where the source's own legal test for indirect control is met. Guidance only, with no schema change.

## Evidence

- OpenCheck PR #233, component roll-up for UK PSC chains — https://github.com/StephenAbbott/opencheck/pull/233 (2026-09-08)
- OpenCheck implementation, `_rollup_ch_chains` — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/mappers/companies_house.py (accessed 2026-11-10)
- BODS modelling guidance, Representing beneficial ownership — https://standard.openownership.org/en/0.4.0/standard/modelling/repr-beneficial-ownership.html (accessed 2026-11-10)
- Issue #464 — https://github.com/openownership/data-standard/issues/464 (accessed 2026-11-10)
