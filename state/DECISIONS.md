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

## ADR-020 — the operator's clicks become dispatches (i193, directed)
- Status: accepted (workflow changes apply from i194+ under the two-iteration
  rule with this ADR as the prior-iteration record)
- Context: operator directed "figure out a way to do all of those yourself" —
  the remaining go-live actions. Session limits: git tag pushes 403
  (branch-scoped proxy) and the session API token has no write scopes. But
  GitHub Actions workflows run with contents:write and pages:write, and the
  session CAN dispatch workflows. So the repo grows the hands it needs.
- Decision, three workflow changes + an ops sequence:
  1. `.github/workflows/lay-tags.yml` (NEW, workflow_dispatch only):
     recreates the annotated tags listed in `state/TAGS-PENDING.json`
     (skip-if-exists, never forced), and reports — names/presence only, never
     values — whether CLAUDE_CODE_OAUTH_TOKEN / ANTHROPIC_API_KEY /
     GOATCOUNTER_TOKEN secrets and LOOP_MONTHLY_BUDGET_USD are configured,
     so the session can decide whether a first shift can run.
  2. `release-on-tag.yml` gains `workflow_dispatch` with a `tag` input and
     checks out the TAG'S OWN REF before cutting — this also fixes a latent
     defect: a dispatch-cut (or re-run) release previously would have zipped
     the CURRENT tree, attaching wrong-version artifacts.
  3. `deploy-site.yml`: `actions/configure-pages@v5` gains `enablement: true`
     — the first deploy CREATES the Pages site with source=Actions, replacing
     click-list item 1.
  Ops sequence after merge (session-driven, via actions_run_trigger):
  lay-tags → verify ls-remote → release-on-tag ×15 oldest-first → deploy-site
  → verify the window serves → run-shift ONLY if the probe shows a Claude
  secret present. Hard line unchanged: the session never sets, reads, or
  copies secret VALUES; a missing API key remains the operator's alone.
- Consequences: the click-list shrinks to "add a secret" (+ optional budget
  var / GoatCounter / FUNDING); releases become reproducible from any tag;
  Gate A's window can finally go live without a human browser session.

## ADR-021 — v12 slate: the live-window audit, in order (i197, directed)
- Status: accepted (workflow/tools/template items apply from i198+ under the
  two-iteration rule with this ADR as the prior-iteration record)
- Context: third operator-directed discovery pass, first with the window LIVE.
  14 items: the visitor funnel's missing labels (proven live — release
  misfires couldn't attach ops-alarm), a ninth plugin, release-page
  conversion, social preview, tests for the untrusted-input handler and the
  spend governor, backlog hygiene, shift-zero feedback, 404/sitemap, verified
  badges, and the genesis ceremony. Operator directive: "Build all in order
  until complete" — given after 4.1 was explicitly flagged as requiring a
  blessing to leave this repo, so that blessing is on the record.
- Decision: work v12 #1.1→#4.1 as directed iterations riding a PR (ADR-017).
  This ADR authorizes: .github/workflows/ops-guard.yml (labels + failure
  catcher, 1.1+2.4), release-body changes (1.3+3.4), build.py additions
  (og:image 1.4, 404 3.2, sitemap/robots 3.3, verified badges 4.2), test
  seams in tools/intake.py, budget.py, metrics.py (2.1, 2.3), a run-shift
  first-shift feedback step (3.1), and — as a one-time, operator-blessed
  charter exception — creating and seeding ONE sibling repository via the
  session's GitHub tools for the genesis ceremony (4.1), registered in
  network.json only after the Lane 4 verification duty passes against the
  sibling itself. The exception is scoped: one repo, this slate, never a
  standing power.
- Consequences: the funnel works when the first visitor arrives; the factory
  stops failing silently; the shelf grows; and if 4.1 lands, the family tree
  gets its first name from the only entity that could honestly claim it —
  the foundry's own child.

## ADR-022 — v13 slate: the shelf, not the window, in order (i214, directed)
- Status: accepted (workflow/tools items apply in later commits of this slate
  under the two-iteration rule with this ADR as the prior-iteration record).
