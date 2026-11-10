---
title: "lib-cove-bods checks annotation pointers on entity statements only, so bad pointers on relationship statements pass validation"
date: "2026-11-10"
area: "tooling"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues: []
status: "needs-issue"
summary: "lib-cove-bods' annotation_statement_pointer_target_invalid check runs on entity statements only; a relationship statement whose annotation points at nothing, or at a sentence, passes every check."
---

## What was observed

OpenCheck's Ukrainian ЄДР mapper wrote two founder-share annotations whose `statementPointerTarget` was a sentence rather than a JSON Pointer. The argument order had been swapped. The statements were relationship statements, and they passed lib-cove-bods without a warning, because its `annotation_statement_pointer_target_invalid` check runs on entity statements only. OpenCheck's weekly BODS quality sweep now has its own `annotation_pointer_invalid` rule, which applies to every statement type.

A related gap showed up on OpenCheck's side in September 2026 ([PR #250](https://github.com/StephenAbbott/opencheck/pull/250)). An invalid person identifier had shipped since the first release, because only the company bundle, not the officer bundle, was run through lib-cove-bods. That is an implementation lesson rather than a standard one, but it makes the same point: validator coverage is only as good as the data it is given.

## Why it matters for the standard

Annotations are the documented way to carry caveats on any field ([languages guidance](https://standard.openownership.org/en/0.4.0/standard/modelling/languages.html), transformations), and relationship statements are where the caveats matter most: shares, interest types, dates. A pointer that resolves to nothing is useless to a consumer, and the JSON Schema cannot catch it. Implementers reasonably assume that a clean lib-cove-bods run covers this.

## Suggested change

Run the pointer check in lib-cove-bods on all statement types, and add a test fixture with a bad pointer on a relationship statement. Until then, mention the check's scope in the validation documentation. This needs an issue on openownership/lib-cove-bods, which could be cross-referenced from the data-standard repository's validation docs.

## Evidence

- OpenCheck BODS quality sweep, `annotation_pointer_invalid` — https://github.com/StephenAbbott/opencheck/blob/main/docs/bods-quality.md (accessed 2026-11-10)
- OpenCheck PR #250, validate the officer-appointments path against lib-cove-bods — https://github.com/StephenAbbott/opencheck/pull/250 (2026-09-09)
- lib-cove-bods — https://github.com/openownership/lib-cove-bods
