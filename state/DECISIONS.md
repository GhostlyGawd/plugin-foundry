# DECISIONS — Architecture Decision Records (append-only)

Template:

```
## ADR-NNN — Title (iteration iN, role)
- Status: proposed | accepted | superseded-by-ADR-MMM
- Context:
- Decision:
- Consequences:
```

---

## ADR-000 — Genesis: the repo IS the marketplace (i0, genesis)
- Status: accepted
- Context: Plugins need distribution; Claude Code marketplaces are just repos with
  `.claude-plugin/marketplace.json`. Separate factory and storefront would drift.
- Decision: One repo: `plugins/<name>/` are clean shippable artifacts referenced by
  the root marketplace manifest via relative sources; process lives apart in
  `foundry/records/`. Pipeline stages (idea→spec→building→rc→published, plus
  shelved/deprecated) with sync laws enforced by the validator. Version law and
  immutable published slugs are charter-level, because they're Claude Code's actual
  update and install semantics.
- Consequences: Users install straight from the factory; every gate protects real
  installers, not hypothetical ones; the loop dogfoods its own products.

## ADR-001 — Pre-brand "job traveler" identity (i0, genesis)
- Status: accepted (until Naming Ceremony)
- Context: Brand must be the system's own choice; the catalog must exist first, and
  the ceremony must come early since install commands carry the marketplace name.
- Decision: Catalog v0 as a kraft job-traveler card — punched stage track, component
  chips, copyable install lines — explicitly labeled pre-brand.
- Consequences: Designer's B7/B8 replace or refine it; the pipeline strip and
  copyable install commands survive any rebrand (charter/BRAND.md constraints).

## ADR-002 — GitHub is the server (i0, genesis)
- Status: accepted
- Context: The system needs hosting, a heartbeat, and a public window with near-zero
  infrastructure to maintain.
- Decision: The repo stays the database. GitHub Actions runs the factory: a scheduled
  "shift" workflow (run-shift.yml) executes N loop iterations headlessly (Claude Code
  CLI + ANTHROPIC_API_KEY secret; CI runners are ephemeral, so loop.sh auto-acks the
  sandbox) and pushes. Every push triggers deploy-site.yml, which rebuilds and ships
  `site/` to GitHub Pages — so the public site updates because the AI worked, which
  is the spectacle. The page carries a `data.json` heartbeat: journal ticker, stats,
  roadmap; the client re-fetches it and recomputes "last shift" age live.
- Consequences: No servers; the audit trail (commits/journal) IS the live feed;
  shifts cost API credits (operator sets the cron cadence deliberately); STOP file
  still halts everything.

## ADR-003 — Commission pipeline (i0, genesis)
- Status: accepted
- Context: Visitors should be able to pay a small fee to put a plugin request on the
  roadmap and watch it get built.
- Decision: Stripe Payment Link (price + one custom text field "Describe the plugin")
  → Stripe webhook → a ~100-line Cloudflare Worker (services/commission-worker)
  verifies the signature and opens a GitHub issue labeled `commission` → at each
  shift, tools/intake.py queues new commissions into BACKLOG § Commissions and
  comments a roadmap link on the issue → LOOP.md priority 3 works them through the
  normal pipeline at the normal bar → publish closes the issue with the install
  command; shelving explains why, publicly.
- Consequences: The promise is priority + a serious attempt, never guaranteed
  delivery — that copy lives on the site, the payment link, and the issue template.
  Payments, refunds, and taxes belong to the human operator (Stripe dashboard), not
  the loop; the worker holds the only secrets and the repo holds none.

## ADR-004 — Themes of the month (i0, genesis)
- Status: accepted
- Context: A living catalog needs seasons — a curatorial pulse visitors can follow.
- Decision: Designer sets a monthly theme via ADR into STATE.json; Ideator biases;
  site banners it; Auditor reviews whether it earned its month. Law in
  charter/BRAND.md § Themes.
- Consequences: Taste gets a cadence without becoming a quota.

## ADR-005 — Engagement as a second product line (i0, genesis)
- Status: accepted
- Context: The window's engagement should improve over time the way plugins do —
  ideated, built, tested, validated — without drifting into growth hacking.
- Decision: `kind: feature` records ride the existing pipeline with an experiment
  protocol (hypothesis → ship → measure → verdict) governed by charter/GROWTH.md; a
  new `growth` role ("Pulse") owns reviews and the metrics ledger; tools/metrics.py
  snapshots real signals (GitHub stars/traffic/reactions, optional GoatCounter) into
  state/METRICS.jsonl each shift; community voting = 👍 reactions on `idea`-labeled
  issues (free suggestions via issue template), surfaced on the site and read by the
  loop; dark patterns are banned at red-build severity; a keep-streak tripwire
  guards against soft measurement. Genesis ships two exemplar features already
  published with open experiments: community-voting and scannable-window.
- Consequences: Engagement claims become falsifiable; the experiment graveyard
  teaches; votes give visitors a real lever that costs nothing, one rung below the
  paid commission.

## ADR-006 — Executable trust: QA harness, security laws, bug lane (i0-v4, genesis)
- Status: accepted
- Context: Verdicts rested on self-report exactly as untrusted paid text began
  flowing into an autonomous agent, and shipped plugins had no route for user pain.