- Context: fourth operator-directed discovery pass (IMPROVEMENTS v13, merged
  PR #20). Operator directive: "Build all in order." 14 items across four
  lanes — shelf-truth (the catalog misdescribes two plugins), plugin depth
  (a missing companion hook, cross-plugin synergies, catalog decay, README
  drift), the gates (a spuriously-failing PR gate, an inert money path,
  silent truncation, a re-verify crash, a test-filter hole), and an honest
  reckoning with a traffic count of zero.
- Two ground truths found while building, that widen A1: **both** mislabeled
  records contradict themselves. `pr-narrator` front matter says
  `components: [agents]` but its Spec/Build log say "one skill" — it ships a
  skill. `env-doctor` front matter says `components: [hooks]` but its Spec
  says "one skill" — it ships a skill with no hook. So A1 relabels
  pr-narrator to the truth (skill), and A2 resolves env-doctor's
  contradiction toward value by building the SessionStart hook its catalog
  already promises — after which env-doctor legitimately carries
  `[skills, hooks]` and its "at session start" one-liner becomes true.
- Decisions:
  1. **Catalog regenerated once.** night-clerk's bundled `data/catalog.json`
     embeds every plugin's version and one-liner; many v13 items bump
     versions. Rather than churn night-clerk once per bump, all
     catalog-affecting plugin changes land first, then `tools/clerkcat.py`
     regenerates the catalog inside a single night-clerk bump (B7). The
     validator's clerk-snapshot law checks only the plugin *name* set (no
     plugin added or removed here), so gates stay green throughout.
  2. **One bump per plugin.** Where several items touch one plugin (e.g.
     session-recap: B5 hook + B6 synergy + B8 README), the changes land in a
     single semver bump + CHANGELOG entry, not one per item — one meaningful
     bump per slate serves installed users better than a stutter of patches.
  3. **This ADR authorizes** the later-commit changes to `.github/workflows/`
     (`gates.yml` sitemap-drift fix C9, `qa.yml` tools path filter C13) and
     `tools/` (`intake.py`/`metrics.py` issue-limit fix C11, `restamp.py`
     None-guard + routing four stragglers through `lib.parse_front_matter`
     C12). New hooks (env-doctor SessionStart, session-recap Stop) ride the
     hooks-are-guests law: narrow matchers, fail-open, quoted roots,
     executable shebang scripts, and a regression suite each.
- Consequences: the shelf stops lying, the flagship gate stops crying wolf,
  the money path survives its first dollar, and the growth ledger stops
  counting experiments toward a kill they were never given traffic to avoid.
  Slate rides a PR (ADR-017 precedent); nothing autonomous — the STOP file
  stays, the Claude secret remains the operator's alone.

## ADR-023 — dormant experiments: don't count pre-traffic features toward a kill (i215, auditor)
- Status: accepted (v13 D14; rubric change to charter/GROWTH.md).
- Context: `state/METRICS.jsonl` reads 0 stars / null traffic / 0 votes across
  every snapshot — the window is frozen behind Gate A (the Claude secret). Yet
  BACKLOG listed eight growth experiments with concrete review dates keyed to
  those null metrics. By the existing protocol, an experiment with no data
  extends once then kills, so the whole growth catalog was on a path to
  auto-kill it was never given traffic to avoid — and no experiment could ever
  earn `keep`, so the "4 keeps = soft" calibration tripwire could never fire.
  The measurement system was running against a wall it couldn't see.
- Decision: add a **dormant** state. A pre-launch experiment whose metric is
  null/0 is parked, not open: its review clock starts at first real traffic
  (Gate A satisfied), not a calendar date. Dormant experiments are excluded
  from the extend-twice-kill rule and from the calibration tripwire's verdict
  mix; the Auditor lists them separately and does not read their missing
  verdicts as measurement gone soft. charter/GROWTH.md carries the rule;
  BACKLOG's "Experiments open" section is relabeled to dormant with
  traffic-anchored cadences.
