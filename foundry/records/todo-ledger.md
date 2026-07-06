---
name: todo-ledger
title: TODO Ledger
category: quality
stage: idea
version: null
kind: plugin
components: [skills]
one_liner: Inventories TODO/FIXME/HACK comments with git-blame age and owners — tech debt as a dated, ranked ledger.
tags: [tech-debt, todos, reporting]
created: 2026-07-06
updated: 2026-07-06
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
