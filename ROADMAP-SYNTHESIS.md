# ROADMAP-SYNTHESIS — one sequenced plan from every root audit

*Brief 28 (Roadmap Synthesis), written to a new file at the operator's direction so the
hand-maintained governance `ROADMAP.md` (Gates A/B/C, Auditor-owned checkboxes) is
preserved. This is **synthesis, not re-auditing**: every item below traces to a source
report; nothing new is smuggled in. Where reports disagree on priority, it's called out
and ruled with reasoning.*

---

## 1 — Sources

**Audit family found at repo root (7 reports + 1 governance doc):**

| Report | What it covers | State of its findings |
|---|---|---|
| `FUNNEL.md` | Plugin-adoption funnel (discover→install→habit) | **open** (report-only) |
| `COMPETITIVE.md` | Rivals, table stakes, differentiation bets | **open** |
| `REVENUE.md` | Commission + patronage monetization | **open** |
| `AI-IDEAS.md` | Where new AI earns its place | **open** |
| `HIERARCHY.md` | Visual hierarchy of the window | **open** (no styles changed) |
| `IMPROVEMENTS.md` | Product-improvement slates v10–v13 | **mostly BUILT** (i153–i215); a few open items + big bets remain |
| `SECURITY.md` | Security **policy** (not a findings audit) | shipped policy; contributes one integrity gap |
| `ROADMAP.md` *(governance)* | Phase gates A/B/C, ownership | context for dependencies, **not** a findings source |

**Reports missing — and which would most change this plan:**
- **A Security / supply-chain audit** *(most valuable absent audit)* — `SECURITY.md` is a
  policy, not findings. No report systematically covers **install-time integrity** (SHA
  pinning of plugins and of GitHub Actions), yet these plugins execute on users' machines
  and `COMPETITIVE.md` flags SHA-pinning as the one table stake we lack. **Run this next.**
- **No `BUGS.md`** — bugs live ad hoc in `state/BACKLOG.md § Bugs` (the one live bug,
  `build.py` fresh-checkout crash, was already fixed in v14). A consolidated bug audit is absent but low-value at current scale.
- **No `PERF.md`** — `IMPROVEMENTS.md` notes a `build.py` re-parse drag; a perf audit is
  absent and correctly low-urgency while builds are sub-second and traffic is zero.
- **No traffic/analytics readout** — impossible today (see Theme 2); it becomes the most
  important "audit" the moment GoatCounter is set.

---

## 2 — Unified backlog (deduplicated)

Impact/effort recalibrated onto one scale across all reports. **Dep** = what must land first.
Every item cites its source report(s).