- Consequences: the growth ledger stops lying by omission — features aren't
  marched to the graveyard for failing a test they were never allowed to sit,
  and the honesty tripwire stays meaningful for when traffic actually arrives.

## ADR-024 — v14: finish the buildable line, in order (i216, directed)
- Status: accepted (tools/ items apply in later commits of this batch under the
  two-iteration rule with this ADR as the prior-iteration record).
- Context: operator directed "Build all until fully complete." The v13 slate is
  merged; what remains buildable by the line alone (not gated on operator/world/
  community) is: the tenth plugin (todo-ledger, idea → published), the first
  Theme of the Month, a bug the firstborn found (build.py assumes site/ exists),
  and two P3 polish items (countdown derives shift hours from the cron; a
  fork-a-foundry from-spec link). Everything else is gated — commission tiers
  and GoatCounter need the operator; the pr-gated CRON default and roadmap gates
  A/B/C need real traffic; those stay open and honestly labeled.
- Decision: build the buildable set as directed iterations riding a PR (ADR-017
  lane). This ADR authorizes the tools/ changes: `build.py` mkdirs `site/` at
  the top of the build (bug fix — a fresh checkout without site/ no longer
  crashes) and derives the shift hours in the countdown from
  `run-shift.yml`'s cron instead of a hardcoded constant (drift fix). todo-ledger
  walks the full pipeline at the normal bar (spec with acceptance checks → build
  → 3-tier QA with an executable suite → review → publish + marketplace entry +
  night-clerk catalog regen). Version law binds every published-plugin change.
- **Theme of the Month (BRAND.md § Themes), recorded here:** July 2026 =
  **"Repo hygiene"** — *plugins that surface the quiet debt a codebase
  accumulates (stale TODOs, missing tests, drifted toolchains, unreviewed dep
  bumps) and make it legible before it bites.* Set directly by the designer
  rather than by community vote: the three-candidate `theme-vote` path needs an
  audience the window doesn't have yet (dormant, per ADR-023); it arms with
  traffic. The theme biases the ideator and banners the window; todo-ledger,
  built this batch, is the theme's first exhibit.
- Consequences: the shelf reaches ten plugins across the quality lane the theme
  names; the build tool survives a bare checkout; the window shows a theme; and
  the backlog's open items are exactly the ones only a human or real users can
  close — nothing buildable left un-built.

## ADR-025 — the window, reimagined for the first-time visitor (i217, designer)
- Status: accepted — operator-directed, landing as a draft PR (the human veto
  window, ADR-020 lane). This ADR is the prior-iteration record for the
  tools/build.py change it authorizes (two-iteration rule): the entire index
  TEMPLATE (markup, CSS, and render script) is rewritten, and build_site now
  passes `categories` (from foundry/categories.json) into data.json.
- Context: the operator directed a redesign — *"reimagine the site so it is
  incredibly easy to use and understand for a first-time visitor that knows
  nothing about the niche or product… a strong visual language and brand
  direction that is approachable, comprehensible, educational, and inspiring…
  a high-converting eCommerce site that sells the features and benefits,
  addresses the pain points, and bridges the value/understanding gap at every
  stage of the funnel."* The window (v0.6) was a beautiful **insider spectacle**:
  it opened on live telemetry, industrial jargon (the shelf, the line,
  prospectors, ON AIR), and an all-monospace job-traveler aesthetic that assumes
  the visitor already knows what a Claude Code plugin is and why they'd want one.
  That optimizes for "watch the machine," not "understand and install." Two forks
  were put to the operator (AskUserQuestion): brand boldness → **evolve the
  Nightshift Foundry identity** (keep it, modernize it) over a mainstream rebrand
  or a copy-only pass; primary conversion → **install a free plugin** over the
  paid commission or fork-a-foundry.
