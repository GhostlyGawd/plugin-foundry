---
name: pr
description: Draft a pull-request title and description from this branch's actual commits and diff. Use when opening a PR, or the user says write the PR, describe this branch, or draft a pull request.
---

# Narrate the pull request

1. Evidence first — never memory:
   - detect base: `main` if it exists, else `master`, else ask
   - `git log --oneline <base>..HEAD` and `git diff --stat <base>...HEAD`
2. Title: conventional form from the dominant change (`feat(scope): ...`), ≤72 chars.
3. Body, exactly these sections:
   - **Summary** — the why, 2–4 lines a reviewer reads first
   - **Changes** — grouped bullets built from the real commit list
   - **Test notes** — only what was actually run; **"none" is a valid and honest
     answer** — never claim untested coverage
   - **Risk & rollback** — blast radius in one line + how to revert
4. Show the draft. If `gh` is installed, offer:
   `gh pr create --title "..." --body-file <tmp>` — show the exact command and run
   it only after the user says yes. Never push, never force-anything, never open
   the PR unasked.
