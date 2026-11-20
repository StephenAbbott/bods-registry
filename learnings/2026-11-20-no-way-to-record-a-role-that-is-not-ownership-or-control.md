---
title: "BODS has no way to record a role that is neither ownership nor control, so registered agents, secretaries and other service providers are dropped or mis-typed"
date: "2026-11-20"
area: "schema"
source: ["opencheck"]
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/626"
  - "https://github.com/openownership/data-standard/pull/781"
  - "https://github.com/openownership/data-standard/issues/466"
status: "raised"
summary: "Registers publish company secretaries, registered agents, incorporators and authorised representatives who hold no interest; BODS 0.4 can only drop them or type them as otherInfluenceOrControl, and OpenCheck needed an extension field to stop readers drawing them as controllers, so #466 should add a way to record a non-controlling role."
---

## What was observed

Many of the registers OpenCheck reads name people and companies who act for an entity but neither own nor control it. BODS 0.4 has two options for them: leave them out, or write a Relationship statement with an interest type, which says they have an interest in the entity. OpenCheck has used both, depending on the source.

- **Left out.** Florida's Sunbiz file names a registered agent for every company. The mapper puts it in the finding and the bundle, not in BODS, because "it holds no role in the company" (`bods/mappers/us_fl.py`). Connecticut publishes a separate Agents dataset, which OpenCheck does not read. Companies House publishes no presenter, so the declarant is always the company (`bods/ch_filings.py`), and `source.assertedBy` has nothing to say about an agent who filed.
- **Typed as control, then marked.** Companies House and OpenCorporates company secretaries and limited partners, Cypriot secretaries (most of them fiduciary companies), Pennsylvania organisers and incorporators, Taiwanese supervisors and litigation agents, Bulgarian liquidators and procurators, and Korean statutory auditors are all written as `otherInfluenceOrControl`, the nearest code. Phase 197 moved secretaries off `seniorManagingOfficial`. That was not enough: every reader that classifies an edge by interest type (the canvas, the PDF diagram, the MCP ownership map) then drew a company secretary as a controller. Phase 352 found this on Unilever PLC, where `opencheck_ownership_map` drew the company secretary as a "Controls" edge. The fix was an extension field on the interest, `opencheckOfficerPosition`, which OpenCheck's own readers treat as "a role, not control" (`bods/officer_roles.py`). Seven mappers now set it. Any other BODS consumer still reads these as control.

ICIJ Offshore Leaks has the same split. Its `Intermediary` node is the law firm or formation agent that arranged a structure, and OpenCheck words a match on it differently from a match on an officer or owner (`icij_check.py`). FollowTheMoney gives these relationships their own `Representation` schema, separate from `Ownership` and `Directorship`.

## Why it matters for the standard

A publisher that maps a whole register has to either lose information users want (who the agent or secretary is, which formation agent a network of companies shares) or overstate control. Overstating control reaches every downstream reader: network diagrams, "who controls this company" answers and related-party screens all treat an `otherInfluenceOrControl` edge as control. OpenCheck's extension field fixes this for OpenCheck only.

The draft guidance for #626 says service relationships SHOULD NOT be Relationship statements and points to annotations in the meantime. That keeps the ownership graph honest, but annotations are not a graph: a formation agent shared across fifty companies cannot be traversed or screened. OpenCheck chose to keep its officers as relationships with a marker for exactly that reason, so its current practice does not follow the guidance.

## Suggested change

Short term: the #626 guidance (a new page, *Representing professional intermediaries*, proposed in data-standard PR #781) documents what BODS 0.4 can and cannot say, and recommends `source.assertedBy` for filing agents and annotations for service relationships.

Longer term, as part of #466: a way to record a role that carries no ownership or control. Options, from smallest to largest: an interest-level flag (OpenCheck's `opencheckOfficerPosition` is a working example); role codes outside the ownership-or-control set (secretary, registered agent, formation agent, auditor, legal adviser, introducer) that readers know not to count as control; or a separate relationship kind, like FollowTheMoney's `Representation`. Any of these is a schema change. A candidate for the registry's `agents` extension category in the meantime.

## Evidence

- OpenCheck `officer_roles.py`, the `opencheckOfficerPosition` extension field and why it exists — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/officer_roles.py (accessed 2026-11-20)
- OpenCheck Companies House mapper, secretaries marked as officers — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/mappers/companies_house.py (accessed 2026-11-20)
- OpenCheck Florida mapper, registered agent not a party — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/mappers/us_fl.py (accessed 2026-11-20)
- OpenCheck Cyprus mapper, fiduciary-company secretaries — https://github.com/StephenAbbott/opencheck/blob/main/backend/opencheck/bods/mappers/cyprus.py (accessed 2026-11-20)
- OpenCheck status, Phases 197 and 352 — https://github.com/StephenAbbott/opencheck/blob/main/docs/status.md (accessed 2026-11-20)
- OpenSanctions mapping of ICIJ Offshore Leaks roles to FollowTheMoney, including `Representation` — https://github.com/opensanctions/opensanctions/blob/main/datasets/_global/icij_offshoreleaks/icij_offshoreleaks.yml (accessed 2026-11-16)
- data-standard issue #626 — https://github.com/openownership/data-standard/issues/626
- data-standard PR #781, the guidance page — https://github.com/openownership/data-standard/pull/781 (2026-11-20)
