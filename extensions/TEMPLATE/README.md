# Template extension

> Copy this directory to start a new extension. Replace every section below. Keep the headings: the registry validator looks for **Purpose**, **Fields**, **Codelists** and **Example**.

## Purpose

One or two paragraphs. What information does this extension carry that the core BODS schema cannot? Who needs it, and in what process (a register's filing form, a due-diligence product, a sectoral dataset)? If a core field was considered and rejected, say which and why.

## Fields

List every field the extension adds, with its JSON path relative to the statement, type, and meaning. Group new fields under a single namespace object named after the extension (rule 8 in [`extensions/README.md`](../README.md)).

| Path | Type | Required | Description |
|---|---|---|---|
| `recordDetails.templateExtension` | object | no | Container for this extension's fields on an entity record. |
| `recordDetails.templateExtension.exampleStatus` | string (codelist `exampleStatus`) | no | An illustrative status drawn from the `exampleStatus` codelist. |
| `recordDetails.templateExtension.exampleNote` | string | no | Free-text note accompanying the status. |

The machine-readable version of this table is the JSON Merge Patch in [`schema/entity-record.json`](schema/entity-record.json), which is applied to the BODS 0.4 `entity-record.json` schema.

## Codelists

| Codelist | File | Open or closed | Notes |
|---|---|---|---|
| `exampleStatus` | [`codelists/exampleStatus.csv`](codelists/exampleStatus.csv) | closed | New codelist introduced by this extension. |

To add codes to an existing **open** BODS codelist, name the file `+<codelist>.csv` (for example `+addressType.csv`). Closed core codelists cannot be extended (rule 4).

## Example

[`examples/example.json`](examples/example.json) is a BODS 0.4 statement array containing one entity statement that uses the extension. It validates against the core schema with this extension's patch applied.

## Changelog

- 0.1.0 — first draft.
