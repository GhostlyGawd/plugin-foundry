# REVENUE — Monetization Map

*Brief 11 (Monetization Map), adapted. This is not a SaaS with features to paywall —
the plugins are free, and `COMPETITIVE.md` shows **every** rival is free, so gating the
shelf would be competitive suicide and off-brand. The honest question here is
**sustainability**: how does a free, autonomous plugin line fund its own operation?
Revenue = **labor-on-demand (commissions)** + **goodwill (patronage)**, never access.
Read-only pass; the only write is this file.*

---

## 1 — Current model snapshot

**What exists (built, in the repo):**
- A **commission path, end-to-end**: a Stripe Payment Link (default **$5.99**) → Cloudflare
  Worker verifies the webhook → opens a `commission`-labeled issue → `tools/intake.py` queues
  it → **LOOP.md priority 3** builds it on the normal line at the normal bar
  (`services/commission-worker/README.md`, README §"living window").
- A **honest promise** baked into the copy: *"priority + a serious attempt at the full quality
  bar — never guaranteed delivery"* (`services/commission-worker/README.md:18-21`).
- A **commission-tiers experiment** at spec: standard / rush (~3×) / sponsor (~5×, named credit),
  worker maps link→label, intake orders rush-first (`foundry/records/commission-tiers.md`).
- A **fuel gauge + Sponsor path**: month-to-date spend vs a cap, GitHub Sponsors button, patron
  recognition (README v5 "Sustainable", `OPERATIONS.md §8`, `foundry/records/fuel-gauge.md`).
- A **budget governor**: `LOOP_MONTHLY_BUDGET_USD` self-skips shifts over the monthly ledger
  (`state/BUDGET.jsonl`) — this is **cost control, not revenue** (`OPERATIONS.md §7`).

**What's enforced:** only the *spend* ceiling (the governor). Nothing on the revenue side is live.

