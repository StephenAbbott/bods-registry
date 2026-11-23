---
title: "The OECD's IPI MCAA field list shows that representing assets in BODS needs a link with a right, a fraction and dates, not only an asset record"
date: "2026-11-23"
area: "schema"
source: []
bods_versions: ["0.4"]
upstream_issues:
  - "https://github.com/openownership/data-standard/issues/752"
  - "https://github.com/openownership/data-standard/issues/752#issuecomment-7115824286"
status: "raised"
summary: "Of the 38 information items in the OECD's agreement on exchanging real estate information, BODS 0.4 carries 16 of the 17 about people and entities and none of the 21 about the asset; the nine in-scope asset items split into three about the asset and six about the holder's link to it, which have the shape of a BODS interest, and an entity's tax residence has no field."
---

## What was observed

In October 2025 the OECD published the Framework for the Automatic Exchange of Readily Available Information on Immovable Property for Tax Purposes. It contains the IPI MCAA, an agreement under which tax authorities exchange information on real estate held, bought, sold or rented out by each other's residents. Twenty-five jurisdictions said on 4 December 2025 that they aim to join by 2029 or 2030, and Indonesia has joined them since. The agreement covers only "readily available" information and names "immovable property registers and Beneficial Owner registers" as its sources. The exchange format will be an XML schema.

The Annex to the agreement lists the information items. Counting each item once per block, there are 38 items in seven blocks. Read against the BODS 0.4.0 schema:

| Block | IPI MCAA item | BODS 0.4 |
|---|---|---|
| Asset | Address of the asset | None |
| Asset | Unique reference number | None |
| Asset | Type of immovable property | None |
| Asset | Value | None (tax and valuation data) |
| Asset | Date of last determination of the value | None (tax and valuation data) |
| Asset | Type of ownership or property rights | None; describes the holder's link to the asset, like `interests[].type` |
| Asset | Fraction of ownership | None; describes the link, like `interests[].share` |
| Transaction, holdings and acquisitions | Price | None (tax and valuation data) |
| Transaction, holdings and acquisitions | Date of acquisition | None; describes the link, like `interests[].startDate` |
| Transaction, holdings and acquisitions | Mode of acquisition | None; describes the link |
| Transaction, holdings and acquisitions | Financing information | None (tax and valuation data) |
| Transaction, disposals | Price | None (tax and valuation data) |
| Transaction, disposals | Capital gain | None (tax and valuation data) |
| Transaction, disposals | Year to which the capital gain relates | None (tax and valuation data) |
| Transaction, disposals | Date of disposal | None; describes the link, like `interests[].endDate` |
| Transaction, disposals | Mode of disposal | None; describes the link |
| Transaction, disposals | Taxes paid | None (tax and valuation data) |
| Income | Amount of the income | None (tax and valuation data) |
| Income | Type of income | None (tax and valuation data) |
| Income | Taxes paid | None (tax and valuation data) |
| Income | Year to which the income relates | None (tax and valuation data) |
| Legal owner, individual | Name | person `names[].fullName` |
| Legal owner, individual | Jurisdiction of tax residence | person `taxResidencies[]` |
| Legal owner, individual | Address in the jurisdiction in respect of which the individual is a Relevant Person | person `addresses[]` |
| Legal owner, individual | Resident TIN | person `identifiers[]`, scheme `{ISO3}-TAXID` |
| Legal owner, individual | Date of birth | person `birthDate` |
| Legal owner, Entity | Name | entity `name` |
| Legal owner, Entity | Type of Entity | entity `entityType` (`type`, `subtype`, `details`), in part: the OECD's code list is not published |
| Legal owner, Entity | Jurisdiction of tax residence | **None.** Entity records have `jurisdiction` only |
| Legal owner, Entity | Address in the jurisdiction in respect of which the Entity is a Relevant Person | entity `addresses[]` |
| Legal owner, Entity | Resident TIN | entity `identifiers[]` |
| Legal owner, Entity | Resident Business Identification Number | entity `identifiers[]` |
| Beneficial Owner | Name | person `names[].fullName` |
| Beneficial Owner | Type of Beneficial Owner | relationship `interests[].type`, `beneficialOwnershipOrControl`, `directOrIndirect` |
| Beneficial Owner | Jurisdiction of tax residence | person `taxResidencies[]` |
| Beneficial Owner | Address in the jurisdiction in respect of which the Beneficial Owner is a Relevant Person | person `addresses[]` |
| Beneficial Owner | Resident TIN | person `identifiers[]`, scheme `{ISO3}-TAXID` |
| Beneficial Owner | Date of birth | person `birthDate` |

