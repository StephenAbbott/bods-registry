---
title: "It is unclear what declarationSubject should be when a republisher merges several sources' records of one company"
date: "2026-11-10"
area: "documentation"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues: []
status: "needs-issue"
summary: "declarationSubject is defined for a single declared network; a republisher that combines several sources' records of the same subject must choose between one subject per source and one merged subject, and the standard gives no guidance."
---

## What was observed

BODS 0.4 says every statement about a declared network MUST carry the subject's `recordId` as its `declarationSubject`. OpenCheck's statement factories had defaulted each party to its own `recordId`, and each relationship to its immediate subject's. An Ørsted lookup on 22 Oct 2026 showed a Wikidata party with `statementId == recordId == declarationSubject`.

Fixing it ([PR #478](https://github.com/StephenAbbott/opencheck/pull/478)) meant answering a question the standard does not address. A lookup holds several sources' separate records of the same company, so which record is "the subject"? OpenCheck chose one subject per source. Each source bundle's statements name that source's own record of the company, so each bundle read alone is a well-formed declared network.

There was a side effect. A consumer that had used `declarationSubject` as an alias for lookup resolution pointed a chain's middle company at the subject, and the alias was removed.

## Why it matters for the standard

Republishing and aggregating are where most BODS data is consumed, and `declarationSubject` is the field that lets a consumer split a file back into declarations. If republishers choose differently (per source, per merged entity, or each party's own id), the field cannot be relied on across datasets. The definition also does not say that `declarationSubject` is not a reference to resolve.

## Suggested change

Add a paragraph to the declarations guidance for republishers. A republisher that combines sources SHOULD keep each source's network separate, each with its own subject's `recordId` as `declarationSubject`. Say explicitly that `declarationSubject` groups statements and is not a party reference. This could sit with #464 on republishing, or in a new issue.

## Evidence

- OpenCheck PR #478, declarationSubject names the network's subject, per source — https://github.com/StephenAbbott/opencheck/pull/478 (2026-10-23)
- BODS schema, `declarationSubject` — https://standard.openownership.org/en/0.4.0/standard/reference.html (accessed 2026-11-10)