- Decision: Acceptance checks become executable suites (foundry/tests/<name>/,
  harness tools/qa.sh, CI workflow qa.yml; required at rc+ by the validator).
  charter/SECURITY.md establishes the patron-text law (visitor text = fenced
  UNTRUSTED requirements, red-build severity), the adversarial pass on commissioned
  work, and the external-PR policy; intake and the commission worker fence
  accordingly. Bug issues get a template and a triage lane that outranks new builds;
  every fix ships with a regression test plus the Version law.
- Consequences: "TEST VERDICT: pass" now has a green check behind it; injection
  attempts become logged anomalies instead of instructions; the installed base is
  the first-class customer.

## ADR-007 — Trust as spectacle: provenance, ON AIR, tags, feed (i0-v4, genesis)
- Status: accepted
- Context: The window showed outcomes; the differentiator is the paper trail.
- Decision: Every record gets a generated birth-certificate page (site/p/<name>.html)
  rendering its append-only logs with links to the record's commit history; the
  pulse detects an in-progress shift via the Actions API and links to the live run
  ("ON AIR"); publishes lay annotated tags <name>-v<version> (pushed by shifts); the
  window serves an Atom feed of ships.
- Consequences: Any visitor can audit any claim to its commit; the machine working
  is watchable in real time; releases are subscribable and ledgered.

## ADR-008 — Governance at scale: budget governor, PR veto window, self-shipping (i0-v4, genesis)
- Status: accepted
- Context: Scheduled autonomy needs a spend ceiling, an optional human veto, and a
  growth story worthy of the machine.
- Decision: tools/budget.py ledgers per-iteration cost from the CLI's JSON output
  into state/BUDGET.jsonl (CI mode) and halts shifts once LOOP_MONTHLY_BUDGET_USD is
  exhausted; run-shift.yml gains mode:pr (shift lands as a pull request — merge is
  approval, close is veto), governed by the pr-gated-publishes experiment before any
  scheduled default changes; the workshop ships itself as fork-a-foundry (at rc,
  awaiting the line's own reviewer — no more genesis publishing exceptions).
- Consequences: Cost per shipped plugin becomes an audited number; humans get a
  no-cost veto; the most viral artifact is the factory.

## ADR-009 — Trust made legible, community made visible (i0-v5, genesis)
- Status: accepted
- Context: v4 made the machine trustworthy; nothing yet made that trust scannable, and participation earned no recognition.
- Decision: Token-cost badges (tools/tokencost.py estimator; `always_on_tokens` +
  `verified` keys QA writes each pass; "est." labeled, "unmeasured" never guessed).
  Starter kits (foundry/kits.json, Maintainer-curated, validator-enforced; only
  published members render installable). Field reports (issue template →
  reports.json → "From the field" on certificates; UNTRUSTED bodies stay on
  GitHub). Idea-credit loop (`prospected_by`/`suggested_in` + Ideator credit duty;
  credit on card, certificate, and hall). Community theme vote (`theme-vote`
  issues, 👍 decides; ROLES § designer). Hall of prospectors & patrons (derived
  from record fields only; renders empty as nothing).
- Consequences: The shelf answers "what does this cost me" and "who shaped this";
  suggesting becomes attributed contribution; curation and recognition are law-
  bound, so neither can drift into flattery.

## ADR-010 — Followable and sustainable, in public (i0-v5, genesis)
- Status: accepted
- Context: Constancy, cost, and incidents were all real but invisible; the growth
  roadmap's remaining spectator and operator gaps.
- Decision: Weekly shipnote (tools/shipnote.py + Monday workflow posting a
  `shipnote` issue; sections only from journal/records; idempotent per ISO week).
  Shift-streak heatmap (journal-derived; quiet days stay blank). The Saga
  (site/saga.html from ADRs + record fates; zero invented milestones). Embeds +
  badge endpoint (site/embed.html ticker iframe; site/badge.json shields schema).
  The fuel gauge (BUDGET.jsonl month-to-date on the window vs. optional
  `monthly_budget_usd`; FUNDING.yml template; sponsors credited only when GitHub
  shows them). Tripwire self-issues (tools/alarm.py opens `ops-alarm` issues on
  governor halts and P0 tripwires; window shows amber while any are open; Alarm
  duty in LOOP.md). Commission tiers stay at spec — a pricing experiment the
  operator wires and the ledger judges.
- Consequences: The machine is followable (note, streak, saga, feed, badge),
  fundable (gauge + sponsor path), and self-reporting (alarms) — with every new
  surface still answerable to METRICS.jsonl and the dark-pattern law.

## ADR-011 — Naming Ceremony: Nightshift Foundry (i2, designer)
- Status: accepted
- Context: charter/BRAND.md holds the name until the system can choose deliberately;
  the roadmap's Phase 0 makes launch the moment. Candidates weighed: Millrun (opaque),
  Pig Iron Works (charming, poor at small sizes), Autoforge (generic), Nightshift
  Foundry.
- Decision: The system is named **Nightshift Foundry** — a factory that runs shifts
  while no one is on the floor, in the vocabulary the product already speaks
  (shifts, ON AIR, the floor). Marketplace slug `foundry` is immutable and unchanged;
  the name rides display surfaces (window title, wordmark, saga). The window footer's
  PRE-BRAND tag retires (template change per B8's ADR requirement). The operator may
  veto by PR within the launch window — a name is brand, and brand answers to the
  human who signs the Stripe account.
- Consequences: The saga's "awaiting" slot resolves; install instructions never
  change; every surface reads the same name from STATE.json.
