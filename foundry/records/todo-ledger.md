---
name: todo-ledger
title: TODO Ledger
category: quality
stage: published
version: 0.1.0
always_on_tokens: 108
kind: plugin
verified: 2026-07-13
components: [skills]
one_liner: Inventories TODO/FIXME/HACK comments with git-blame age and owners — tech debt as a dated, ranked ledger.
tags: [tech-debt, todos, reporting]
created: 2026-07-06
updated: 2026-07-07
---

# TODO Ledger

Every repo carries a sediment of TODO, FIXME, and HACK comments. Nobody reads them
because they're scattered and undated; the five-year-old FIXME looks identical to
Friday's. The information to rank them — age, author, file churn — is already in git.

## Pitch
- **Job:** produce a ledger of debt comments (TODO/FIXME/HACK/XXX) ranked by age
  (git blame) and grouped by area, with a short "worst offenders" summary and
  copyable file:line references.
- **User:** tech leads before planning; new maintainers inheriting a codebase;
  anyone who suspects the TODOs are load-bearing.
- **Components:** one skill (`skills/ledger/`). Greps for the markers, blames each
  hit for date and author, ranks oldest-first, and writes the report to stdout or a
  dated markdown file on request. Read-only by default — it never deletes or edits
  a comment unasked.
- **Why a plugin:** the grep+blame+rank recipe is mechanical and identical across
  repos, but tedious enough that nobody does it by hand twice. One job, no always-on
  cost, obviously shareable.

## Spec
- Name: `todo-ledger` (forever). One skill, `ledger`, description (verbatim):
  "Inventory a repo's TODO/FIXME/HACK/XXX comments into a ranked, dated ledger
  with git-blame age and author. Use when the user says list the TODOs, audit the
  tech debt, what FIXMEs are in here, or before planning a cleanup."
- Behavior: find markers with `git grep -nE '\b(TODO|FIXME|HACK|XXX)\b'` (tracked
  files only; recursive grep fallback outside git, with age/author declared
  unavailable); blame each `file:line` for author + author-time; age in whole
  days, with "uncommitted"/"unknown" for unblameable lines — never a guessed
  date; rank oldest-first, group by top-level dir, FIXME/HACK above TODO on ties;
  report a summary line + worst-offenders top 5 + the grouped ledger with copyable
  `file:line` refs; write a dated `TODO-LEDGER-<date>.md` only on request.
  Read-only otherwise — never edits or deletes a marker.
### Acceptance checks
1. Markers found via git grep on tracked files; non-git repo degrades gracefully
   (lists markers, says age/author unavailable).
2. Each hit carries git-blame age + author, or an honest "unknown"/"uncommitted"
   — never a guessed date.
3. Ranking is oldest-first with a worst-offenders summary; references are copyable
   `file:line`.
4. Never writes or edits unasked; the dated report file is opt-in.

## Build log
- v14 (builder, ADR-024): scaffolded to the official layout (plugin.json, `ledger`
  skill, README with recipes + honest disclosures, CHANGELOG 0.1.0), plus the
  executable suite. One skill, no hooks, no network — the tenth plugin and the
  first exhibit of July's "Repo hygiene" theme.

## Test log
### Test pass — v14 (qa)
- tier 1: structure suite 9/9 (manifest, invoke contract, git-grep + non-git
  fallback, blame + honest-unknown, oldest-first + worst-offenders + copyable,
  read-only + opt-in write, docs present, skills-only, official validate).
- tier 2: always-on cost 108 tok (est., tokencost) — under the 300 budget; one
  skill description, no hooks.
- tier 3: acceptance checks 1–4 traced through the skill text; probed the
  dating-honesty clause (unblameable → "unknown", never invented) and the
  read-only default (dated file is opt-in, never unasked).
- defects: none found.
TEST VERDICT: pass

## Review log
### Review — v14 (reviewer)
- Scope discipline (5): one job — inventory debt comments — done whole; no
  always-on hook, no mutation, no scope creep into "fixing" TODOs.
- Prompt craft (5): the description carries concrete trigger phrases ("list the
  TODOs", "audit the tech debt", "what FIXMEs are in here") — it fires when it
  should; the body names inputs (git grep/blame), outputs (summary + worst
  offenders + grouped ledger), and edge behavior (non-git, unblameable lines).
- Docs truth (5): README recipes and disclosures match the skill; the
  never-invent-a-date and read-only clauses are load-bearing and stated plainly.
- Structure (5): official layout, kebab-case name, semver, CHANGELOG top entry
  matches; validator + official --strict green.
- Sharpest question: could it fabricate an age with no git history? No — the spec
  routes unblameable lines to "unknown"/"uncommitted" and the suite pins it.
REVIEW: approved

## Publish log
- v14 (maintainer): marketplace entry (source ./plugins/todo-ledger), version
  0.1.0 synced across plugin.json + record + CHANGELOG, night-clerk catalog
  regenerated (tenth plugin joins the snapshot). Tag todo-ledger-v0.1.0 to be
  cut via release dispatch post-merge (ADR-020 path). Experiment: none — utility
  plugin; install proxy rides the shelf-wide metric.