| ID | Item | Sources | Impact | Effort | Dep |
|---|---|---|:--:|:--:|---|
| **OW1** | **Regenerate the OAuth token, delete `STOP`** → un-halt the loop | `ROADMAP` Gate A · `STOP` (repo state) | **H** | S *(operator)* | — (root) |
| **OW2** | Set `goatcounter_site` → funnel becomes measurable | `FUNNEL §4` | H | S *(operator)* | — |
| **OW3** | Wire the Stripe payment link → open the till | `REVENUE §1/§4` · `FUNNEL` (Funnel C) | H | S *(operator)* | — |
| **OW4** | Uncomment Sponsors + set `monthly_budget_usd` | `REVENUE §4` · `OPERATIONS §8` | M | S *(operator)* | — |
| **SW1** | Demote telemetry type + kill chrome motion (4 lines) | `HIERARCHY` F1/F2 (#1/#2) · `FUNNEL` · `IMPROVEMENTS` v13 | **H** | S | OW1 |
| **SW2** | Guided "start here" pick + group shelf by category | `FUNNEL §2` (biggest leak) · `IMPROVEMENTS` v10#3 | **H** | M | OW1 |
| **SW3** | Install command + "tested·reviewed" trust card as the loudest detail elements | `HIERARCHY` F4 (#5) · `COMPETITIVE` Bet 1 · `FUNNEL` | **H** | S–M | OW1 |
| **SW4** | One primary in the duo: commission CTA wins; promote dim empty-state | `REVENUE §4` · `HIERARCHY` F3 | M | S | OW1 (+OW3 to convert) |
| **SW5** | Build-time semantic shelf search (aliases → static picker) | `AI-IDEAS` Idea 1/§5 · `FUNNEL` | M–H | M | OW1 |
| **DR1** | Get listed where users actually look (awesome-claude-code issue-form, Anthropic community marketplace, aggregators) | `IMPROVEMENTS` v13 big-bet · `COMPETITIVE §1/§4` · `FUNNEL` Entry | **H** | M | SW1–SW3 (soft) |
| **DR2** | Verified-by-foundry as a trust flywheel (promote the CI action + badges) | `COMPETITIVE` Bet 3 · `IMPROVEMENTS` v10#13 | **H** | M | partly built |
| **DR3** | Freshness positioning — tie telemetry to plugin freshness | `COMPETITIVE` Bet 2 | M | S–M | SW1 |
| **RV1** | Honest terms + refund policy at the point of sale | `REVENUE §4` · `commission-worker` | M | S | OW3 |
| **RV2** | Commission-tiers experiment (rush / sponsor) | `REVENUE §5` · `records/commission-tiers.md` | M | M | OW3 + single-tier baseline |
| **RV3** | Intake triage — dedupe/categorize incoming ideas & commissions | `AI-IDEAS` Idea 2 | M | M | commissions arriving (OW3+DR1) |
| **IN1** | SHA-pin plugins (install-time integrity) | `COMPETITIVE` stake #6 · `SECURITY.md` | M | M | — |
| **IN2** | SHA-pin GitHub Actions (supply-chain) | `IMPROVEMENTS` "noted" | L–M | S | — |
| **L1** | Foundry Network federation | `IMPROVEMENTS` v10#14 · `records/foundry-network.md` | H | L | sister foundries (world) |
| **L2** | Operator digest with anomaly flags | `AI-IDEAS` Idea 3 | M | M | OW2 (data) |
| **H1** | `build.py` re-parse perf | `IMPROVEMENTS` "noted" | L | S | — |

---

## 3 — Themes (one root cause under many findings)

**Theme 1 — The storefront serves the machine, not the shopper.** *(HIERARCHY F1–F6 · FUNNEL
biggest-leak · REVENUE two-primaries · IMPROVEMENTS v13 "10:1 tilt")* Five reports independently
hit the same root: size, contrast, motion, and *engineering investment* are spent on telemetry
and the window while the two things a visitor does — **find a plugin, install/commission it** —
are the quietest, most-buried, least-invested surfaces. One structural rule (`HIERARCHY §4`:
emphasis reserved for find+install; and reverse the plugins-vs-site investment tilt) dissolves the
whole cluster. → **SW1–SW4.**

**Theme 2 — Everything is unwired, so everything is unmeasured, frozen, and unpaid.** *(FUNNEL §4 ·
REVENUE closed-till · ROADMAP Gate A · IMPROVEMENTS "audience zero" · D14 dormant experiments)* The
funnel has no analytics, the till has no Stripe link, the fuel gauge has no denominator, and every
growth experiment is frozen behind Gate A — and **right now the loop itself is halted** because the
OAuth token is rejected (the `STOP`). This is not five problems; it is **one operator go-live
bundle** sitting on the critical path of almost everything else. → **OW1–OW4.**

**Theme 3 — The plugins are invisible where Claude Code users look.** *(IMPROVEMENTS v13 "Reach"
big-bet · COMPETITIVE §1/§4 · FUNNEL Entry)* Discovery — not distribution rights — is the whole
battleground, and the foundry has no presence in the lists/marketplaces/aggregators where buyers
actually browse. Distribution is the growth lever the window (built for zero visitors) cannot pull.
→ **DR1–DR2.**

**Theme 4 — The real moat is under-surfaced.** *(COMPETITIVE Bet 1/Bet 3 · HIERARCHY F4 ·
IMPROVEMENTS verified-by-foundry)* The foundry's genuine, near-unique advantages — a *tested +
reviewed* gate, provenance, token-cost honesty, a portable verification badge — are exactly what
rivals lack, yet they're buried. Surfacing them is cheap and compounding. → **SW3, DR2.**

**Theme 5 — It runs on strangers' machines, but integrity is unpinned.** *(COMPETITIVE stake #6 ·
IMPROVEMENTS Actions-pin · SECURITY.md)* Plugins and workflows execute untrusted-adjacent code; SHA
pinning (plugins + Actions) is the one under-examined risk. → **IN1–IN2** (and the missing
security audit in §1).

---

## 4 — Three milestones

### NOW (1–2 weeks) — "Unblock, then stop flying blind"
**OW1 → OW2/OW3/OW4, then SW1, SW3, SW4, SW2, SW5.**
The literal top of the critical path is not a feature — it's **OW1**: until the operator regenerates
the OAuth token and deletes `STOP`, the loop that builds everything else cannot run. Do OW2/OW3/OW4
in the *same operator sitting*, because every downstream measurement and the entire till depend on
that wiring. Then spend the loop's first cheap iterations on the highest-leverage conversion fixes
that need **no traffic**: SW1 (four lines, biggest reclaim), SW3/SW4 (make install + the trust card
+ the commission CTA the loud things), SW2 (the guided pick that fixes the biggest funnel leak), and
SW5 (semantic search). *Story: instruments before measurements; unblock the machine before you ask
it to build; fix conversion while it's free.*

### NEXT (a month) — "Get seen, get trusted, get paid"
**DR1, DR2, DR3 ‖ RV1, RV2, RV3.**
With the shelf honest and conversion fixed, aim net-new energy at **distribution** — the growth lever
the window can't provide: DR1 (list where users look), DR2 (verified-by-foundry flywheel), DR3
(freshness positioning). *In parallel*, once Stripe is live (OW3) and a single-tier baseline exists,
turn on revenue depth: RV1 (honest terms), RV2 (the spec'd tiers experiment), RV3 (intake triage,
which compounds as commissions arrive). *Story: traffic and trust must precede monetization — you
cannot A/B a funnel with no visitors, and tiers need a baseline to beat.*

### LATER — "Moats and integrity"
**IN1, IN2, L1, L2, H1.**
The structural bets that need time/users or are lower-urgency at current scale: IN1/IN2 (install-time
integrity — the one gap a security-minded buyer notices; pair with the missing security audit), L1
(Foundry Network federation — the VISION endgame, gated on real sister foundries), L2 (operator
digest), H1 (perf). *Story: these compound once there's a base to protect and an audience to
federate.*

---

## 5 — Merge log (nothing lost)

- **The "window shouts over the shelf" cluster** — `HIERARCHY` F1/F2/F3/F4/F6 + `FUNNEL`
  biggest-leak + `REVENUE` two-primaries + `IMPROVEMENTS` v13 "10:1 tilt" → merged into **Theme 1**
  and items **SW1–SW4** (kept every report's specific evidence; strongest framing = HIERARCHY's
  "emphasis reserved for find+install").
- **The "unwired / unmeasured / frozen" cluster** — `FUNNEL §4` + `REVENUE` closed-till +
  `ROADMAP` Gate A + `IMPROVEMENTS` audience-zero, plus the live `STOP` → merged into **Theme 2**
  and **OW1–OW4**. FUNNEL's "GoatCounter first" and REVENUE's "Stripe first" were **not** a
  conflict — both are the same operator-wiring bundle; ruled into one NOW dependency.
- **Discovery/Reach** — `IMPROVEMENTS` v13 big-bet + `FUNNEL` Entry + `COMPETITIVE` arena →
  **DR1** (one item, three evidences).
- **Trust surfacing** — `COMPETITIVE` Bet 1 + `HIERARCHY` F4 + `IMPROVEMENTS` verified-by-foundry →
  split into **SW3** (on-site) and **DR2** (as a distribution flywheel).
- **Integrity** — `COMPETITIVE` stake #6 + `IMPROVEMENTS` Actions-pin + `SECURITY.md` → **IN1/IN2**
  + the recommended security audit.

**Disagreement ruled:** `HIERARCHY` implies investing in the window; `IMPROVEMENTS` v13 says stop
polishing a window no one visits. Ruling: do **only the cheap window-conversion fixes** (SW1–SW4 are
prerequisites for converting *future* traffic) and weight all larger net-new energy toward
**distribution (Theme 3)** and the shelf — which honors both reports.

---

*Report only — no code, config, or governance file changed; the existing `ROADMAP.md` is untouched.
This plan's critical path starts with an operator action (OW1: fix the token, delete `STOP`) that no
session here can perform. **Should I adjust the sequence** — e.g., pull integrity (IN1/IN2) forward,
or split the NOW milestone into an operator track and a loop track? And which absent audit should I
run next; my recommendation is the security/supply-chain one.*
