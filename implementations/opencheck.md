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
learnings:
  - "2026-09-26-entity-subtype-is-a-closed-codelist.md"
author_relationship: "implementer"
last_reviewed: "2026-09-26"
---

## Summary

OpenCheck is an open-source customer due diligence tool that takes a Legal Entity Identifier (LEI), fans out across national and international corporate data sources, and assembles everything it finds into a single BODS v0.4 bundle with a layer of risk signals on top. It is a republisher rather than an original publisher: every statement it emits is derived from a register or dataset it names as the source. Because it maps around thirty sources with very different vocabularies into one schema, it exercises the standard's codelists, provenance fields and missing-information mechanisms harder than most single-register implementations.

## How BODS is used

BODS v0.4 is the internal data model and the export format. Each source adapter maps a register's own records to entity, person and relationship statements using shared factory functions; the assembled bundle is exported as JSON, JSON Lines, XML and RDF. Statement identifiers are deterministic (derived from source and local identifier) and `recordId` equals `statementId`, because OpenCheck never versions records itself; lifecycle semantics are emitted only where a source expresses them (for example a ceased UK PSC becomes a relationship with `recordStatus: "closed"` and an interest `endDate`). Cross-source entity resolution is a display-layer concern and does not alter the exported statements. The UK Companies House mapping is shared with [bods-stream](https://github.com/StephenAbbott/bods-stream) through the [bods-mapper](https://github.com/StephenAbbott/bods-mapper) library, which maps all 86 PSC `natures_of_control` codes to BODS interest types.

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

- `entityType.subtype` is a closed codelist and the natural home for a register's own wording is `entityType.details`; the documentation does not make this obvious enough to stop implementers getting it wrong. See [learnings/2026-09-26-entity-subtype-is-a-closed-codelist.md](../learnings/2026-09-26-entity-subtype-is-a-closed-codelist.md). Feeds a documentation fix and [#472](https://github.com/openownership/data-standard/issues/472).
- The republisher roll-up pattern (a synthesised primary with `thirdParty` source and a `transformation` annotation) is a candidate for guidance under [#464](https://github.com/openownership/data-standard/issues/464) on republishing and provenance.
- The three-state treatment of `beneficialOwnershipOrControl` is evidence for [#389](https://github.com/openownership/data-standard/issues/389) on representing missing information: "not stated" and "false" need to be distinguishable.
- Mapping thirty source vocabularies onto the 23 interest types is a ready-made coverage test for any proposal under [#466](https://github.com/openownership/data-standard/issues/466).

## Sources

- OpenCheck repository — https://github.com/StephenAbbott/opencheck (accessed 2026-09-26)
- OpenCheck live instance — https://opencheck.world/ (accessed 2026-09-26)
- PR #233, component roll-up for UK PSC chains — https://github.com/StephenAbbott/opencheck/pull/233 (2026-09-08)
- PR #278, entityType.subtype fix and registry-wide guard — https://github.com/StephenAbbott/opencheck/pull/278 (2026-09-16)
- bods-mapper, shared Companies House PSC → BODS v0.4 mapping — https://github.com/StephenAbbott/bods-mapper (accessed 2026-09-26)
- BODS modelling guidance: representing beneficial ownership — https://standard.openownership.org/en/main/standard/modelling/repr-beneficial-ownership.html (accessed 2026-09-26)
