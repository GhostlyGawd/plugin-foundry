# AI-IDEAS — Opportunity Scan

*Brief 12 (AI Opportunity Scan), adapted — with a twist this product forces: **the
workshop is already autonomous AI.** The loop pitches, builds, tests, reviews, and
publishes every plugin. So "add AI" is usually the *wrong* instinct here, and the
gimmick list (§4) does more work than the idea list. The bar: a new AI feature must beat
not just a button, but **the AI we already run** — it must live somewhere the loop
doesn't. Read-only pass; the only write is this file.*

---

## 1 — Raw material (the data & toil this product actually has)

**Data that accumulates:**
- **Narrative:** `state/JOURNAL.md` (append-only, every iteration), `DECISIONS.md` (ADRs),
  `reviews/` (audits), and **39 job-traveler records** with structured frontmatter + prose
  (`foundry/records/*.md`).
- **Structured telemetry:** `STATE.json`, `METRICS.jsonl`, `BUDGET.jsonl`, `marketplace.json`,
  `categories.json`.
- **Inbound, natural-language:** the idea inbox (`BACKLOG.md`), `commission`-labeled issues,
  `theme-vote` issues.
- **The plugins themselves** — every skill/agent/hook is a prompt artifact.

**Toil that repeats (the honest candidates for automation):**
- **Visitor toil:** figuring out *which of 10 plugins* solves their problem — `FUNNEL.md`'s
  single biggest leak.
- **Intake toil:** for each new idea/commission — is it a **duplicate** of a published or shelved
  record? which **category**? how **feasible** (which components)?
- **Operator toil:** reading the raw journal + ledgers to answer "what shipped, what's stuck,
  where's the fuel."

**Judgment calls the product could draft:** which plugin fits a need (night-clerk already does
this in-session); is an incoming request a dup; a plugin's name at the Naming Ceremony.

---

## 2 — Ideas

Each answers the five questions the brief requires, plus value/feasibility.

### Idea 1 — Semantic shelf matching (need → plugin), computed at build time
- **User moment:** the site shelf + `#empty` search — a visitor types *"I keep forgetting to
  write tests"* and gets **test-gap-nudge** + its exact install line. Directly targets
  `FUNNEL.md`'s biggest leak (10 undifferentiated cards, no guide).
- **Data needed:** have it — the 10 records + descriptions. Missing: natural-language **aliases**
  per plugin (the phrases a user would actually type).
- **Failure mode:** wrong match → wrong plugin recommended. Fallback: always render "or browse
  all / **commission it**" beneath the match; **never auto-install**; show the match's *why*.
- **Cost & latency:** the trick — **AI runs at build, not at runtime.** The loop generates
  aliases/keywords per plugin once per shift (batched, cents); the site stays static
  (GitHub-is-the-server), search runs client-side at zero latency/zero LLM cost.
- **Build shape:** build-time prompt enrichment (a `keywords`/`aliases` field per record) folded
  into the existing static `renderClerk` search. No backend, no runtime model.
- **Value: HIGH** (biggest funnel leak) · **Feasibility: HIGH** (fits the no-backend law).

### Idea 2 — Intake triage: dedup + categorize + feasibility-tag
- **User moment:** the ideator role / `tools/intake.py` processing a new idea-inbox pitch or a
  paid `commission` issue.
- **Data needed:** have it — the 39 records + 10 published plugins as the comparison set.
- **Failure mode:** a wrong "duplicate" flag could wrongly sideline a valid (or *paid*) request.
  Fallback: output is a **draft tag for the human/ideator to confirm**, never an auto-decline —
  the loop already has a legible review gate; this feeds it, doesn't replace it.
- **Cost & latency:** one classification call per inbound issue — trivial volume, fully async,
  high tolerance.
- **Build shape:** prompt-only with the catalog snapshot in context (RAG is overkill at 39
  records — just include them).
