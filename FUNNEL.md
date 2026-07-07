# FUNNEL — Adoption Friction Audit

*Brief 09 (Funnel Friction Audit), adapted at operator direction from a SaaS
signup funnel to what this repo actually is: a **Claude Code plugin marketplace**.
The "funnel" here is **plugin adoption** — discover → add the marketplace → choose
→ install → first value → habit. Read-only pass; the only write is this file.*

There is no signup, no account, no OAuth, no billing wall. That is the funnel's
greatest asset (zero account friction) and its central weakness (zero owned
relationship — the marketplace never learns who installed anything). Every count
below is from the user's fingers: commands typed, cards scanned, decisions made.

This audit builds on `HIERARCHY.md` (the existing visual-hierarchy pass on the
site) rather than repeating it; where a claim traces to that report I cite its
finding id (F1–F9).

---

## The three funnels

| # | Funnel | Entry | Aha (first value) | Status |
|---|--------|-------|-------------------|--------|
| **A** | **Install a plugin** (the main one) | GitHub repo / living-window site | a plugin does its job in your session | live |
| **B** | **Verify your own plugin** (CI action → dated listing + badge) | README "Verify YOUR plugin" | green run earns a public listing | live, un-instrumented |
| **C** | **Commission the missing plugin** ($5.99 → issue → built on the line) | site request box | the queued issue ships | **dead end today** — `stripe_payment_link` is empty (`foundry/site-config.json:5`) |

Funnel A is where adoption happens; it gets the depth below. B and C are covered
in *Silent stalls*.

---

## 1 — Funnel map (Funnel A: install a plugin)

