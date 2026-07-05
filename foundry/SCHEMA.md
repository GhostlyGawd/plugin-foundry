# SCHEMA — anatomy of a foundry record

Every plugin has exactly one record: `foundry/records/<plugin-name>.md` — the job
traveler that follows it down the line. **Process lives here; the shippable artifact
lives in `plugins/<plugin-name>/` and contains only what installers should receive.**
Records are never deleted: shelved and deprecated plugins keep theirs forever.

## Front matter (all keys required)

```yaml
---
name: commit-craft            # kebab-case; must equal the plugins/ dir once building
title: Commit Craft
category: workflow            # must exist in foundry/categories.json
stage: spec                   # idea | spec | building | rc | published | deprecated | shelved
version: null                 # mirrors plugin.json once building; semver
kind: plugin                  # plugin | feature (engagement/site/system work — see GROWTH.md)
components: [skills, hooks]   # plugins: skills|agents|hooks|mcp|lsp|output-styles · features: site|workflow|template|worker|docs
one_liner: Drafts conventional commits from the staged diff and guards message format.
tags: [git, conventional-commits]
created: 2026-07-04
updated: 2026-07-04
---
```

## Sections by stage — each stage requires all previous stages' sections

**idea** (Ideator)
1. `# {title}` — one paragraph: the friction observed.
2. `## Pitch` — the job (one sentence), the user, sketch of components, and why a
   plugin (vs. a note in CLAUDE.md or a one-off prompt).

**spec** (Builder)
3. `## Spec` — the contract QA will hold the build to:
   - Final `name` (names are forever — say it like you mean it).
   - Component inventory with exact file paths.
   - Every skill/agent `description` written **verbatim** (it's the auto-invoke
     trigger; spec it like an API).
   - Hook plan with safety notes (events, matchers, failure behavior) — if any.
   - `### Acceptance checks` — numbered, concrete, runnable by a skeptic.
   - Token budget estimate vs. the QUALITY bar.

**building** (Builder; may span iterations)
4. `## Build log` — one dated line per iteration: component landed, decisions,
   deviations from spec (each deviation justified or the spec amended).

**rc** (QA)
5. `## Test log` — per charter/TESTING.md format, ending `TEST VERDICT: pass`.
   Bounces append here too and return stage to `building`.

**published** (Maintainer, after Reviewer sign-off)
6. `## Review log` — `REVIEW: approved|bounced — {notes}` entries with QUALITY axis
   scores. At publish, Maintainer appends the marketplace entry summary + version.

**deprecated** (Maintainer)
7. `## Deprecation` — reason, migration note for installed users, date removed from
   marketplace.json.

**shelved** (any role; ideas/specs declined before build)
8. `## Shelf note` — reason + **Revival trigger**: what observable change reopens it.

## Sync laws (validator-enforced)
- stage `building`+ ⇒ `plugins/<name>/.claude-plugin/plugin.json` exists, parses,
  `name` matches.
- stage `rc`+ ⇒ plugin has README.md + CHANGELOG.md; structural checks pass.
- stage `published` ⇔ listed in `.claude-plugin/marketplace.json` with
  `source: "./plugins/<name>"`; record.version = plugin.json version = semver;
  CHANGELOG's top entry mentions that version.
- stage `deprecated`/`shelved` ⇒ **not** in marketplace.json.

## kind: feature — engagement records (charter/GROWTH.md)
Features ride the same stages with three differences:
- No `plugins/<name>/` artifact or marketplace entry; the artifact is the change
  itself (site template via ADR + two-iteration rule, workflow, issue template,
  worker, docs). Sync laws for plugin artifacts don't apply.
- `## Experiment` is required from spec onward: Hypothesis, Metric, Baseline,
  Review-after.
- Post-publish, the growth role appends `## Verdict` (`VERDICT: keep|kill|extend`)
  when the review date passes; `kill` moves the record to `deprecated` and reverts
  the feature. `version` stays null for features.

## Optional front-matter keys (v5)
- `always_on_tokens` (int) + `verified` (date) — QA records the estimator's output
  (`python3 tools/tokencost.py <name>`) at each test pass; the window badges it as
  "est." because that's what it is.
- `prospected_by` (GitHub login) + `suggested_in` (issue #) — set by the Ideator
  when formalizing a community idea; renders as credit on the card and birth
  certificate, and the issue gets a thank-you comment linking both.
- `patron` (display name, opt-in only) — a commissioner who asked to be named.
- `commission` (issue #) — already in use; listed here for completeness.
