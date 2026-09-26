# Contributing

Thank you for helping keep a record of how BODS is used. There are three kinds of contribution, each with a template. Everything is Markdown or JSON; no build step is needed.

## Before you start

1. **Check the evidence rule.** Every statement must link to a public source. If you are documenting your own implementation and nothing is public yet, publish a short note (a README, a blog post, a mapping file) first and link to that.
2. **Search first.** Look in `implementations/`, `extensions/registry.json` and `learnings/` for an existing entry. Update rather than duplicate.
3. **Run the validator** before opening a pull request:
   ```bash
   pip install -r scripts/requirements.txt
   python scripts/validate.py
   ```

## Adding an implementation profile

1. Copy `implementations/TEMPLATE.md` to `implementations/<slug>.md`. The slug is lower-case, hyphenated, and stable: use the organisation or product name, not the country alone (`foster-moore-verne`, not `namibia`).
2. Fill in the YAML front matter. Required keys are listed in the template; `status`, `roles` and `type` use closed lists, also given in the template.
3. Write each section. Keep "What could not be modelled" concrete: the field or concept, what the implementer did instead, and a link to where that is visible.
4. In "Learnings for the standard", link to any `learnings/` entries this profile gave rise to, and to the upstream issues they feed.
5. Set `last_reviewed` to today.

If you are not the implementer, say so in the front matter (`author_relationship: third-party`) and stick to what the public sources show.

## Registering an extension

An extension is a documented set of additional fields or codes. To register one:

1. Read the normative rules in `extensions/README.md`. An extension that removes or redefines a core field will not be listed.
2. Host the extension in its own repository (or a directory of your project's repository) following the layout in `extensions/TEMPLATE/`. The essential files are `extension.json` (metadata), `README.md` (documentation with at least one example), and `schema/` (JSON Merge Patch files named after the BODS schema file they patch).
3. Add an entry to `extensions/registry.json`. Its fields mirror `extension.json`; the validator checks they agree.
4. If you would like the registry to hold a copy of the extension rather than only link to it, add it under `extensions/<slug>/` as well. This is optional; a link is enough.

Extensions are listed with a `status` of `draft`, `community` or `deprecated`. There is no "core" status: the registry does not endorse extensions, it records them.

## Recording a learning

1. Copy `learnings/TEMPLATE.md` to `learnings/YYYY-MM-DD-<slug>.md` using the date the learning was first written up.
2. State the observation in one sentence in `summary`. The body explains what happened, why it matters for the standard, and what change (if any) it suggests.
3. Link the upstream issue in `upstream_issues`. If none exists, set `status: needs-issue` and a maintainer will help open one using the [BODS issue templates](https://github.com/openownership/data-standard/issues/new/choose).
4. Where a learning came from a specific implementation, name it in `source` using the profile slug.

## Review

Pull requests are reviewed by the maintainer for the evidence rule, for accuracy against the linked sources, and for tone (describe, do not judge). Expect a review within two weeks. Small factual corrections to existing entries can be made directly in a pull request without discussion.

## Licence of contributions

By contributing content you agree it is released under CC BY 4.0 (see `LICENSE-CONTENT`); code contributions are released under MIT (see `LICENSE`).
