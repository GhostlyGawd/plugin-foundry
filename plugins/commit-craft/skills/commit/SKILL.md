---
name: commit
description: Write a conventional commit message for staged changes and commit them. Use when the user says commit this, write a commit message, clean up my commit, or finishes a change that should land in git.
---

# Craft the commit

1. Read what's actually staged: `git diff --cached --stat` then `git diff --cached`
   (unstaged-only? ask before `git add`; never add secrets, .env, or build junk).
2. Choose the one true type: `feat | fix | docs | refactor | test | chore | perf`
   — **unless `COMMIT_CRAFT_TYPES` is set in the environment, in which case use
   exactly that list** (pipe/comma/space-separated). The guard hook enforces the
   same variable, so the type you write and the type it allows must be the same
   set; check it before choosing. Scope in parens when the repo has clear areas,
   e.g. `feat(parser):`.
3. Subject ≤ 72 chars, imperative mood, no trailing period. Body (when the diff
   needs one): the *why*, wrapped at 72; `BREAKING CHANGE:` footer when true.
4. Show the message, then run `git commit -m "<subject>" [-m "<body>"]`.
5. If the guard hook blocks you, it prints the reason on stderr — fix the message,
   don't fight the hook.

One logical change per commit. If the diff is two ideas, offer to split.
