# IMPROVEMENTS — Product Improvement Discovery (2026-07-06, post-v8 slate)

Discovery-only audit. Every item cites repo evidence; nothing here is implemented.

## 1 · Product snapshot

Nightshift Foundry is a self-running Claude Code plugin workshop that is also the
marketplace it publishes to — the repo itself is the store (`.claude-plugin/marketplace.json`),
and a generated static "window" (`site/`) is the storefront. Users are Claude Code
developers who install plugins in two commands; spectators who watch an autonomous
loop design → build → QA → review → publish in public; and contributors who climb a
ladder from voting (`idea` issues) to spec PRs to paid commissions. The intended
journey: land on the window → read a card with an honest token-cost badge → paste
an install block → return via saga/streak/Monday shipnote → participate via
idea/question/bug/bounty issues. Trust is the differentiator: every number on every
surface must be substantiated by the repo (dark-pattern law, `charter/GROWTH.md`).
The core constraint today: the window has never been deployed (Gate A in
`ROADMAP.md` is unchecked; `state/METRICS.jsonl` has no real snapshots), so all 8
armed experiments are baseline-less and every conversion surface is unmeasured.
32 of 38 records are published; the machinery is far ahead of its audience.

## 2 · Opportunity map

| # | Item | Tag | Impact | Effort |
|---|------|-----|--------|--------|
| 1 | README install line is a placeholder | FIX | High | S |
| 2 | night-clerk's bundled catalog is stale (+ validator law) | FIX | High | S |
| 3 | Backlog hygiene: done/stale items still open | FIX | Med | S |
| 4 | "Solo dev" starter kit — cover the uncovered half of the shelf | IMPROVE | High | S |
| 5 | Social/OG meta on window + certificates | IMPROVE | Med | S |
| 6 | Copy-to-clipboard on install blocks and kits | IMPROVE | Med | S |
| 7 | pr-gated-publishes: file the trial verdict (it just ran) | IMPROVE | Med | S |
| 8 | Night-clerk learns kits (bundle recommendations) | NEW | Med | S |
| 9 | Polish pass: saga ellipsis + field-report cap link (filed nits) | FIX | Low | S |
| 10 | Executable-suite backfill for v5/v7 features (audit-003 #3) | IMPROVE | Med | M |
| 11 | Dark mode across all generated surfaces | IMPROVE | Med | M |
| 12 | CI-recorded demo transcripts (replace "authored example" labels) | IMPROVE | High | M |
| 13 | Go-live assist pack: GoatCounter wiring + operator dry-run check | IMPROVE | High | M |

## 3 · Top 5 quick wins (~a day each)

1. **README install line** (#1) — the front door fails as pasted.
2. **night-clerk snapshot refresh + validator law** (#2) — the front desk is
   recommending from yesterday's shelf; the law prevents recurrence forever.
3. **Solo dev kit** (#4) — cheapest lever on the one experiment already measuring
   installs-per-visitor.
4. **OG/social meta** (#5) — every future share of the window currently renders as
   a bare link.
5. **pr-gated-publishes verdict** (#7) — the trial ran itself as PR #9; the record
   just needs its honest verdict.

## 3b · Top 3 big bets

- **Go-live assist pack** (#13) — everything downstream (8 experiments, gauge,
  metrics, Gate A) is dark until Pages + secrets exist. The machine can't press
  the button but can wire GoatCounter (`OPERATIONS.md` §6, `tools/metrics.py`
  already nulls gracefully), pre-verify workflows, and hand the operator a
  15-minute checklist with a dry-run proof.
- **CI-recorded demo transcripts** (#12) — the certificates promise it explicitly;
  delivering converts an honesty apology into the shelf's best proof-of-function.
- **Dark mode** (#11) — a terminal-native audience gets a paper-only palette today.

## 4 · Full list

### 1 · README install line is a placeholder — FIX · UX/onboarding
- **Evidence:** `README.md:28` reads `/plugin marketplace add <this-repo-or-path>`
  while `foundry/site-config.json` has had `repo: GhostlyGawd/plugin-foundry` since
  go-live prep. This is the *same drift class* the i114 review bounced embed-badges
  for (record: `foundry/records/embed-badges.md`) — the README's badge/iframe
  snippets got fixed; the install line two sections above did not.
- **Proposal:** bake the real slug; extend the existing embed-badges QA check
  (`foundry/tests/embed-badges/badge.test.sh` check 3) to also fail on
  `<this-repo` when config is set.
- **Why:** it's the first command every visitor pastes; time-to-first-value is
  exactly this line. **Effort S · Impact H · Risk:** none.

### 2 · night-clerk's bundled catalog is stale — FIX · Helpfulness/synergy
- **Evidence:** `plugins/night-clerk/data/catalog.json` says `"snapshot":
  "2026-07-05"` and lists 7 plugins — no `test-gap-nudge` (published i106), none of
  the v8 features. The clerk's whole pitch is "real recommendations with exact
  install lines from a bundled catalog snapshot" (`.claude-plugin/marketplace.json`).
- **Proposal:** regenerate the snapshot (version law: bump to 0.1.1 + CHANGELOG +
  tag), and add a `tools/validate.py` rule: every published `kind: plugin` record
  must appear in night-clerk's snapshot — so any future publish goes red until the
  clerk learns it.
- **Why:** a front desk that doesn't know the newest shelf item quietly breaks the
  product's one law (nothing shown that the repo can't substantiate — in reverse).
  **Effort S · Impact H · Risk:** validator rule must exempt night-clerk itself
  gracefully during its own publish iteration.

### 3 · Backlog hygiene — FIX · Felt debt
- **Evidence:** `state/BACKLOG.md` still lists as open: "P2 Per-plugin detail
  pages on the catalog (ADR first)" — but 38 certificates already exist
  (`site/p/*.html`, built by `build_pages` in `tools/build.py`); "P2 Spec
  weekly-shipnote" and "P2 Spec shift-streak" — both *published* in the v8 slate.
  `state/STATE.json` carries twin keys `note` and `notes`.
- **Proposal:** one maintainer pass: check off the three done items with pointers,
  merge STATE's twin keys.
- **Why:** the backlog is the machine's memory; stale entries waste future
  iterations and erode trust in the queue. **Effort S · Impact M · Risk:** none.

### 4 · "Solo dev kit" — IMPROVE · Helpfulness/synergy
- **Evidence:** `foundry/kits.json` has 2 kits covering only plugin-smith,
  fork-a-foundry, commit-craft, pr-narrator. Four published plugins are in no kit:
  env-doctor, session-recap, night-clerk, test-gap-nudge — and those four *are* a
  coherent bundle (diagnose env → work with a test nudge → recap the session).
  The starter-kits experiment (review 2026-07-26) measures clones-per-unique —
  kit coverage is its direct input.
- **Proposal:** Maintainer curates a third kit ("solo dev kit": env-doctor +
  test-gap-nudge + session-recap; night-clerk optional). Renders instantly — kit
  plumbing and per-line copy-blocks shipped in v8.
- **Why:** conversion lever on existing, tested infrastructure; zero new code.
  **Effort S · Impact H · Risk:** kit bloat — keep 2–4 members per the spec.

### 5 · Social/OG meta — IMPROVE · Reach
- **Evidence:** `site/index.html` head has `meta name="description"` and the atom
  `rel="alternate"` link but zero `og:*`/`twitter:*` tags (grep: no matches);
  certificates (`PAGE_TEMPLATE` in `tools/build.py`) likewise.
- **Proposal:** build.py emits og:title/description/url per page from data it
  already computes (title, one_liner, pages_url); og:description for the index can
  carry the substantiated live line ("32 shipped · i135" — same source as
  `site/badge.json`).
- **Why:** embed-badges (published i118) bets on fans sharing; today every share
  unfurls as a bare URL. **Effort S · Impact M · Risk:** keep numbers derived at
  build time, same honesty law as the badge.

### 6 · Copy-to-clipboard — IMPROVE · Feedback & state
- **Evidence:** `.install{... user-select:all}` (`tools/build.py:313`) is the only
  copy affordance; no `navigator.clipboard` anywhere in `site/index.html`. Kits'
  multi-line blocks (fixed at i90) still require manual select-copy.
- **Proposal:** one small JS handler + "copied ✓" flash on `.install` blocks and
  kit blocks; keep `user-select:all` as the no-JS fallback.
- **Why:** the product's core conversion is literally copying a command; this is
  the last inch of that funnel. **Effort S · Impact M · Risk:** clipboard API
  needs a secure context — fine on Pages; degrade silently on file://.

### 7 · pr-gated-publishes verdict — IMPROVE · Process/trust
- **Evidence:** `foundry/records/pr-gated-publishes.md` is `stage: spec`, and
  BACKLOG carries "P1 (growth) Run the pr-gated-publishes trial." PR #9 *was* the
  trial: 48 publish-bearing commits gated behind an operator merge, veto window
  honored, merged 2026-07-06 (`reviews/audit-003.md`).
- **Proposal:** growth iteration writes the trial outcome into the record and
  rules on the scheduled default (gate scheduled shift publishes behind PRs or
  not), checking the P1 off.
- **Why:** the experiment already produced its data; leaving the record at spec
  wastes a finished result. **Effort S · Impact M · Risk:** none.

### 8 · Night-clerk learns kits — NEW · Synergy
- **Evidence:** `plugins/night-clerk/skills/clerk/SKILL.md` recommends per-plugin
  from `data/catalog.json`; kits exist only on the window (`foundry/kits.json`).
  Both are Maintainer-curated JSON; the snapshot regeneration in item #2 can carry
  kits along for free.
- **Proposal:** include kits in the clerk's snapshot; when a task maps to a
  bundle ("set up a new repo workflow"), the clerk offers the kit's paste-block.
- **Why:** the two features multiply: discovery (clerk) × curation (kits) with no
  new data source. **Effort S · Impact M · Risk:** rides item #2's version bump —
  same release.

### 9 · Polish pass — FIX · UI (filed nits)
- **Evidence:** BACKLOG P3s from the v8 reviews: saga wall truncates quotes
  mid-word with no ellipsis (i107, `build_saga` 220-char slice); field-report
  certificates cap at 8 with no "all N →" link (i125, `[:8]` in `tools/build.py`).
- **Proposal:** one designer iteration for both.
- **Why:** small, but both sit on trust surfaces. **Effort S · Impact L · Risk:** none.

### 10 · Executable-suite backfill — IMPROVE · Felt debt
- **Evidence:** `reviews/audit-003.md` finding #3; `tools/qa.sh` declares suites
  "required at rc+" yet v5/v7-published features (saga-page, field-reports,
  community-hall, fuel-gauge, shift-streak, scannable-window, …) have no
  `foundry/tests/<name>/` dirs. The v8 slate proved the value: its 6 new suites
  caught/pinned 5 real defects.
- **Proposal:** the P2 already filed — one suite per QA pass, oldest first.
- **Why:** the gap is exactly where the next silent regression will live.
  **Effort M (spread) · Impact M · Risk:** none.

### 11 · Dark mode — IMPROVE · UI & beauty
- **Evidence:** zero `prefers-color-scheme` in `tools/build.py` (the single
  source of all page CSS); the palette is hardcoded light paper
  (`--paper:#E9DFC8...` at :root, duplicated in saga/embed/theater templates).
  Reduced-motion IS handled (two `@media` blocks) — the a11y instinct exists;
  color didn't follow.
- **Proposal:** define the palette once as CSS custom properties with a
  `prefers-color-scheme: dark` override block; template change → needs a
  prior-iteration ADR per LOOP.md rule 4.
- **Why:** the audience lives in terminals and dark IDEs; first impressions of a
  glaring paper page cost return visits. **Effort M · Impact M · Risk:** brand v1
  is "warm paper" (ADR-011 lineage) — the dark variant must be designed, not
  inverted; Designer role owns it.

### 12 · CI-recorded demo transcripts — IMPROVE · Trust/engagement
- **Evidence:** every certificate with an example renders "authored example — a
  CI-recorded transcript replaces this per charter/TESTING.md"
  (`sec()` in `tools/build.py` ~line 818); no recording pipeline exists in
  `.github/workflows/` (only shift, shipnote, re-verify). The label is a standing
  promissory note.
- **Proposal:** a workflow step that runs each published plugin's skill headlessly
  (`claude -p` in CI) against a fixture repo, captures the transcript, and swaps
  the label to a dated "recorded YYYY-MM-DD" — mirroring how `releases-and-reverify`
  already stamps `verified:`.
- **Why:** turns the shelf's biggest apology into its best proof; nobody else
  shows real recorded plugin sessions. **Effort M · Impact H · Risk:** CI token
  cost per run — record on publish + monthly, not weekly; budget governor applies.

### 13 · Go-live assist pack — IMPROVE · Everything-gated-on-it
- **Evidence:** ROADMAP Gate A unchecked; `state/METRICS.jsonl` empty of real
  snapshots; `foundry/site-config.json` has `goatcounter_site: ""` and
  `monthly_budget_usd: null` (fuel gauge permanently in arming state,
  `renderFuel` branch at `tools/build.py:612`); 8 experiments in BACKLOG await
  baselines.
- **Proposal:** machine-side: pre-flight script that validates workflows, secrets
  presence (names only), Pages config, and GoatCounter wiring end-to-end in dry
  run; operator-side: the 15-minute checklist distilled from OPERATIONS §1–6 with
  the exact clicks. Then the operator does the one thing only they can.
- **Why:** every metric-driven feature shipped in v5–v8 is a stopped clock until
  this happens. **Effort M · Impact H · Risk:** none beyond API spend starting.

## 5 · Sequence — if only 3 ship first

1. **#1 README install line** — the single highest-traffic string in the product
   is broken as pasted; fix + regression in an hour.
2. **#2/#8 night-clerk refresh + kits (one release)** — un-stales the flagship
   recommender, adds the validator law so it can never drift again, and lands the
   kit synergy in the same version bump.
3. **#4 Solo dev kit** — with the funnel honest (1) and the clerk current (2),
   this is the highest-leverage conversion input before the first real visitors
   arrive at go-live.

All three are conversion-path items deliberately sequenced *ahead* of the
operator's go-live so the first measured visitor hits a working funnel — and the
starter-kits/token-cost-badges experiments (reviews 2026-07-19/26) get clean
baselines instead of measuring a broken front door.
