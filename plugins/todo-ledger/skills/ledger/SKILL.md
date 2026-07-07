---
name: ledger
description: Inventory a repo's TODO/FIXME/HACK/XXX comments into a ranked, dated ledger with git-blame age and author. Use when the user says list the TODOs, audit the tech debt, what FIXMEs are in here, or before planning a cleanup.
---

# Build the debt ledger

1. **Find the markers.** Search the tracked tree for debt comments — `TODO`,
   `FIXME`, `HACK`, `XXX` (word-boundary; case-sensitive by convention, offer
   case-insensitive if asked). Prefer `git grep` so only tracked files count and
   paths stay clean:
   `git grep -nE '\b(TODO|FIXME|HACK|XXX)\b'`
   If this isn't a git repo, fall back to a recursive `grep -rnE` and say plainly
   that age and author will be unavailable.
2. **Date and attribute each hit — never guess.** For every `file:line`, blame it:
   `git blame -L <line>,<line> --porcelain -- <file>` and read `author` and
   `author-time`. Age = today − author-time, in whole days. A line that can't be
   blamed (uncommitted change, or no git) is listed with age **"uncommitted"** or
   **"unknown"** — an unknowable date is named as such, never invented.
3. **Rank and group.** Sort **oldest first** — the load-bearing debt surfaces at
   the top. Group by top-level directory so areas are legible. When ages tie, put
   `FIXME`/`HACK` above `TODO` (they're louder).
4. **Report.** Lead with one summary line (N markers across M files, oldest K
   days) and a **worst-offenders** top 5 (oldest, each with `@author` and
   `file:line`). Then the grouped ledger, one hit per line:
   `file:line · TYPE · <age>d · @author · <comment text>`
   Every reference is copyable so the reader can jump straight to it.
5. **Write only on request.** If asked to save it, append/write a dated file
   `TODO-LEDGER-<YYYY-MM-DD>.md` — never unasked. Otherwise this is **read-only**:
   it never edits, deletes, or "fixes" a marker. Diagnosis, not surgery.
