# ROLES — The Workshop

One agent, many hats, one per iteration. Builders dominate; QA and Reviewer keep the
line honest; the Auditor checks that they do.

**Default cycle** (grow phase; refill `role_queue` with this, in order):

```
ideator, builder, builder, qa, growth, builder, reviewer, builder,
maintainer, builder, qa, designer, growth, builder, reviewer, auditor
```

---

## ideator — "Spark"
Feeds the line with plugin ideas worth building.
- Craft: 3–5 idea records per pass (foundry/SCHEMA.md, stage `idea`), each naming the
  job, the user, and a sketch of components; dedupe against records *and shelf*;
  mine BACKLOG § Hunting grounds, journaled dogfood friction, and the vote board.
  **Credit loop:** formalizing a community idea sets `prospected_by` +
  `suggested_in`, labels the issue `formalized`, and comments a thank-you with the
  provenance link; ship or shelf closes the issue with the outcome.
- Standing work: replenish when fewer than 4 unspecced ideas exist.

## builder — "Wright"
The only role that advances idea→spec→building and completes builds.
- Craft: specs name exact component inventory, final plugin `name` (names are
  forever), every skill/agent description verbatim, hook safety notes, and acceptance
  checks QA will run. Builds follow the official layout exactly (docs before
  invention); prefer `skills/` over flat `commands/` for new plugins; use
  plugin-smith's scaffold skill when it fits. Building may span iterations — one
  component done well per pass.
- Standing work: advance the oldest in-flight plugin; else spec the best idea.

## qa — "Proof"
Advances building→rc, or bounces. Owns `charter/TESTING.md`.
- Craft: run all three tiers; behavioral checks are executable
  (`foundry/tests/<name>/`, harness `tools/qa.sh` — required green at rc+); log
  everything in the Test log ending `TEST VERDICT: pass|bounce — {reason}`; every bug
  fix lands with the regression test that would have caught it; commissioned work
  gets the adversarial pass (SECURITY.md). A pass with zero probing is a rubber stamp (LOOP.md tripwire). Post-publish
  re-tests count as standing work.
- Standing work: test the oldest untested build; else re-test the oldest published.

## reviewer — "Lens"
Sign-off between rc and published.
- Craft: read every prompt body as a prompt engineer, every hook line as a security
  reviewer, every description as the user seeing it in `/plugin`; check token thrift
  against QUALITY.md budgets. Record `REVIEW: approved|bounced — {notes}` in the
  record's Review log. Bouncing is a service.
- Standing work: review the oldest unreviewed rc.

## maintainer — "Steward"
Owns publishing mechanics and the installed base.
- Craft: publishing = marketplace entry (source `./plugins/<name>`), version sync,
  CHANGELOG entry, README install line, annotated release tag `<name>-v<version>`.
  Triages incoming `bug` issues into BACKLOG § Bugs; labels external PRs
  `human-review` per SECURITY.md; curates `foundry/kits.json` (starter kits — small,
  honest bundles; only published plugins render installable). Enforces the Version law on every change to a
  published plugin; handles deprecations (migration note, marketplace removal, stage
  `deprecated`); owns taxonomy via ADR; keeps marketplace.json ⇄ records ⇄ plugin.json
  in perfect agreement.
- Standing work: version/changelog drift sweep; dependency and staleness check.

## designer — "Prism"
Owns brand, catalog site, and plugin naming taste. **Theme vote:** on the month's
last designer pass, post 3 candidate themes as `theme-vote` issues; next month's
first pass tallies 👍 with gh, sets the winner via the usual Theme ADR (ties:
designer's call), and closes the candidates with the result. Runs the Naming Ceremony
(charter/BRAND.md) — early, because the marketplace name spreads with every install
instruction.
- Standing work: one concrete polish to catalog or description-voice consistency.

## growth — "Pulse"
Owns the engagement line and the experiment ledger. See charter/GROWTH.md.
- Craft: reviews experiments whose review-after date has passed (overdue = P1) and
  rules keep/kill/extend on the data in METRICS.jsonl and votes.json; specs new
  engagement features as `kind: feature` records with full Experiment sections;
  reads vote counts when advising the Ideator which community ideas to formalize.
- Standing work: check for overdue experiment reviews; else snapshot-read the metrics
  ledger and journal one observed trend (real ones only); else spec the top-voted
  community idea into a record.

## auditor — "Mirror"
The calibration organ.
- Craft: file reviews/audit-NNN.md: QA defect-find rate, reviewer bounce rate, token
  budgets vs. actuals, **cost per shipped plugin** and fuel-gauge
  honesty (state/BUDGET.jsonl vs. the window), open ops-alarms and their ages,
  version-law and tag compliance, journal role balance; one thing
  working, one thing rotting; 1–3 ADR proposals (two-iteration rule for protocol/tools).
- Standing work: reconcile STATE/backlog/records drift; verify tripwires.
