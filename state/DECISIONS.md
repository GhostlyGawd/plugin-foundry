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

## ADR-012 — Relax the hook-quoting check to the docs pattern (i10, builder)
- Status: accepted (proposed i10, applied i12 — two-iteration rule honored)
- Context: tools/validate.py requires the literal token `"${CLAUDE_PLUGIN_ROOT}"`,
  which false-positives on the official docs pattern
  `"${CLAUDE_PLUGIN_ROOT}/path/script.sh"` (whole path quoted). Found by dogfood
  while building commit-craft — the gate blocked a lawful artifact.
- Decision (proposed): accept any command where `${CLAUDE_PLUGIN_ROOT}` is
  immediately preceded by a double quote (`"${CLAUDE_PLUGIN_ROOT}` substring),
  covering both the var-quoted and whole-path-quoted forms; keep failing truly
  bare expansions.
- Consequences: gate matches the documented contract; no published artifact is
  affected (fix lands before commit-craft publishes).

## ADR-013 — Metadata-only re-verification stamps are exempt from the version law (i83, builder)
- Status: accepted (proposed i83, applied i86 — two-iteration rule honored)
- Context: the weekly re-verify job re-runs every published suite and refreshes
  `verified:` (and `tested_with` when the CLI is present) on records. The version
  law says changes to a published plugin bump semver + CHANGELOG + tag — but these
  stamps touch only record front-matter metadata, never plugin files, and forcing
  a weekly patch-bump across the shelf would make version numbers noise.
- Decision (proposed): writes that modify only `verified:`/`tested_with` on a
  record are exempt from the version-bump law. Any write under plugins/ remains
  fully bound. charter/QUALITY.md gains the exemption text when this applies.
- Consequences: freshness becomes a standing, dated promise; version numbers keep
  meaning "behavior changed".

## ADR-014 — v8 directed slate: activation first, then community (i88, ideator)
- Status: accepted (queue seeding follows audit precedent: audit-001/002 both set
  role_queue to match upcoming work; LOOP.md's default-cycle refill is the fallback,
  not a ceiling)
- Context: an operator-directed session ordered the roadmap recommendations built in
  sequence: (1) publish the ten rc features stalled behind review (starter-kits,
  token-cost-badges, saga-page, weekly-shipnote, embed-badges, field-reports,
  community-hall, idea-credit-loop, fuel-gauge, shift-streak), (2) rebalance the
  catalog toward everyday-utility plugins (the shelf is meta-heavy: 3 of 7 published
  plugins are about the foundry itself), (3) lower the community contribution floor
  (idea-label intake, seeded boards, adversarial-qa-bounties).
- Decision: role_queue seeded for the full slate — reviewer/maintainer pairs per rc
  record, builder/builder/qa/reviewer/maintainer for one utility-plugin walk
  (test-gap-nudge first: hook-only, smallest, exercises hook-safety law), a growth
  iteration for honest board seeding + the intake ADR, builders for intake.py and
  adversarial-qa-bounties, and a closing auditor. Reviews stay genuine — bouncing is
  a service, and the rubber-stamp tripwire stands: if the slate's reviews bounce
  nothing, the closing audit runs as P0.