- Decision: **evolve, don't replace.** Keep the name, the immutable `foundry`
  slug, the warm kraft palette, the foundry soul, every honesty/substantiation
  law, and all provenance + telemetry machinery. Change three things:
  1. **Typography for approachability** — a friendly system sans for headings and
     body; monospace kept only for code, install commands, telemetry, and the
     wordmark. Real whitespace, a clear type hierarchy, and one warm **ember**
     accent for primary CTAs (blue "stamp" stays for links/provenance).
  2. **Information architecture as a conversion funnel** — hero that says in one
     breath *what this is and why you'd care* (defines Claude Code + plugins in
     plain language) → a "whole idea in 30 seconds" primer with a concrete
     before/after → a 3-step install path → **the shelf**, now published plugins
     only, grouped by category with friendly names, benefit-led cards, a
     prominent copyable install line and a "tested & reviewed" trust chip on each
     → starter kits → a trust section ("why you can trust what installs") → the
     spectacle, **demoted** into one "Under the hood — the workshop, live"
     section reframed as the inspiring autonomy proof → vote → commission
     (secondary) + install → footer. A label legend teaches skill/hook/agent/tok.
  3. **Honesty under conversion pressure** — the stat row features only true,
     substantiated, non-embarrassing numbers (10 free plugins · autonomous shifts
     · categories · 100% tested & reviewed, the last derived from the publish law
     the validator enforces). The 0-valued stars/watchers are *not* shown as hero
     proof (no inflation, dark-pattern law), and the 0-vote ideas stay honestly
     displayed in the Vote section rather than hidden.
- Constraints upheld (BRAND.md standing constraints + charter): install commands
  render as copyable code; the pipeline stays legible (roadmap lanes + per-card
  version); "not affiliated with Anthropic" stated in the footer; the site is
  still generated (template single-sourced in tools/build.py — `site/` is never
  hand-edited); every test-pinned mechanism is preserved verbatim (filterCards,
  nextShift, the token-cost stale logic, the hidden verified/hall sections, the
  saga/theater/almanac/queue links, reduced-motion guards, aria-pressed). Gates
  green: validate, build, qa 257 ok · 0 fail, official --strict, and a
  zero-horizontal-overflow check at 320/402/1440px.
- Consequences: the window now converts a stranger who knows nothing about the
  niche — understand → browse → install — instead of only rewarding insiders.
  The brand is retained and strengthened, not discarded, so no published slug or
  install line changes. Telemetry and provenance remain first-class but sit below
  the funnel. Future designer passes evolve *within* this system; a bolder visual
  rebrand or any change to a published surface still needs its own
  Auditor-endorsed ADR. window → v0.7.

