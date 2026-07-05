# CLAUDE.md — standing instructions for any Claude Code session in this repo

This repository is a self-running plugin workshop AND the marketplace it publishes to
(`.claude-plugin/marketplace.json`). Its protocol is `LOOP.md`; its laws are in
`charter/`. However you arrived — `loop.sh`, `/loop`, or interactively — these bind you:

## Map
- `LOOP.md` — the iteration protocol (the engine)
- `charter/` — VISION · ROLES · QUALITY · TESTING · BRAND
- `state/` — STATE.json, BACKLOG.md, JOURNAL.md (append-only), DECISIONS.md (ADRs)
- `foundry/` — SCHEMA.md, categories.json, records/<name>.md (job travelers), INDEX.md (generated)
- `plugins/<name>/` — clean shippable artifacts ONLY (official layout; no process files)
- `.claude-plugin/marketplace.json` — the storefront; validator keeps it in sync
- `tools/` — validate.py + build.py (the gates) + smoke.sh (official CLI validate wrapper)
- `site/` — generated catalog (never edit by hand; template in tools/build.py)
- `reviews/` — audits and reviews (append-only)

## Non-negotiables (digest of LOOP.md)
1. One task, one commit, one journal entry; one plugin moves one stage max.
2. `python3 tools/validate.py && python3 tools/build.py` green before every commit;
   `bash tools/smoke.sh` too when plugins/ changed.
3. Docs before invention: uncertain about plugin schema? Check
   https://code.claude.com/docs/en/plugins-reference — never guess fields or events.
4. Version law: any change to a published plugin bumps semver + CHANGELOG in the same
   iteration, or installed users never receive it.
5. Published plugin names are immutable slugs. Hooks are guests: narrow matchers,
   fail gracefully, quoted "${CLAUDE_PLUGIN_ROOT}", executable scripts.
6. Nothing publishes without TEST VERDICT: pass + REVIEW: approved in its record.
7. Two-iteration ADR rule for LOOP.md, loop.sh, tools/. JOURNAL/DECISIONS/logs append-only.
8. `STOP` file at root: journal one line, exit. Stay inside this repo.

When in doubt: build one component well, log it on the traveler, and let the next
iteration continue.