- Work rides the operator's PR branch (claude/product-roadmap-ux-f11e8a) — this doubles
  as the pr-gated-publishes trial run (see that record's spec): publishes land on main
  only when the PR merges, giving the operator a veto window over the whole slate.
- Consequences: ten features exit rc limbo or bounce honestly; first utility plugin
  since v5 walks the full line; community intake path opens. Counts stay floors, not
  the point.

## ADR-015 — intake.py grows an `idea` lane (i119, growth)
- Status: accepted (proposed i119, applied i120 — two-iteration rule honored)
- Context: the co-op lane's floor is a spec PR — high for a passerby. The vote
  board and mailbag now open with foundry-authored seeds, but a visitor's raw
  pitch still has no automated path into the workshop: intake.py handles only
  `commission` and `bug` labels; `idea` issues are read for votes but never land
  in BACKLOG § Idea inbox.
- Decision (proposed): intake.py also lists open `idea`-labeled issues and
  appends any new ones to BACKLOG § Idea inbox as
  `- [ ] I#<issue> (<author>) <title>` (deduped by issue number, patron-text law:
  titles fenced as data). The Ideator formalizes from the inbox with full credit
  (`prospected_by`/`suggested_in`), which idea-credit-loop already renders.
- Consequences: pitch → inbox → formalized → credited becomes fully automatic;
  the contribution floor drops from "write a spec PR" to "open an issue".

## ADR-016 — v9 slate: the discovery-report backlog, in order (i136, maintainer)
- Status: accepted (queue seeding per audit precedent; tools/ items apply from
  i137+ under the two-iteration rule with this ADR as the prior-iteration record)
- Context: operator commissioned a full product-discovery audit (IMPROVEMENTS.md,
  committed with this ADR) and directed: build everything, in order. 13 items,
  two broken today (README front-door placeholder; night-clerk's stale bundled
  catalog), the rest conversion, trust, and reach work on existing surfaces.
- Decision: work IMPROVEMENTS.md #1→#13 as loop iterations on the restarted PR
  branch (pr-gated publishes, second run). This ADR authorizes the slate's
  tools/ work: validate.py clerk-freshness law (#2), build.py template changes
  (OG meta #5, copy buttons #6, saga ellipsis + report-cap link #9, dark-mode
  palette #11, recorded-transcript labels #12), and a new tools/preflight.py
  (#13). Version law applies in full to the plugin README sweep (patch bumps).
  role_queue seeded: maintainer(sweep), builder(night-clerk 0.1.1), builder
  (validator law), maintainer(hygiene), maintainer(solo kit), builder(OG),
  builder(copy), growth(pr-gated verdict), designer(polish), qa(backfill ×2),
  designer(dark mode), builder(transcripts), builder(preflight), auditor.
- Consequences: the funnel is honest before the first measured visitor; the
  clerk can never drift again; the window earns shares and dark rooms.

## ADR-017 — Directed slates publish via PR; cron default deferred (i144, growth)
- Status: accepted
- Context: pr-gated-publishes specs a trial of `mode: pr` cron shifts (10 PRs or
  21 days). The factory isn't live, but two operator-directed slates (v8: PR #9
  merged in minutes with zero vetoes; v9: in flight) exercised the same veto
  window end to end.
- Decision: multi-iteration directed sessions always land as PRs (this codifies
  existing practice). The scheduled-shift default remains `direct` until the
  spec's own cron-shift data exists — no default flipped on proxy data.
- Consequences: humans get a costless veto exactly where stakes are highest
  (large slates); the experiment's terms stay intact for the real trial.

## ADR-018 — v10 slate: the post-v9 discovery report, in order (i153, directed)
- Status: accepted (tools/, template, and workflow items apply from i154+ under
  the two-iteration rule with this ADR as the prior-iteration record)
- Context: operator merged the post-v9 discovery slate (IMPROVEMENTS.md, PR #12)
  and directed: build everything, in order, autonomously. 14 items: shelf value
  (update awareness, hook knobs, storefront picker, certificate READMEs), the
  untested gates (PR CI, gate tests, qa.sh silent-skip, parser dedup),
  productization (SECURITY.md, hook debug mode, CI pin, release assets), and two
  line-riders (verified-by-foundry, foundry-network) that advance one stage per
  iteration like everything else.
- Decision: work IMPROVEMENTS.md #1→#14 as directed iterations riding a PR
  (ADR-017 lane). This ADR authorizes the slate's tools/ and workflow work:
  clerkcat.py version field (#1), build.py template changes (picker #3,
  certificate READMEs #4, verified hall #13, network cross-list #14), new
  .github/workflows/gates.yml (#5), foundry/tests/_tools/ gate suite (#6),
  qa.sh rc+ silent-skip fail (#7), tools/lib.py extraction (#8), workflow pins
  (#11), release assets (#12), and tools/doctor.py (#13). Version law applies
  in full to every published-plugin change (patch/minor bumps + CHANGELOG +
  tag). Roles are named per iteration in the journal; role_queue stays the
  default cycle for future shifts (i152 precedent).
- Consequences: installed users learn about updates; the gates that guard
  everything gain their own guard; PRs stop merging unchecked; the machinery
  points outward for the first time (verification and federation).

## ADR-019 — v11 slate: the UX audit, in order (i180, directed)
- Status: accepted (tools/, template, and skill items apply from i181+ under
  the two-iteration rule with this ADR as the prior-iteration record)
- Context: operator reviewed the merged v10 build-out and directed a UX pass:
  "more user friendly, easy to use, and intuitive" — 12 items across three
  personas (installers, window visitors, operator/contributors), appended to
  IMPROVEMENTS.md with this ADR. The lore is an asset for spectators and a tax
  on installers; the fix is a plain-language layer, never lore removal.
- Decision: work the v11 items #1→#12 as directed iterations riding a PR
  (ADR-017 lane). This ADR authorizes: build.py template changes (strap +
  card-link language #1, card changelog links #3, kit paste note #5,
  visitor-first reorder #6, nav grouping #7, unified discovery input #8,
  follow chip #9), the 8-README Manage sweep with patch bumps under full
  version law + plugin-smith scaffold template (#2, #4), preflight.py growth
  (--issue checklist #10, tag-drift check #11), and a new /backlog command
  (#12). Window minor-versions once at the end of the template run. Roles
  named per iteration in the journal; role_queue untouched (i152 precedent).
- Consequences: the funnel reads human at first contact; every installed
  README answers "how do I manage this thing"; the operator's two known
  footguns (unchecked go-live list, stranded local tags) become visible.