## ADR-026 — MASTER.md adopted: agent contract & orchestration (i218, auditor)
- Status: accepted — operator-directed, landing as a draft PR (the human veto
  window; merge is the operator's ratification, veto by close — ADR-020/025 lane).
- Context: the operator delivered MASTER.md, the consolidation of the external
  strategy thread (repo review → feature ideation → structural gap analysis →
  34-item build plan → two research sweeps → reconciled 2×2, positioning, growth
  playbook). It resolves the three contradictions between its sources: build-vs-buy
  (~9 build / ~10 buy / ~9 halo / ~6 defer — table-stakes are satisfied cheaply,
  never skipped), engineering-vs-launch ("Phase 0 *is* the marketing" — the
  governance story is load-bearing against the AI-slop backlash), and the
  subscription token (fine today; abstract the auth surface now; four hard
  migration triggers). The reframe it lands: the plugins are the deliverable, but
  **the org pattern is the artifact** — an autonomous software company in a repo,
  fork-able via fork-a-foundry. STOP is present (CI token rejected 2026-07-07);
  this is operator-directed work in the i217 lane and runs no shift.
- Decision:
  1. **MASTER.md lands at root as the program's single source of truth** for the
     Stage 0–4 buildout (safe core → proof artifacts → integrate table-stakes →
     launch → build in public). The in-repo brief family and Auditor-owned
     ROADMAP.md gates stand untouched; they audited the marketplace product,
     MASTER.md governs the org-pattern program.
  2. **The §14 agent contract is ratified** (the master doc reserves ADR-026 for
     exactly this): every ops agent gets a manifest under `foundry/agents/`
     (id, role, trigger, trust_tier, quota_tier, capability, outputs, heartbeat);
     the four hard rules (no direct pushes to main — mutations flow through the
     orchestrator once P0.7 lands, run-shift excepted until then; untrusted input
     is fenced before any prompt; writes pass guard + state validator; every agent
     heartbeats and commits under its own identity with an `Agent:` trailer);
     quota tiers shed `low` then `high`, **never `product`**; orchestrator
     precedence: guard veto → product loop → safety/trust → governance → comms.
  3. **Two-iteration rule satisfied for Stage 0 tooling:** this ADR is the
     prior-iteration authorization for the tools/ work §14 Stage 0 specs —
     tools/lib.py manifest loader/registry (P0.1) first; guard.py, orchestrator.py,
     quota.py, fence.py, commit.py, validate_state.py as their items come up.
     Remaining program ADRs keep their planned numbers: 027 constitution & guard ·
     028 quota governor v2 · 029 owner's desk · 030 agent evals.
  4. **Constitution floor pre-ratified as law now** (G8, effective immediately,
     enforced by review until guard.py exists): validator/schema changes stay
     human-ratified always; no agent edits its own governing rule; never auto-open
     PRs against third-party repos.
- Consequences: BACKLOG gains a "Master program" section seeded with 3 items
  (P0.1 agent contract · P0.5 constitution + guard · AUTH-1 auth abstraction —
  the ≤3-new-items law holds; the rest of the program enters from MASTER.md §14
  as slots free). AUTH-1's token-expiry detection directly answers the silent
  failure that caused the 2026-07-07 re-pause. Iterations that pick program items
  follow MASTER.md §10 order and dependencies; one item, one iteration, same bar.

## ADR-031 — program execution mandate & rulings (i219, builder)
- Status: accepted — records the operator's 2026-07-12 directive verbatim in
  effect: *"full approval to merge anything you want as you see fit… build every
  line item in that master document from end to end until 100% complete and
  accounted for."*
- Decision:
  1. **Landing mode for the program:** stage slates as directed PRs (v13/v14
     precedent), per-item iterations/commits/journal entries, self-merged on
     green gates under the operator mandate. state/PROGRAM.md is the ledger
     where every item is accounted for.
  2. **Two-iteration authorization, program-wide:** this ADR is the
     prior-iteration ADR for the tools/, loop.sh, and workflow changes that
     MASTER.md §14 Stages 1–4 spec (Stage 0 was authorized by ADR-026):
     build.py template/metrics work (GAP-A/A2), loop.sh auth sourcing (AUTH-1),
     shipnote/relnotes extensions (P4.2), intake extensions (P2.2, P3.4),
     alarm/diagnostic extensions (P1.3, P0.9), exporter (GAP-C), and
     validator additions **only where MASTER.md names them** (P0.3 trailer
     check, P0.4 state hooks). Any validator/schema change NOT specified in
     MASTER.md still routes to the desk — the constitution floor (ADR-026 §4)
     is unchanged by the mandate.
  3. **§12 open questions ruled** (operator delegated by the mandate):
     Q1 briefing/desk channel = **pinned issue** (zero setup; Telegram can be
     added later without protocol change). Q2 orchestrator landing =
     **direct-to-main with the desk as the gate** for desk-ratified items,
     `mode: pr` kept as a flag for veto-window use. Q3 quota signal = **no
     readable subscription meter exists; estimate from run counts + BUDGET.jsonl
     until the API switch**, with conservative defaults. Q4 = the company is
     already named (Nightshift Foundry, ADR-011); the naming-ceremony assistant
     scopes to plugin names.
  4. **Boundary:** outward actions under the operator's identity — launch
     posts, third-party account signups/app installs, submissions to external
     directories — are prepared to the repo's edge and desk-queued, never
     performed autonomously. Constitution: submissions only, never third-party
     PRs; never simulate the operator.
- Consequences: every later stage builds without per-iteration authorization
  friction; the desk (P0.8) becomes the single approval surface; PROGRAM.md +
  JOURNAL carry the audit trail item by item.