**What leaks — and it's the whole headline:**
> **The till is closed.** `stripe_payment_link` is empty (`foundry/site-config.json:5`), so the
> fully-built commission machine has **no way to take a payment** — 100% of commission demand
> leaks. The request box degrades to a dead end (this is also `FUNNEL.md`'s Funnel C finding).

Secondary leaks:
- **No sponsor button wired** — `.github/FUNDING.yml` ships commented (`OPERATIONS.md §8`), so the
  goodwill path is off too.
- **The fuel gauge has no denominator** — `monthly_budget_usd` is `null` (`site-config.json:8`),
  so the "help fuel the shift" ask shows no target to fill.
- **What's expensive to serve is unoffset:** the real cost is **Claude-subscription usage per
  shift** (the `BUDGET.jsonl` ledger). Today commissions/sponsors offset *none* of it because
  both paths are unwired. The cost is *gated* (governor) but not *funded*.

**Willingness-to-pay signals already present in the product:** the **empty-state search** ("no
plugin does X" — the missing-plugin need), the **idea-inbox** pitch, and the **moment a
commission ships** (peak satisfaction). Each is a natural, honest place value is felt.

---

## 2 — Packaging proposal

Reframed as **funding tiers, not access tiers.** Each names its one-line job. The generous free
story is the same for all: *the entire shelf is free forever; paying only buys priority,
recognition, or fuel — never the plugins.*

| Tier | One-line job | Price | Status |
|---|---|---|---|
| **Free (always)** | Install any published plugin, browse the catalog, run the verify action | $0 | live — this is the brand and a table stake |
| **Commission · Standard** | "Request a specific plugin: a priority slot + a serious full-bar attempt" | **$5.99** | built, **not wired** |
| **Commission · Rush** | "Front of the commission lane" (speed, not a guarantee) | ~3× (~$18) | spec'd (`commission-tiers.md`) |
| **Commission · Sponsor** | "Rush + your name on the shipped card & shipnote" | ~5× (~$30) | spec'd, opt-in credit |
| **Patron (recurring)** | "Keep the night shift running — fuel the gauge, take a seat in the patron hall" | GitHub Sponsors | path exists, **not wired** |

**Explicitly keep free (a deliberate non-gate):** the **`foundry-doctor` verify action + badge**.
`COMPETITIVE.md` Bet 3 makes it a *distribution flywheel*; charging for a trust badge would poison
exactly the trust it exists to signal. Monetize the labor, never the credibility.

---

## 3 — Upgrade-moment placements

Where an honest, well-placed prompt meets a real high-WTP moment (with the trigger):

| Moment | Where (UI / code) | Trigger | Ask |
|---|---|---|---|
| **Missing plugin** (the strongest) | site `#empty` search state (today dim — `HIERARCHY.md`) | search returns no match | "No plugin does this yet — **commission it** (from $5.99, priority + a serious attempt)" |
| **Pitching an idea** | idea-inbox issue / `/backlog` | user opens an idea | "Want it sooner? A commission jumps the queue." |
| **A commission ships** | issue close comment + shipped card | commission delivered | "Glad it helped — **sponsor** to keep the shifts coming (credit included)." |
| **Fuel low / window amber** | fuel gauge, `ops-alarm` | month-to-date spend nears cap | "The shift is low on fuel — **sponsor a shift**." |
| **Following the work** | weekly shipnote / `feed.xml` | subscriber opens a shipnote | soft patron ask + patron-hall credit |

The **empty-state → commission** placement is the highest-value: the user has hit the one real
"limit" (the plugin doesn't exist) at the exact instant WTP peaks. It already has a home in the
markup; it's just styled to disappear.

---

## 4 — Friction fixes (checkout & pricing, ranked)

1. **Wire the Stripe link.** Paste the Payment Link into `site-config.json:stripe_payment_link`
   (needs the operator's Stripe account). *Nothing else in this report matters until this is done* —
   it is the difference between a storefront and a display case. **(Operator action.)**
2. **State honest terms at the point of sale.** The "priority + serious attempt, not guaranteed
   delivery" line + a **refund policy** must render on the payment link *and* the request box
   (`commission-worker/README.md`). This is the trust signal that makes charging for
   AI-generated-on-demand work defensible (see the risk note below). **(Config + copy.)**
3. **Resolve the two-primaries collision.** `HIERARCHY.md` F3: the commission `.cta` competes with
   ink-filled install blocks in the same row. Make the commission CTA the **single** filled primary
   in the duo, and **promote the dim `#empty` recovery link**. **(≈2 CSS lines.)**
4. **Wire goodwill + a target.** Uncomment `.github/FUNDING.yml` and set `monthly_budget_usd` so the
   fuel gauge shows a cap bar to fill (`OPERATIONS.md §8`). **(Config.)**
5. **Instrument it** (from `FUNNEL.md §4`): count `commission`-labeled issues opened→shipped and,
   once GoatCounter is set, request-box clicks — otherwise conversion is unmeasurable.

---

## 5 — Quick wins vs structural changes

**Quick wins (config + a few CSS lines, no new architecture):**
- Paste the Stripe link (fix #1) — unlocks 100% of the currently-leaking commission demand.
- Uncomment FUNDING.yml + set the budget denominator (fix #4).
- Promote the empty-state commission CTA and de-collide the duo (fix #3).
- Put honest terms + refund policy on the box (fix #2).

**Structural (real build, governed as experiments):**
- **Commission tiers** (rush/sponsor): 2 more Stripe links + worker label mapping + intake ordering —
  already spec'd with a **45-day, ≥2× revenue** hypothesis (`commission-tiers.md`). Ship *after* the
  single-tier baseline exists, or the experiment has nothing to measure against.
- **Patron recognition** (hall of patrons, named credit rendering) — renders nothing until a first
  real patron exists (the repo's own "no fake data" law).

---

## The risk this report must name

Charging **per plugin, generated on demand**, is genuinely novel — `COMPETITIVE.md` found *no one*
in the Claude Code space sells per-plugin (creators use sponsors / Buy-Me-a-Coffee; Smithery pays
creators $0). Novelty cuts both ways: it's a real differentiator **and** it imports quality,
liability, and refund expectations the loop must be able to honor. The mitigation is already
designed and must never be watered down: **priority + a serious attempt, explicitly not a guaranteed
delivery, with a stated refund policy** — sold on that honesty, not on a promise the machine can't
keep. Monetize value *delivered* (prioritized labor, recognition, fuel), never a hostage feature.

---

*Report only — nothing wired, no config changed (and the operator STOP is still in force). Which
moves? The honest sequence: **the operator wires Stripe + Sponsors (fixes #1, #4)** — I can't do
that part — then I open **fixes #2, #3, #5** as backlog items on the normal line, and the
commission-tiers experiment stays parked until a single-tier baseline exists. Tell me which to
queue.*