| Stage | Steps today (from the fingers) | Friction found | Proposed fix | Expected effect | Effort |
|-------|-------------------------------|----------------|--------------|-----------------|--------|
| **Entry / Discovery** | Land on repo README or the Pages site from some channel (stars, ticker embed, a verified-listing badge, word of mouth) | Value prop `.strap` ("A plugin marketplace for Claude Code — two commands to install anything") is the *quietest* text on the page at 12.5px dim, out-shouted by telemetry (F1); the masthead is a status bar wearing a storefront's clothes (F6) | Demote telemetry type, promote the value prop above the fold (HIERARCHY fix #1/#7) | More landers grasp "what is this" in the first second | S (≈3 CSS lines + markup) |
| **Add marketplace** | `/plugin marketplace add GhostlyGawd/plugin-foundry` — **1 command**, inside Claude Code | Assumes the visitor (a) already runs Claude Code and (b) knows plugins exist; the site never onboards a newcomer to that prerequisite | One line near the top: "New to Claude Code plugins? Here's the 30-second version" + link to Anthropic docs | Rescues the newcomer segment that silently bounces | S |
| **Choose** | Scan the shelf of **10** undifferentiated plugin cards (`marketplace.json`) and decide which to install | No "start here," no ranking, no bundle; card title barely wins its own card (F5); every card carries an identical ink-filled install block drawn ~35× so none reads as "the action" (F3) | Feature a "start here" pick (plugin-smith or night-clerk) + group the shelf by the existing categories (`foundry/categories.json`) | Cuts choice paralysis at the highest-drop step | M |
| **Install** | `/plugin install <name>@foundry` — **1 command** | On the plugin **detail** page the install command is 12px inline `<code>` in a footer link list, below the darkest surface on the site — a *demo* terminal (F4) | Render the install line as the loudest block at the top of the detail sheet (HIERARCHY fix #5) | The "yes" visitor stops hunting for how | S |
| **First value** | Invoke it: `/command`, or a hook fires on your next commit/PR/session | Some plugins self-activate (commit-craft guard hook, test-gap-nudge Stop hook) → instant passive value; others need the user to know the command | Each card/detail names the *first thing to run* ("try: `doctor my plugin`") | Shrinks time-to-aha to one line | S |
| **Habit / Return** | Hooks run in daily flow; user may watch the repo, subscribe to `feed.xml`, or revisit the window | **No owned channel** — no email, no in-client update nudge; re-engagement depends entirely on the user opting into GitHub watch/Atom | Lean into the followable surfaces already built (shipnote, ticker embed, badge) and make "watch for new plugins" a one-click CTA | Converts one-time installers into returners without owning PII | S–M |

**Removing a step beats improving one:** the install itself is already ~2 commands
and one decision — near the achievable floor. The reclaimable waste is *upstream*
(discovery comprehension) and *in the choice* (10 cards, no guide), not in the
install mechanics.

---

## 2 — The biggest leak

**The Choose stage — the shelf abandons everyone who doesn't already know what they
want.** The install path is genuinely short, but it only pays off for a visitor who
arrives with a specific plugin in mind. Everyone else meets ten near-identical cards
with no "start here," no ranking, and no grouping, while the page's loudest, only-moving
pixels advertise the machine's own telemetry instead of the shelf (F1, F2, F3). This is
early-funnel, so the loss compounds through every stage after it. The one tool built to
solve exactly this — **night-clerk**, "the foundry's front desk… ask what plugin helps
with a task and get real recommendations with exact install lines" — sits *behind* the
funnel it would fix: you must already be in a Claude Code session and have installed it,
a chicken-and-egg. The site's on-page equivalent (`renderClerk` task-search) exists but
is out-weighted by chrome (F1). Fixing this stage is mostly **subtraction** (quiet the
telemetry) plus one **promotion** (a guided "what do you need?" entry that surfaces a
single confident install) — cheap, and it lifts every downstream stage at once.

---

## 3 — Step-count budget (to first value)

| | Steps |
|---|---|
| **Today** | 1 discover → 1 comprehend the pitch → *(prereq: Claude Code installed)* → 1 `marketplace add` → 1 choose among 10 → 1 `install` → 1 invoke = **~6 acts, 2 of them commands** |
| **Achievable minimum** | 1 discover → 1 `marketplace add` → 1 `install <the guided pick>` → value from a self-activating hook = **~4 acts, 2 commands** |

The command count is already at the floor (the platform needs both `marketplace add`
and `install`). The budget is won by **collapsing the comprehension + choice steps**:
a guided pick means the visitor never manually shops the shelf, and a self-activating
first plugin means value arrives without a remembered command.

---

## 4 — Instrumentation gaps

Today the funnel is **almost entirely blind.** Nothing between "someone visited" and
"a plugin ran" is measured.

- **No pageview analytics at all.** `goatcounter_site` is empty (`foundry/site-config.json:7`),
  so visits, bounce, and which cards draw attention are all unknown — the wiring exists
  (OPERATIONS §6), it's just unset.
- **Install counts are unobservable by design.** Claude Code does not report marketplace
  installs back to the marketplace owner. The foundry *cannot* know per-plugin install
  volume from the client — this is a platform limit, not a config gap. Any "installs"
  metric must be proxied.
- **The commission funnel (C) can't convert** because `stripe_payment_link` is empty
  (`site-config.json:5`), so there is nothing to measure there yet.

**Events worth capturing (in rough priority):**
1. **Pageviews + top-cards** — set `goatcounter_site`; privacy-respecting, already supported. Without this, every fix above is a guess.
2. **Install-intent proxy** — a copy-to-clipboard handler on each install block that pings a GoatCounter event path (e.g. `/copy/plugin-smith`). The closest observable stand-in for an install.
3. **Repo traffic** — GitHub Insights clones/views + stars over time (free, already available; just isn't surfaced on the window).
4. **Verified-listing opens** (Funnel B) and **commission issues opened** (Funnel C) — count the issues by label; the plumbing (labels) already exists.
5. **Return signal** — `feed.xml` subscribers / repo watchers as the only honest "habit" proxy.

Rule of the house applies: no surface should claim a number it cannot honestly measure —
so until (1) is set, the funnel dashboard should read *unknown*, not *zero*.

---

*Report only — no code or config changed. Which fixes should I build? I'd start with
the two highest-leverage, cheapest ones: **set `goatcounter_site`** (so the rest stops
being guesswork) and **the guided "start here" pick on the shelf** (the biggest-leak
fix). Both are small. Say the word and I'll open them as backlog items on the normal
line — not implement them here, since the repo is under an operator STOP.*