The agreement defines "Entity" as "a legal person or a legal arrangement, such as a corporation, a partnership, a trust, or a foundation", and "Beneficial Owner" as "the individual that exercises ultimate effective control over an Entity, as defined in domestic law implementing the FATF's International Standards". Its Minimum Data Set for the asset is "the address or other unique identifier" and the price or value.

In summary:

- 16 of the 17 items about individuals, entities and beneficial owners have a BODS 0.4 field. The one without is an entity's jurisdiction of tax residence.
- None of the 21 items about the asset, the transaction or the income has a BODS 0.4 field.
- 12 of those 21 are tax and valuation data.
- The other 9 are three that describe the asset (address, unique reference number, type) and six that describe the link between a holder and the asset (type of ownership or property rights, fraction of ownership, date and mode of acquisition, date and mode of disposal).
- The Beneficial Owner block is flat: one individual and a type. It has no intermediate entities, no statement date and no source.

## Why it matters for the standard

The feature ticket on representing assets (data-standard #752) suggests a minimal asset record with `assetType`, `assetId` and `assetName`, and asks what user needs it would meet. The IPI MCAA is the first intergovernmental field list for exchanging information that joins an asset register to beneficial ownership information, so it is a concrete test of that proposal.

The test shows two things. A minimal asset record would cover the three items about the asset, if it can hold an address. It would not cover the six items about the link, and those are what make the data useful: which right is held, what fraction, from when and until when. They have the same shape as a BODS interest (`type`, `share`, `startDate`, `endDate`). So an asset feature would also need a relationship that can point at an asset, and an interest type list that can name property rights.

If assets stay outside BODS, which the ticket treats as a reasonable outcome, the IPI MCAA still shows where BODS is needed. The agreement's Beneficial Owner block cannot carry an ownership chain, and BODS can. The join between the two then depends on the land register holding an entity identifier that the beneficial ownership register also uses.

The missing entity tax residence is a smaller, separate finding. Tax authorities are a growing class of BODS data user, and tax residence of an entity can differ from its jurisdiction of formation.

## Suggested change

No schema change on this evidence alone. Three things for the #752 discussion:

1. Record the IPI MCAA field list on the ticket as a use case, with the split between asset items and link items.
2. If an asset record is taken forward, design the relationship to an asset at the same time, reusing the interest structure.
3. Consider whether entity records should be able to carry tax residence, as person records can (`taxResidencies`). This would be an additive change.

Outside the schema: a guidance note on joining BODS data to an asset register through entity identifiers would help land registers and tax authorities now, whatever is decided on assets.

## Evidence

- OECD, Framework for the Automatic Exchange of Readily Available Information on Immovable Property for Tax Purposes, October 2025, Annex on pages 14 to 16 — https://www.oecd.org/content/dam/oecd/en/topics/policy-issues/tax-transparency-and-international-co-operation/framework-for-the-automatic-exchange-of-readily-available-information-on-immovable-property-for-tax-purposes.pdf (accessed 2026-11-23)
- Joint statement of 4 December 2025 on the IPI MCAA — https://www.oecd.org/content/dam/oecd/en/topics/policy-issues/tax-transparency-and-international-co-operation/joint-statement-ipi-mcaa.pdf (accessed 2026-11-23)
- BODS 0.4.0 schema — https://github.com/openownership/data-standard/tree/0.4.0/schema (accessed 2026-11-23)
- data-standard issue #752, Feature: Representing assets — https://github.com/openownership/data-standard/issues/752 (2025-12-12)
- Open Ownership, Bridging the gap for effective asset transparency — https://www.openownership.org/en/publications/bridging-the-gap-for-effective-asset-transparency/ (2026-01-26)
