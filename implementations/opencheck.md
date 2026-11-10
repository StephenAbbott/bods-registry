---
name: "OpenCheck"
slug: "opencheck"
type: "tool"
organisation: "Stephen Abbott Pugh (Understand Beneficial Ownership)"
organisation_url: "https://www.beneficialownership.co.uk/"
jurisdictions: ["global"]
bods_versions: ["0.4"]
roles: ["republish", "consume"]
status: "live"
since: "2026-06"
data_url: "https://opencheck.world/"
repository_url: "https://github.com/StephenAbbott/opencheck"
extensions: []
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/389"
  - "https://github.com/openownership/data-standard/issues/464"
  - "https://github.com/openownership/data-standard/issues/466"
  - "https://github.com/openownership/data-standard/issues/769"
learnings:
  - "2026-09-26-entity-subtype-is-a-closed-codelist.md"
  - "2026-11-10-republisher-rollup-of-indirect-ownership.md"
  - "2026-11-10-psc-natures-do-not-encode-directness.md"
  - "2026-11-10-beneficial-ownership-flag-needs-a-not-stated-state.md"
  - "2026-11-10-v03-unspecified-idiom-under-v04-stamp.md"
  - "2026-11-10-annotations-dropped-by-exporters.md"
  - "2026-11-10-statementid-equal-to-recordid-hides-reference-bugs.md"
  - "2026-11-10-declaration-subject-for-republishers.md"
  - "2026-11-10-libcovebods-checks-miss-relationship-annotations.md"
author_relationship: "implementer"
last_reviewed: "2026-11-10"
---

## Summary

OpenCheck is an open-source customer due diligence tool that takes a Legal Entity Identifier (LEI), fans out across national and international corporate data sources, and assembles everything it finds into a single BODS v0.4 bundle with a layer of risk signals on top. It is a republisher rather than an original publisher: every statement it emits is derived from a register or dataset it names as the source. Because it maps around thirty sources with very different vocabularies into one schema, it exercises the standard's codelists, provenance fields and missing-information mechanisms harder than most single-register implementations.

## How BODS is used

BODS v0.4 is the internal data model and the export format. Each source adapter maps a register's own records to entity, person and relationship statements using shared factory functions; the assembled bundle is exported as JSON, JSON Lines, XML and RDF. `recordId` is deterministic (derived from source and local identifier) and, since October 2026, `statementId` is content-addressed (derived from the `recordId` and a digest of the record's content), so the two differ and a changed record gets a new `statementId`. Relationships reference parties by `recordId`. Each source bundle is a declared network whose `declarationSubject` is that source's own record of the looked-up company; lifecycle semantics are emitted only where a source expresses them (for example a ceased UK PSC becomes a relationship with `recordStatus: "closed"` and an interest `endDate`). Cross-source entity resolution is a display-layer concern and does not alter the exported statements. The UK Companies House mapping is shared with [bods-stream](https://github.com/StephenAbbott/bods-stream) through the [bods-mapper](https://github.com/StephenAbbott/bods-mapper) library, which maps all 86 PSC `natures_of_control` codes to BODS interest types.

## What was extended or adapted

No schema extension. Three adaptations of note, all visible in the repository:

- **Three-state `beneficialOwnershipOrControl`.** The flag is set `true` or `false` only for sources that publish beneficial ownership declarations (UK PSC, GLEIF/Open Ownership output, Slovak RPVS, Latvian and Nigerian registers and similar). For sources that record legal ownership without a BO regime the field is omitted, meaning "not stated", so that a legal holding is never equated with a beneficial one.
- **Republisher roll-up of indirect ownership.** Where UK corporate PSC chains lead to an individual, OpenCheck synthesises the primary indirect relationship the modelling guidance asks for, with `source.type: ["thirdParty"]`, `assertedBy` naming OpenCheck, a `transformation` annotation on `componentRecords`, and the register-sourced hops kept as `isComponent: true` secondaries. It only does so where the PSC regime's own majority-stake rule (Companies Act 2006 Sch 1A) would make the person a PSC of the subject. See [PR #233](https://github.com/StephenAbbott/opencheck/pull/233).
- **Register wording in `entityType.details`, never `subtype`.** After three adapters were found emitting free text in the closed `subtype` codelist, a registry-wide test guard was added; see [PR #278](https://github.com/StephenAbbott/opencheck/pull/278).

## What could not be modelled

- **Directness of PSC interests.** UK `natures_of_control` codes do not encode whether an interest is held directly or indirectly, so every PSC interest is emitted with `directOrIndirect: "unknown"`, which loses the cases where directness is in fact obvious.
- **Cross-source chains.** A chain whose hops come from different registers (a Companies House hop stitched to a GLEIF hop) is deliberately not rolled up into a primary relationship, because the identity of the shared entity rests on OpenCheck's own reconciliation rather than on either source. The standard has no way to express "these two records are the same entity according to the republisher".
- **Source-level licensing.** Each contributing source has its own licence; the JSON export can only carry this in a separate `LICENSES.md`, while the RDF export stamps each statement with a licence URI. `publicationDetails.license` is per statement but assumes one publisher.

## Learnings for the standard

- `entityType.subtype` is a closed codelist and a register's own wording belongs in `entityType.details`. See [the learning](../learnings/2026-09-26-entity-subtype-is-a-closed-codelist.md); raised as [#769](https://github.com/openownership/data-standard/issues/769) with [PR #770](https://github.com/openownership/data-standard/pull/770).
- A republisher can synthesise the primary indirect relationship, but nothing says how to mark it as derived. See [the learning](../learnings/2026-11-10-republisher-rollup-of-indirect-ownership.md); feeds [#464](https://github.com/openownership/data-standard/issues/464).
- UK PSC codes do not encode directness, so `directOrIndirect` must be `unknown`. See [the learning](../learnings/2026-11-10-psc-natures-do-not-encode-directness.md); feeds [#466](https://github.com/openownership/data-standard/issues/466).
- An omitted `beneficialOwnershipOrControl` needs to mean "not stated". See [the learning](../learnings/2026-11-10-beneficial-ownership-flag-needs-a-not-stated-state.md); feeds [#389](https://github.com/openownership/data-standard/issues/389).
- 0.3 missing-information idioms still circulate under a 0.4 stamp. See [the learning](../learnings/2026-11-10-v03-unspecified-idiom-under-v04-stamp.md); feeds #389.
- Exporters drop annotations. See [the learning](../learnings/2026-11-10-annotations-dropped-by-exporters.md).
- `statementId == recordId` hides consumers that join on the wrong id. See [the learning](../learnings/2026-11-10-statementid-equal-to-recordid-hides-reference-bugs.md).
- `declarationSubject` is undefined for a republisher that merges sources. See [the learning](../learnings/2026-11-10-declaration-subject-for-republishers.md).
- lib-cove-bods checks annotation pointers on entity statements only. See [the learning](../learnings/2026-11-10-libcovebods-checks-miss-relationship-annotations.md).
- Mapping thirty source vocabularies onto the 23 interest types is a ready-made coverage test for any proposal under [#466](https://github.com/openownership/data-standard/issues/466).

## Sources

- OpenCheck repository — https://github.com/StephenAbbott/opencheck (accessed 2026-09-26)
- OpenCheck live instance — https://opencheck.world/ (accessed 2026-09-26)
- PR #233, component roll-up for UK PSC chains — https://github.com/StephenAbbott/opencheck/pull/233 (2026-09-08)
- PR #278, entityType.subtype fix and registry-wide guard — https://github.com/StephenAbbott/opencheck/pull/278 (2026-09-16)
- bods-mapper, shared Companies House PSC → BODS v0.4 mapping — https://github.com/StephenAbbott/bods-mapper (accessed 2026-09-26)
- BODS modelling guidance: representing beneficial ownership — https://standard.openownership.org/en/main/standard/modelling/repr-beneficial-ownership.html (accessed 2026-09-26)
