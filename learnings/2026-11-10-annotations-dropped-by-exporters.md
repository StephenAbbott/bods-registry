---
title: "Exporters drop BODS annotations even when the target format has the vocabulary for them"
date: "2026-11-10"
area: "serialisation"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues: []
status: "needs-issue"
summary: "OpenCheck's RDF export had the annotation vocabulary but silently dropped every statement annotation; the serialisation docs should say annotations are part of the statement and must survive conversion, and conversion tools should be checked for it."
---

## What was observed

In August 2026 OpenCheck began emitting BODS `annotations` that record what a register actually said ([PR #120](https://github.com/StephenAbbott/opencheck/pull/120)), for example:

- the Companies House nature-of-control code behind an `otherInfluenceOrControl` interest
- a note that a `birthDate` was published imprecise, not truncated by OpenCheck

The RDF export dropped every one of them. The exporter already emitted `Annotation`, `motivation`, `statementPointerTarget` and the related terms, but only for OpenCheck's own analysis notes, and it never read `stmt["annotations"]`. The fix ([PR #124](https://github.com/StephenAbbott/opencheck/pull/124)) emits both, separated by named graph. It also corrected a codelist namespace that had been wrong since the exporter was written.

## Why it matters for the standard

Annotations are how BODS carries provenance and caveats: "the register said X, we mapped it to Y". An export that loses them turns a mapping that can be checked into one that cannot, and nothing fails when that happens. The serialisation pages do not say that annotations are part of the statement for conversion purposes, so implementers treat them as optional decoration.

## Suggested change

Add a sentence to the serialisation guidance: a conversion between BODS serialisations (JSON, JSON Lines, RDF, tabular) MUST keep `annotations`, or say that it does not. Add an annotation to the RDF vocabulary's worked example, if there is one. Worth checking the BODS tabular (flatten) and RDF tools for the same gap. Needs a new upstream issue.

## Evidence

- OpenCheck PR #120, provenance annotations — https://github.com/StephenAbbott/opencheck/pull/120 (2026-08-14)
- OpenCheck PR #124, emit statement annotations in RDF, and fix the codelist namespace — https://github.com/StephenAbbott/opencheck/pull/124 (2026-08-15)
- BODS serialisation guidance — https://standard.openownership.org/en/0.4.0/standard/system/serialisation.html (accessed 2026-11-10)