- **Value: MED–HIGH** (saves ideator toil; prevents building a dup; protects paid requests) ·
  **Feasibility: HIGH.** Beats the boring `grep`, because dup-ness is *semantic* ("write my
  commits" ≈ commit-craft).

### Idea 3 — Operator digest with anomaly-flagging
- **User moment:** the operator checking in (private counterpart to the public weekly shipnote).
- **Data needed:** have it — `JOURNAL` tail + `METRICS`/`BUDGET` + open issues.
- **Failure mode:** hallucinated summary or a missed stall. Fallback: **numbers come from the
  ledgers, not prose**, and every claim links its source line (the repo's own "cite it" law).
- **Cost & latency:** one summarize per shift/week — cheap.
- **Build shape:** prompt-only over structured telemetry + journal tail.
- **Value: MED** (the additive part over the existing shipnote is *anomaly-flagging*: stuck RCs,
  rubber-stamp streaks, unpaid-because-unwired commissions) · **Feasibility: HIGH.**

### Idea 4 — Naming Ceremony assistant
- **User moment:** the designer role at spec — names are **immutable/forever**, so this is
  high-stakes but infrequent.
- **Data needed:** existing slugs (collision set) + the plugin's job.
- **Failure mode:** proposes a name that collides or is trademarked. Fallback: the **collision
  check is deterministic** (grep slugs + registry check) — the model only *proposes*, a rule
  *verifies*. The honest AI/rule split.
- **Cost & latency:** trivial, one-off per plugin.
- **Build shape:** prompt-only generation + deterministic collision check.
- **Value: LOW–MED** (infrequent — 10 names so far) · **Feasibility: HIGH.**

---

## 3 — Value × feasibility ranking

| Rank | Idea | Value | Feasibility | Why here |
|---|---|---|---|---|
| 1 | **Semantic shelf matching (build-time)** | High | High | Attacks the #1 funnel leak; respects the no-backend law |
| 2 | **Intake triage** | Med–High | High | Saves loop toil, protects paid commissions from dup-decline |
| 3 | **Operator digest + anomaly flags** | Med | High | Cheap; additive over the existing shipnote |
| 4 | **Naming assistant** | Low–Med | High | Genuine but low-volume |

---

## 4 — Gimmick list (rejected — this list protects the roadmap)

For an already-AI product, the gimmicks are the *tempting* ideas. Named so they don't sneak back:

- **Live LLM search / a chatbot on the static site.** Adds a backend the architecture deliberately
  refuses ("GitHub is the server"), plus per-query cost + latency + hallucination — to do what
  **night-clerk already does in-session for free** and what Idea 1's precomputed index does with no
  runtime model. A visitor wants an install line, not a conversation. **Reject.**
- **AI-reordered shelf** for 10 items that fit on one screen. LLM cost/latency/wrongness for zero
  gain over a sensible static default + the existing categories. A **rule wins.** **Reject.**
- **Auto-generate-and-publish plugins that skip the QA+review gate** to "ship faster." The loop
  already generates plugins; the **gate is the entire value proposition** (`COMPETITIVE.md` Bet 1).
  This isn't a feature, it's an anti-feature that deletes the differentiation. **Reject.**
- **AI-written field reports / patron testimonials / "mood of the foundry" sentiment.** Violates the
  no-fake-data law and the honesty brand outright, for zero decision value. **Reject hard.**
- **AI budget "predictions."** The `BUDGET.jsonl` ledger + a governor cap is exact and honest; a
  forecast adds uncertainty where certainty exists. A **number beats a guess.** **Reject.**

---

## 5 — Prototype this week (scoped to a day)

**A day-sized slice of Idea 1:** have the loop generate a `keywords`/`aliases` field (5–10
natural-language phrases a user might type) for each of the 10 published plugins during
`tools/build.py`, and fold those aliases into the existing static `renderClerk` keyword search.

Why it's a day: it's a **build-time enrichment + a search tweak**, no backend, no runtime model,
no new page. Why it's worth it: it converts the site's blind keyword match into "describe your
problem in your own words → get the right plugin," attacking the **biggest funnel leak** while
staying inside the no-backend law. Wrong-answer handling ships with it (the "or commission it"
fallback from Idea 1). It's AI where the loop *isn't* — enriching how a stranger finds the shelf.

---

*Report only — nothing built, no config changed, operator STOP still in force. Which idea should I
prototype? My pick is the day-scoped **Idea 1** (biggest leak, safest shape); **Idea 2 (intake
triage)** is the best follow-on since it compounds as commissions arrive. Say the word and I'll open
it as a spec on the normal line — tested and reviewed like everything else, never rubber-stamped.*
