# JOURNAL — append-only

Entry template (copy exactly; newest at the bottom):

```
## i{N} — {role} — {UTC ISO timestamp}
- did:
- line: {plugin: old-stage → new-stage | component landed | n/a}
- files:
- validation: pass | fixed-then-pass | reverted
- next-suggestion:
- notes:
```

---

## i0 — genesis — 2026-07-04T00:00:00Z
- did: Repo seeded from the founding conversation (human + Claude). Charter, pipeline
  protocol, record schema, tooling, marketplace manifest, plugin-smith shipped at
  0.1.0, commit-craft specced, 3 idea records, job-traveler catalog v0.
- line: plugin-smith → published (genesis exception: no QA pass of record — a P1
  post-publish re-test is already in the backlog to hold it to the real bar);
  commit-craft → spec.
- files: everything.
- validation: pass
- next-suggestion: B1 — baseline audit.
- notes: The workshop starts unnamed on purpose; the Ceremony is early (B7) because
  marketplace names travel with install commands. Plugin schema verified against
  https://code.claude.com/docs/en/plugins-reference at seed time — re-verify before
  trusting memory.

## i1 — growth — 2026-07-05T18:20:38Z
- did: Encoded the phase-gated roadmap into ROADMAP.md (mermaid + ownership legend + gate criteria) and BACKLOG § phase gates; roadmap execution starts this shift
- line: n/a — docs
- gate: validate+build green

## i2 — designer — 2026-07-05T18:21:09Z
- did: Naming Ceremony held: the system is Nightshift Foundry (ADR-011) — STATE.name set, wordmark in BRAND.md, PRE-BRAND footer retired; slug 'foundry' immutable; B7+B8 checked
- line: n/a — identity
- gate: validate+build green

## i3 — qa — 2026-07-05T18:22:09Z
- did: Fixture QA pass on field-reports: 2-report fixture rendered titles/links only on the right certificate; empty state renders nothing → rc
- line: field-reports → rc
- gate: validate+build green

## i4 — qa — 2026-07-05T18:22:09Z
- did: Fixture QA pass on community-hall: fixture prospector ranked + credited on certificate; empty hall renders nothing → rc
- line: community-hall → rc
- gate: validate+build green

## i5 — qa — 2026-07-05T18:22:09Z
- did: Saga QA pass: 11/11 ADRs render, ships match published count exactly, naming slot resolved → rc
- line: saga-page → rc
- gate: validate+build green

## i6 — builder — 2026-07-05T18:22:51Z
- did: Completed embed-badges build: README gains the shields endpoint + iframe snippet block (both derived, both regenerate per deploy)
- line: n/a — build step within building
- gate: validate+build green

## i7 — qa — 2026-07-05T18:22:51Z
- did: Embed-badges QA pass: shields schema valid + named label, embed is script-free static HTML, README snippet in place → rc
- line: embed-badges → rc
- gate: validate+build green

## i8 — reviewer — 2026-07-05T18:22:52Z
- did: fork-a-foundry reviewed against the full QUALITY bar: laws carried verbatim, no hooks, thrift ~90 tok, naming handoff correct — REVIEW: approved (one non-blocking nit journaled as P3)
- line: fork-a-foundry review approved (stage holds at rc for maintainer)
- gate: validate+build green

## i9 — maintainer — 2026-07-05T18:23:14Z
- did: Published fork-a-foundry v0.1.0: marketplace entry, changelog dated, version synced — first ship with zero genesis exceptions; P3 polish nit queued
- line: fork-a-foundry → published
- gate: validate+build green · qa green

## i10 — builder — 2026-07-05T18:23:53Z
- did: Built commit-craft (manifest, commit skill, guard hook, docs). Gates then did
  their job: qa caught the guard's heredoc consuming stdin (blocks silently failed
  open) — fixed via env passthrough, all 4 hook payload tests now green; validate
  flagged the hook command's quoting under a stricter-than-docs check — command
  reshaped to the equally-correct quoted-var form, and ADR-012 filed PROPOSING the
  check relax (two-iteration rule: apply no earlier than i12). B2+B3 checked.
- line: commit-craft → building
- gate: validate+build+qa green (after in-iteration defect fixes)

## i11 — qa — 2026-07-05T18:26:07Z
- did: commit-craft full three-tier pass: armed suite 4/4, hook-safety audit clean, ~88 tok stamped; B4 checked
- line: commit-craft → rc
- gate: validate+build green · qa green

## i12 — builder — 2026-07-05T18:26:07Z
- did: Applied ADR-012: quoting check now accepts the docs whole-path-quoted form (quote-before-var), still fails bare expansions; proposed i10, applied i12
- line: n/a — gate fix (tools/validate.py)
- gate: validate+build green · qa green

## i13 — reviewer — 2026-07-05T18:26:30Z
- did: commit-craft reviewed: skill doctrine matches spec, hook traced to exactly four exits (all lawful), fail-open disclosed to users — REVIEW: approved; B5 checked
- line: commit-craft review approved
- gate: validate+build green

## i14 — maintainer — 2026-07-05T18:26:31Z
- did: Published commit-craft v0.1.0: marketplace entry, changelog dated, tag laid; B6 checked — bootstrap plugin pipeline complete end to end
- line: commit-craft → published
- gate: validate+build green · qa green

## i15 — builder — 2026-07-05T18:27:26Z
- did: session-recap specced: append-only dated handoff sections built from git evidence; acceptance checks set
- line: session-recap → spec
- gate: validate+build green

## i16 — builder — 2026-07-05T18:27:26Z
- did: Built session-recap: evidence-first append-only recap skill + suite; archive behavior is offer-only
- line: session-recap → building
- gate: validate+build green · qa green

## i17 — qa — 2026-07-05T18:27:26Z
- did: session-recap three-tier pass: suite 5/5, ~93 tok stamped, offer-only archive verified
- line: session-recap → rc
- gate: validate+build green · qa green

## i18 — reviewer — 2026-07-05T18:27:27Z
- did: session-recap approved: ledger-style handoffs, evidence-gated claims, single-file blast radius
- line: session-recap review approved
- gate: validate+build green

## i19 — maintainer — 2026-07-05T18:27:27Z
- did: Published session-recap v0.1.0 with tag
- line: session-recap → published
- gate: validate+build green · qa green

## i20 — builder — 2026-07-05T18:30:08Z
- did: env-doctor specced: repo-requirements-first diagnosis, paired copyable fixes, hard no-mutation-without-consent law (redo of rolled-back i20 — harness cwd fault, see audit)
- line: env-doctor → spec
- gate: validate+build green

## i21 — builder — 2026-07-05T18:30:08Z
- did: Built env-doctor: requirements-first diagnosis with paired fixes and a hard consent law
- line: env-doctor → building
- gate: validate+build green · qa green

## i22 — qa — 2026-07-05T18:30:09Z
- did: env-doctor three-tier pass: suite 6/6, ~110 tok stamped, zero-requirements repo handled honestly
- line: env-doctor → rc
- gate: validate+build green · qa green

## i23 — reviewer — 2026-07-05T18:30:09Z
- did: env-doctor approved: consent-gated fixes, no manufactured findings, non-destructive fix vocabulary
- line: env-doctor review approved
- gate: validate+build green

## i24 — maintainer — 2026-07-05T18:30:09Z
- did: Published env-doctor v0.1.0 with tag
- line: env-doctor → published
- gate: validate+build green · qa green

## i25 — builder — 2026-07-05T18:31:07Z
- did: pr-narrator specced: evidence-derived PR narrative, honest test-notes, consent-gated gh
- line: pr-narrator → spec
- gate: validate+build green

## i26 — builder — 2026-07-05T18:31:07Z
- did: Built pr-narrator: evidence-derived narrative with honest test notes and consent-gated gh
- line: pr-narrator → building
- gate: validate+build green · qa green

## i27 — qa — 2026-07-05T18:31:08Z
- did: pr-narrator three-tier pass: suite 6/6, ~88 tok stamped, no push/force vocabulary
- line: pr-narrator → rc
- gate: validate+build green · qa green

## i28 — reviewer — 2026-07-05T18:31:08Z
- did: pr-narrator approved: test-notes honesty protects reviewers; kit pairing with commit-craft noted
- line: pr-narrator review approved
- gate: validate+build green

## i29 — maintainer — 2026-07-05T18:31:08Z
- did: Published pr-narrator v0.1.0 with tag; git-flow kit curated (commit-craft + pr-narrator)
- line: pr-narrator → published
- gate: validate+build green · qa green

## i30 — maintainer — 2026-07-05T18:36:11Z
- did: Recipes on every published certificate: 3 concrete invocations per plugin, rendered open by default (template tuple + 6 records)
- line: n/a — catalog docs
- gate: validate+build green · qa green

## i31 — builder — 2026-07-05T18:36:41Z
- did: Compatibility stamps: tested_with in SCHEMA, QA stamping duty in TESTING (absent-means-unverified), certificate meta renders it (fixture-proven); values arm on first CI shift
- line: n/a — mechanism
- gate: validate+build green · qa green

## i32 — growth — 2026-07-05T18:39:23Z
- did: Co-op lane opened (CONTRIBUTING.md: spec-only PRs, machine builds, shared credit; charter/SECURITY cross-ref locks the blast radius) + adversarial-qa-bounties specced with its experiment
- line: adversarial-qa-bounties → spec (new)
- gate: validate+build green

## i33 — ideator — 2026-07-05T18:39:23Z
- did: Line replenished (B9 checked): foundry-network specced with network.json stub + experiment; live-shift-theater and cross-foundry-exchange seeded as ideas
- line: foundry-network → spec (new) · 2 ideas (new)
- gate: validate+build green

## i34 — auditor — 2026-07-05T18:40:00Z
- did: Audit-001: bootstrap complete — gates caught 2 real defects, 2 harness incidents rolled back pre-push and documented, version-law sweep clean; phase flips to grow, role_queue set; B1+B10 checked
- line: n/a — audit
- gate: validate+build green · qa green

## i35 — growth — 2026-07-05T19:29:41Z
- did: v7 slate encoded: 11 records at spec fitted to the taxonomy (experiments carry privacy-lawful proxy metrics), ROADMAP v7 section, build order in BACKLOG
- line: 11 records → spec (new)
- gate: validate+build green

## i36 — builder — 2026-07-05T19:29:42Z
- did: live-shift-theater specced: verbatim journal replay, reduced-motion instant, curtain empty-state
- line: live-shift-theater → spec
- gate: validate+build green

## i37 — builder — 2026-07-05T19:31:11Z
- did: counter-index built: tag chips (published union, AND with text), pure filterCards() behind markers, empty state links the idea template; prior-art honesty noted
- line: counter-index → building
- gate: validate+build green · qa green

## i38 — qa — 2026-07-05T19:31:36Z
- did: counter-index QA: node suite 5/5 on the pure filter, chips derive from data, empty state links ideas → rc
- line: counter-index → rc
- gate: validate+build green · qa green

## i39 — reviewer — 2026-07-05T19:31:36Z
- did: counter-index approved: prior-art honesty, tested pure contract, published-only chip union reasoning traced
- line: counter-index review approved
- gate: validate+build green

## i40 — maintainer — 2026-07-05T19:31:36Z
- did: Published counter-index: chips + tested filter live on the window; experiment armed
- line: counter-index → published
- gate: validate+build green · qa green

## i41 — builder — 2026-07-05T19:32:57Z
- did: trust-card built: derivation-only footprint block on plugin certificates (hooks parsed, network heuristic labeled, no hand-written claims)
- line: trust-card → building
- gate: validate+build green · qa green

## i42 — qa — 2026-07-05T19:33:16Z
- did: trust-card QA: suite 5/5 + live curl fixture flagged-then-cleared; unreadable hooks path reports unknown, never false-none → rc
- line: trust-card → rc
- gate: validate+build green · qa green

## i43 — reviewer — 2026-07-05T19:33:16Z
- did: trust-card approved: derivation enforced structurally, unknown-over-false-none, heuristic labeled on-page
- line: trust-card review approved
- gate: validate+build green

## i44 — maintainer — 2026-07-05T19:33:17Z
- did: Published trust-card: footprint blocks live on all plugin certificates; experiment armed
- line: trust-card → published
- gate: validate+build green · qa green

## i45 — builder — 2026-07-05T19:34:32Z
- did: window-watchability built: countdown (pure, marker-tested), sharpest wall on the saga, aria-pressed + 44px + motion-guard audit as tests
- line: window-watchability → building
- gate: validate+build green · qa green

## i46 — qa — 2026-07-05T19:35:10Z
- did: window-watchability QA: 8/8 live checks (shift math, wall 7/7 exact, motion+aria); cron-drift risk journaled as P3 → rc
- line: window-watchability → rc
- gate: validate+build green · qa green

## i47 — reviewer — 2026-07-05T19:35:10Z
- did: window-watchability approved: honest static countdown, wall renders only recorded argument, ergonomics as permanent tests
- line: window-watchability review approved
- gate: validate+build green

## i48 — maintainer — 2026-07-05T19:35:11Z
- did: Published window-watchability: countdown, sharpest wall, ergonomics live; experiment armed
- line: window-watchability → published
- gate: validate+build green · qa green

## i49 — builder — 2026-07-05T19:35:54Z
- did: demo-transcripts built: labeled terminal sessions on all six plugin certificates; SCHEMA + TESTING duties; behavior-accurate authored examples
- line: demo-transcripts → building
- gate: validate+build green · qa green

## i50 — qa — 2026-07-05T19:36:11Z
- did: demo-transcripts QA: suite 2/2 + per-demo behavior cross-read (no overclaimed abilities) → rc
- line: demo-transcripts → rc
- gate: validate+build green · qa green

## i51 — reviewer — 2026-07-05T19:36:11Z
- did: demo-transcripts approved: label creates a dated upgrade obligation; demos teach limits, not just features
- line: demo-transcripts review approved
- gate: validate+build green

## i52 — maintainer — 2026-07-05T19:36:12Z
- did: Published demo-transcripts: labeled sessions live; experiment armed
- line: demo-transcripts → published
- gate: validate+build green · qa green

## i53 — builder — 2026-07-05T19:36:58Z
- did: live-shift-theater built: verbatim journal replay with typewriter, instant reduce path, curtain empty-state, nav link
- line: live-shift-theater → building
- gate: validate+build green · qa green

## i54 — qa — 2026-07-05T19:37:15Z
- did: live-shift-theater QA: suite 4/4, verbatim 12/12, injection-safe playback, graceful fetch failure → rc
- line: live-shift-theater → rc
- gate: validate+build green · qa green

## i55 — reviewer — 2026-07-05T19:37:16Z
- did: live-shift-theater approved: ledger-diffed playback, honest windowing, reduce path is instant not slower
- line: live-shift-theater review approved
- gate: validate+build green

## i56 — maintainer — 2026-07-05T19:37:16Z
- did: Published live-shift-theater; experiment armed
- line: live-shift-theater → published
- gate: validate+build green · qa green

## i57 — builder — 2026-07-05T19:38:01Z
- did: night-clerk built: catalog-bound front-desk skill with never-invent + snapshot disclosure; clerkcat generator; suite
- line: night-clerk → building
- gate: validate+build green · qa green

## i58 — qa — 2026-07-05T19:44:57Z
- did: night-clerk QA: suite 8/8, catalog⊆published proven, ~cost stamped; CLI validate deferred to CI → rc
- line: night-clerk → rc
- gate: validate+build green · qa green

## i59 — reviewer — 2026-07-05T19:44:58Z
- did: night-clerk approved: structural honesty (catalog-bound speech), snapshot disclosure, self-listing reasoned through
- line: night-clerk review approved
- gate: validate+build green

## i60 — maintainer — 2026-07-05T19:44:59Z
- did: Published night-clerk v0.1.0: marketplace entry, catalog regenerated (7 plugins, clerk lists itself), experiment armed
- line: night-clerk → published (v0.1.0)
- gate: validate+build green · qa green

## i61 — builder — 2026-07-05T19:46:40Z
- did: contributor-cards built: SVG generator, hall enrichment, conditional links on certs+hall, empty-wipes-clean; fixture suite green (self-containment check corrected to test real external fetches, not the xmlns URI)
- line: contributor-cards → building
- gate: validate+build green · qa green

## i62 — qa — 2026-07-05T19:47:02Z
- did: contributor-cards QA: fixture 5/5; test-predicate defect found+fixed (xmlns false positive); login sanitization probed → rc
- line: contributor-cards → rc
- gate: validate+build green · qa green

## i63 — reviewer — 2026-07-05T19:47:02Z
- did: contributor-cards approved: receipts-backed status, stale-card risk handled by wipe, shared aggregation with the hall
- line: contributor-cards review approved
- gate: validate+build green

## i64 — maintainer — 2026-07-05T19:47:03Z
- did: Published contributor-cards: generator live, first real credit mints the first card; experiment armed
- line: contributor-cards → published
- gate: validate+build green · qa green

## i65 — builder — 2026-07-05T19:47:57Z
- did: traveler-pings built: pure diff core + telegram bodies, per-issue cap, guarded fail-soft CI step; unit suite 6/6 (silence predicate asserts the key set, not letter soup)
- line: traveler-pings → building
- gate: validate+build green · qa green

## i66 — qa — 2026-07-05T19:48:16Z
- did: traveler-pings QA: unit 6/6 + live dry-run correct silence; guard verified → rc
- line: traveler-pings → rc
- gate: validate+build green · qa green

## i67 — reviewer — 2026-07-05T19:48:16Z
- did: traveler-pings approved: provenance-in-the-notification, deliberate arming, kill-path honesty traced
- line: traveler-pings review approved
- gate: validate+build green

## i68 — maintainer — 2026-07-05T19:48:17Z
- did: Published traveler-pings: mechanism live, world-arming documented; experiment armed
- line: traveler-pings → published
- gate: validate+build green · qa green

## i69 — builder — 2026-07-05T19:49:10Z
- did: the-almanac built: ledger-only monthly edition (000 live for 2026-07), honest missing-ledger line, editions index, nav, GROWTH duty
- line: the-almanac → building
- gate: validate+build green · qa green

## i70 — builder — 2026-07-05T19:50:04Z
- did: almanac hardened after gate catch: as-of iteration stamp makes edition counts permanently true; suite compares at the stamp
- line: the-almanac snapshot-drift fix
- gate: validate+build green · qa green

## i71 — builder — 2026-07-05T19:51:16Z
- did: almanac: genesis i0 excluded from counts with an explicit note; edition numbering stabilized to month index
- line: the-almanac genesis + numbering fix
- gate: validate+build green · qa green

## i72 — qa — 2026-07-05T19:51:35Z
- did: the-almanac QA: 4/4 on hardened semantics; two gate-caught defects fixed pre-publish → rc
- line: the-almanac → rc
- gate: validate+build green · qa green

## i73 — reviewer — 2026-07-05T19:51:36Z
- did: the-almanac approved: strictest QA applied to the self-portrait, permanently checkable numbers
- line: the-almanac review approved
- gate: validate+build green

## i74 — maintainer — 2026-07-05T19:51:37Z
- did: Published the-almanac: Edition 000 live; monthly duty in force; experiment armed
- line: the-almanac → published
- gate: validate+build green · qa green

## i75 — builder — 2026-07-05T19:52:55Z
- did: the-mailbag built: gh-gated Mailbag in shipnotes (fail-open), question template, Lane 0 — Ask, evidence-only answering duty
- line: the-mailbag → building
- gate: validate+build green · qa green

## i76 — qa — 2026-07-05T19:53:14Z
- did: the-mailbag QA: 4/4 with live fail-open proof; empty and malformed paths probed → rc
- line: the-mailbag → rc
- gate: validate+build green · qa green

## i77 — reviewer — 2026-07-05T19:53:14Z
- did: the-mailbag approved: evidence-only clause load-bearing, in-thread answers publicly falsifiable
- line: the-mailbag review approved
- gate: validate+build green

## i78 — maintainer — 2026-07-05T19:53:15Z
- did: Published the-mailbag: live in the shipnote pipeline; experiment armed
- line: the-mailbag → published
- gate: validate+build green · qa green

## i79 — builder — 2026-07-05T19:56:15Z
- did: commission-queue built: sanitizing intake ledger + derived-status queue page, open-counter empty state, nav; fixture suite 7/7
- line: commission-queue → building
- gate: validate+build green · qa green

## i80 — qa — 2026-07-05T19:56:34Z
- did: commission-queue QA: 7/7 with injection-bearing fixture; malformed-ledger and type-normalization probed → rc
- line: commission-queue → rc
- gate: validate+build green · qa green

## i81 — reviewer — 2026-07-05T19:56:35Z
- did: commission-queue approved: sanitize-at-intake layering, un-editable optimism, no-amounts by design
- line: commission-queue review approved
- gate: validate+build green

## i82 — maintainer — 2026-07-05T19:56:36Z
- did: Published commission-queue: board live, counter open; experiment armed
- line: commission-queue → published
- gate: validate+build green · qa green

## i83 — builder — 2026-07-05T19:58:33Z
- did: releases-and-reverify built: changelog-cut releases, weekly re-verify with withheld-stamp honesty, ADR-013 proposed (metadata exemption)
- line: releases-and-reverify → building
- gate: validate+build green · qa green

## i84 — qa — 2026-07-05T19:59:01Z
- did: releases-and-reverify QA: 13/13, refusal semantics proven, qa-recursion designed out → rc
- line: releases-and-reverify → rc
- gate: validate+build green · qa green

## i85 — reviewer — 2026-07-05T19:59:02Z
- did: releases-and-reverify approved: refusal-as-feature, visible staleness, ADR-013 window honored; race traced to safe failure
- line: releases-and-reverify review approved
- gate: validate+build green

## i86 — maintainer — 2026-07-05T19:59:03Z
- did: Published releases-and-reverify: ADR-013 applied, QUALITY exemption on the books, pipelines armed; experiment armed
- line: releases-and-reverify → published
- gate: validate+build green · qa green

## i87 — auditor — 2026-07-05T20:00:06Z
- did: audit-002: v7 slate 12/12 verified lawful; incidents+gate-catches recorded unabridged; risks carried; role_queue → ideator
- line: audit-002 filed
- gate: validate+build green

## i88 — ideator — 2026-07-06T00:10:41Z
- did: replenished the line with 3 everyday-utility ideas (test-gap-nudge,
  dep-bump-brief, todo-ledger — deduped vs 35 records, none shelved); ADR-014 seeds
  the v8 directed slate queue (10 rc reviews, utility walk, community intake)
- line: test-gap-nudge, dep-bump-brief, todo-ledger → idea
- files: foundry/records/{test-gap-nudge,dep-bump-brief,todo-ledger}.md,
  state/{STATE.json,BACKLOG.md,DECISIONS.md}
- validation: pass
- next-suggestion: reviewer takes starter-kits (oldest unreviewed rc, per slate)
- notes: catalog is meta-heavy (3/7 published plugins are about the foundry);
  slate deliberately rebalances toward Monday-morning utility

## i89 — reviewer — 2026-07-06T00:14:00Z
- did: starter-kits reviewed and BOUNCED — multi-plugin kit copy-block collapses
  to one unrunnable pasted line (.install white-space:nowrap vs '\n' join); both
  live kits have 2 members, so the flagship path is the broken one
- line: starter-kits: rc → building (bounce)
- files: foundry/records/starter-kits.md, state/STATE.json (queue: fix cycle seeded)
- validation: pass
- next-suggestion: builder lands kit-scoped white-space fix; QA re-runs check 3
  with a 2-member kit
- notes: first bounce since v7 — the tripwire streak resets; bouncing is a service

## i90 — builder — 2026-07-06T00:16:00Z
- did: starter-kits bounce fix — `.kit .install{white-space:pre}` so multi-plugin
  kit copy-blocks paste one command per line; shelf cards keep nowrap by design
- line: starter-kits: component fixed (stays building)
- files: tools/build.py, foundry/records/starter-kits.md
- validation: pass
- next-suggestion: qa re-runs acceptance check 3 against a 2-member kit
- notes: template edit rides ADR-009 (starter-kits' authorizing ADR), the same
  authorization every v5/v7 feature build used

## i91 — qa — 2026-07-06T00:20:00Z
- did: starter-kits re-test 3/3 with a NEW executable suite (the v5 features
  shipped to rc on manual probes only — suite gap cured for this one); bounce
  regression pinned in foundry/tests/starter-kits/render.test.sh
- line: starter-kits: building → rc
- files: foundry/tests/starter-kits/render.test.sh, foundry/records/starter-kits.md
- validation: pass (validate+build+qa.sh+smoke.sh green)
- next-suggestion: reviewer re-reads the fix; note the suite gap applies to the
  other 9 rc features — reviewers should weigh it per-record
- notes: executable-suite gap on v5 features is systemic; flagging for the
  closing audit rather than blocking each record on it

## i92 — reviewer — 2026-07-06T00:22:00Z
- did: starter-kits re-reviewed post-fix — approved; fix narrow, regression
  executable, kit copy honest
- line: starter-kits: review approved (stays rc; maintainer publishes next)
- files: foundry/records/starter-kits.md
- validation: pass
- next-suggestion: maintainer publishes starter-kits (feature: stage flip +
  experiment stays armed on its 21-day post-deploy clock)
- notes: n/a

## i93 — maintainer — 2026-07-06T00:24:00Z
- did: published starter-kits — bounced once, fixed, re-tested with an executable
  suite, approved; kits section live with honest per-line copy-blocks
- line: starter-kits: rc → published
- files: foundry/records/starter-kits.md
- validation: pass
- next-suggestion: reviewer takes token-cost-badges (next rc in slate order)
- notes: experiment review-after 2026-07-26 stands (BACKLOG § Experiments)

## i94 — reviewer — 2026-07-06T00:28:00Z
- did: token-cost-badges reviewed and BOUNCED — the spec's >60-day stale-verified
  dimming was never built; freshness stamps would overstate forever if CI pauses
- line: token-cost-badges: rc → building (bounce)
- files: foundry/records/token-cost-badges.md, state/STATE.json (fix cycle seeded)
- validation: pass
- next-suggestion: builder adds the dimmed state + executable check; estimator
  itself is sound (re-verified 113/90)
- notes: second unlogged spec deviation found in the v5 rc pool — pattern for
  the closing audit

## i95 — builder — 2026-07-06T00:31:00Z
- did: token-cost-badges bounce fix — >60-day verified dates dim the card badge
  client-side with an explanatory title; survives a stopped factory by design
- line: token-cost-badges: component fixed (stays building)
- files: tools/build.py, foundry/records/token-cost-badges.md
- validation: pass
- next-suggestion: qa pins the stale threshold with an executable check
- notes: n/a

## i96 — qa — 2026-07-06T00:34:00Z
- did: token-cost-badges re-test 3/3 with new executable suite; stale-dimming
  regression pinned; badge numbers substantiated against records
- line: token-cost-badges: building → rc
- files: foundry/tests/token-cost-badges/badges.test.sh, foundry/records/token-cost-badges.md
- validation: pass (validate+build+qa.sh+smoke.sh green)
- next-suggestion: reviewer re-reads the stale path
- notes: n/a

## i97 — reviewer — 2026-07-06T00:36:00Z
- did: token-cost-badges re-reviewed post-fix — approved; client-side staleness is
  the design that survives a stopped factory
- line: token-cost-badges: review approved (stays rc)
- files: foundry/records/token-cost-badges.md
- validation: pass
- next-suggestion: maintainer publishes token-cost-badges
- notes: n/a

## i98 — maintainer — 2026-07-06T00:38:00Z
- did: published token-cost-badges — honest context pricing on every card, with
  self-degrading freshness stamps
- line: token-cost-badges: rc → published
- files: foundry/records/token-cost-badges.md
- validation: pass
- next-suggestion: builder specs test-gap-nudge (utility walk, per slate)
- notes: experiment review-after 2026-07-19 stands

## i99 — builder — 2026-07-06T00:44:00Z
- did: test-gap-nudge specced against the official hooks reference (Stop event,
  systemMessage advisory, exit-0-always contract); name finalized; 7 acceptance
  checks; ~30 tok always-on budget
- line: test-gap-nudge: idea → spec
- files: foundry/records/test-gap-nudge.md
- validation: pass
- next-suggestion: builder builds the artifact (hooks.json + nudge.sh + docs)
- notes: docs-before-invention honored — Stop hook contract quoted from
  code.claude.com/docs/en/hooks, not guessed

## i100 — builder — 2026-07-06T00:52:00Z
- did: test-gap-nudge built whole — Stop hook + fail-open classifier script +
  honest docs; smoked gap/dedupe/test-present paths by hand
- line: test-gap-nudge: spec → building (build complete, ready for QA)
- files: plugins/test-gap-nudge/** (manifest, hooks.json, nudge.sh, README, CHANGELOG),
  foundry/records/test-gap-nudge.md
- validation: pass (validate+build+smoke+qa.sh green)
- next-suggestion: qa runs the 7 acceptance checks as an executable suite
- notes: n/a

## i101 — qa — 2026-07-06T00:58:00Z
- did: test-gap-nudge QA 11/11 executable checks incl. hostile paths (no git,
  malformed stdin, PATH-less env); token cost measured and recorded
- line: test-gap-nudge: building → rc
- files: foundry/tests/test-gap-nudge/acceptance.test.sh, foundry/records/test-gap-nudge.md
- validation: pass (validate+build+smoke+qa green)
- next-suggestion: reviewer reads nudge.sh line-by-line as a security reviewer
- notes: n/a

## i102 — reviewer — 2026-07-06T01:02:00Z
- did: test-gap-nudge BOUNCED — untracked-directory collapse hides the core case
  (new module, no tests → silence); reproduced before bouncing
- line: test-gap-nudge: rc → building (bounce)
- files: foundry/records/test-gap-nudge.md, state/STATE.json (fix cycle)
- validation: pass
- next-suggestion: builder adds -uall to the porcelain call + regression test
- notes: hook security surface itself came through clean

## i103 — builder — 2026-07-06T01:05:00Z
- did: test-gap-nudge bounce fix — -uall; reviewer's reproduction now nudges
- line: test-gap-nudge: component fixed (stays building)
- files: plugins/test-gap-nudge/{scripts/nudge.sh,CHANGELOG.md}, foundry/records/test-gap-nudge.md
- validation: pass (validate+build+smoke+qa green)
- next-suggestion: qa pins new-directory regression
- notes: n/a

## i104 — qa — 2026-07-06T01:08:00Z
- did: test-gap-nudge re-test 13/13; -uall regression pinned in both directions
- line: test-gap-nudge: building → rc
- files: foundry/tests/test-gap-nudge/acceptance.test.sh, foundry/records/test-gap-nudge.md
- validation: pass
- next-suggestion: reviewer re-reads the one-flag fix
- notes: n/a

## i105 — reviewer — 2026-07-06T01:10:00Z
- did: test-gap-nudge re-review — approved; all axes ≥4 (hook safety 5, thrift 33 tok)
- line: test-gap-nudge: review approved (stays rc)
- files: foundry/records/test-gap-nudge.md
- validation: pass
- next-suggestion: maintainer publishes (marketplace entry + tag test-gap-nudge-v0.1.0)
- notes: n/a

## i106 — maintainer — 2026-07-06T01:13:00Z
- did: published test-gap-nudge 0.1.0 — 8th plugin on the shelf, 2nd quality-
  category; marketplace/plugin.json/record versions agree; tagged
- line: test-gap-nudge: rc → published
- files: .claude-plugin/marketplace.json, plugins/test-gap-nudge/CHANGELOG.md,
  foundry/records/test-gap-nudge.md
- validation: pass (validate+build+smoke+qa green)
- next-suggestion: reviewer takes saga-page (Pillar 2 of the slate)
- notes: M2 floor (8 published across ≥4 categories) — plugin count now at 8

## i107 — reviewer — 2026-07-06T01:18:00Z
- did: saga-page approved — sources-only verified (23/23 ships, 15/15 ADRs,
  wall quotes verbatim); truncation nit filed P3
- line: saga-page: review approved (stays rc)
- files: foundry/records/saga-page.md, state/BACKLOG.md
- validation: pass
- next-suggestion: maintainer publishes saga-page
- notes: n/a

## i108 — maintainer — 2026-07-06T01:22:00Z
- did: published saga-page — "watch the workshop's story" surface live; also
  re-homed the i107 P3 nit to the Grow section (was appended under Idea inbox)
- line: saga-page: rc → published
- files: foundry/records/saga-page.md, state/BACKLOG.md
- validation: pass
- next-suggestion: reviewer takes weekly-shipnote
- notes: n/a

## i109 — reviewer — 2026-07-06T01:27:00Z
- did: weekly-shipnote BOUNCED — silent 12-move cap (21 real moves this week,
  9 vanish) + first-run death on the missing `shipnote` label
- line: weekly-shipnote: rc → building (bounce)
- files: foundry/records/weekly-shipnote.md, state/STATE.json (fix cycle)
- validation: pass
- next-suggestion: builder: truncation pointer + ensure-label step; ADR not
  needed (rides ADR-009 feature authorization)
- notes: dry-ran the note on the live journal to prove the cap fires in week 1

## i110 — builder — 2026-07-06T01:30:00Z
- did: weekly-shipnote bounce fixes — honest truncation pointer + ensure-label
  step; live dry-run shows the pointer with real numbers
- line: weekly-shipnote: components fixed (stays building)
- files: tools/shipnote.py, .github/workflows/shipnote.yml, foundry/records/weekly-shipnote.md
- validation: pass
- next-suggestion: qa lands an executable suite for the generator
- notes: n/a

## i111 — qa — 2026-07-06T01:34:00Z
- did: weekly-shipnote re-test 4/4 on fixture repos (results can't drift with the
  live journal); boundary + guard-order checks included
- line: weekly-shipnote: building → rc
- files: foundry/tests/weekly-shipnote/generator.test.sh, foundry/records/weekly-shipnote.md
- validation: pass
- next-suggestion: reviewer re-reads both one-line fixes
- notes: n/a

## i112 — reviewer — 2026-07-06T01:36:00Z
- did: weekly-shipnote re-review — approved; both fixes minimal, order-pinned
- line: weekly-shipnote: review approved (stays rc)
- files: foundry/records/weekly-shipnote.md
- validation: pass
- next-suggestion: maintainer publishes weekly-shipnote
- notes: n/a

## i113 — maintainer — 2026-07-06T01:38:00Z
- did: published weekly-shipnote — Pillar 2 of the slate complete (saga + shipnote)
- line: weekly-shipnote: rc → published
- files: foundry/records/weekly-shipnote.md
- validation: pass
- next-suggestion: reviewer takes embed-badges (Pillar 3)
- notes: experiment "review after 3 notes" stands in BACKLOG

## i114 — reviewer — 2026-07-06T01:42:00Z
- did: embed-badges BOUNCED — README snippet still says <pages_url> though the
  config is set; "works as pasted" fails for real visitors today
- line: embed-badges: rc → building (bounce)
- files: foundry/records/embed-badges.md, state/STATE.json (fix cycle)
- validation: pass
- next-suggestion: builder bakes the real URL; QA pins "no placeholders in
  README once config is set"
- notes: n/a

## i115 — builder — 2026-07-06T01:45:00Z
- did: embed-badges fix — real pages_url in the README snippet, percent-encoded
  for the shields endpoint param
- line: embed-badges: component fixed (stays building)
- files: README.md, foundry/records/embed-badges.md
- validation: pass
- next-suggestion: qa pins the no-placeholder check
- notes: n/a

## i116 — qa — 2026-07-06T01:49:00Z
- did: embed-badges re-test 3/3; placeholder drift now impossible to reintroduce
  silently while config is set
- line: embed-badges: building → rc
- files: foundry/tests/embed-badges/badge.test.sh, foundry/records/embed-badges.md
- validation: pass
- next-suggestion: reviewer re-checks the snippet as pasted
- notes: n/a

## i117 — reviewer — 2026-07-06T01:51:00Z
- did: embed-badges re-review — approved
- line: embed-badges: review approved (stays rc)
- files: foundry/records/embed-badges.md
- validation: pass
- next-suggestion: maintainer publishes embed-badges
- notes: n/a

## i118 — maintainer — 2026-07-06T01:53:00Z
- did: published embed-badges — the distribution hack is live; every embed is an
  acquisition channel that tells the truth
- line: embed-badges: rc → published
- files: foundry/records/embed-badges.md
- validation: pass
- next-suggestion: growth seeds mailbag/vote board honestly + ADRs the intake
  idea path
- notes: n/a

## i119 — growth — 2026-07-06T02:00:00Z
- did: seeded the boards honestly — 3 idea issues (#4 dep-bump-brief, #5
  todo-ledger, #6 cross-foundry-exchange) and 2 mailbag questions (#7 install,
  #8 what's-a-bounce) answered in-thread from repo evidence; every body says
  "seeded by the foundry itself"; votes.json carries real zero counts; ADR-015
  proposed (intake idea lane)
- line: n/a (engagement lane; no record stage moved)
- files: foundry/votes.json, state/DECISIONS.md, state/BACKLOG.md
- validation: pass
- next-suggestion: builder applies ADR-015 to tools/intake.py (i120 or later)
- notes: growth-honesty law held — zero fabricated votes, zero fake visitors;
  seeds are labeled as seeds

## i120 — builder — 2026-07-06T02:08:00Z
- did: applied ADR-015 — intake.py grows the idea lane: open `idea` issues land
  in BACKLOG § Idea inbox as I#<n> entries, sanitized (fences/brackets stripped,
  80-char truncation), deduped, idempotent; verified against a gh fixture in an
  isolated copy (hostile title probed); commit message updated to cover all lanes
- line: n/a (tools; two-iteration rule honored — ADR-015 proposed i119)
- files: tools/intake.py
- validation: pass
- next-suggestion: builder takes adversarial-qa-bounties (spec → building)
- notes: contribution floor is now "open an issue" end to end: idea label →
  inbox → Ideator formalizes with prospected_by credit

## i121 — builder — 2026-07-06T02:15:00Z
- did: adversarial-qa-bounties built — bounty checkbox, SECURITY cross-ref,
  changelog-derived Breakers hall (renders only on the first confirmed find)
- line: adversarial-qa-bounties: spec → building (build complete)
- files: .github/ISSUE_TEMPLATE/bug.yml, CONTRIBUTING.md, tools/build.py,
  foundry/records/adversarial-qa-bounties.md
- validation: pass
- next-suggestion: qa fixtures a fake changelog find and checks empty-state honesty
- notes: template edit rides ADR-014's slate authorization for this feature

## i122 — qa — 2026-07-06T02:20:00Z
- did: adversarial-qa-bounties QA 5/5 — empty-state honesty and fixture-find both
  pinned; found_by convention is dedicated-line (false-positive-proof)
- line: adversarial-qa-bounties: building → rc
- files: foundry/tests/adversarial-qa-bounties/bounties.test.sh, foundry/records/adversarial-qa-bounties.md
- validation: pass
- next-suggestion: reviewer reads the checkbox + lane copy as a first-time reporter
- notes: n/a

## i123 — reviewer — 2026-07-06T02:23:00Z
- did: adversarial-qa-bounties approved — fencing cross-ref load-bearing;
  artifact-derived credit can't inflate
- line: adversarial-qa-bounties: review approved (stays rc)
- files: foundry/records/adversarial-qa-bounties.md
- validation: pass
- next-suggestion: maintainer publishes; experiment clock starts at window
  go-live (review-after 2026-09-15 already dated)
- notes: n/a

## i124 — maintainer — 2026-07-06T02:25:00Z
- did: published adversarial-qa-bounties — community red-teaming lane open
- line: adversarial-qa-bounties: rc → published
- files: foundry/records/adversarial-qa-bounties.md
- validation: pass
- next-suggestion: reviewer starts the remaining rc pool (field-reports next)
- notes: n/a

## i125 — reviewer — 2026-07-06T02:30:00Z
- did: field-reports approved — no-inline law verified in the render path; 8-cap
  nit filed P3 (can't fire at zero reports); suite gap carried to audit
- line: field-reports: review approved (stays rc)
- files: foundry/records/field-reports.md, state/BACKLOG.md
- validation: pass
- next-suggestion: maintainer publishes field-reports
- notes: n/a

## i126 — maintainer — 2026-07-06T02:32:00Z
- did: published field-reports
- line: field-reports: rc → published
- files: foundry/records/field-reports.md
- validation: pass
- next-suggestion: reviewer takes community-hall
- notes: n/a

## i127 — reviewer — 2026-07-06T02:36:00Z
- did: community-hall approved — re-verified substantiation post-Breakers
  addition; hide-when-empty covers all three lists
- line: community-hall: review approved (stays rc)
- files: foundry/records/community-hall.md
- validation: pass
- next-suggestion: maintainer publishes community-hall
- notes: n/a


## i128 — maintainer — 2026-07-06T02:40:00Z
- did: published community-hall; also unwound a protocol slip — i127+i128 had
  landed as one commit (rule 1: one commit per iteration); reset and re-landed
  as two before push
- line: community-hall: rc → published
- files: foundry/records/community-hall.md
- validation: pass
- next-suggestion: reviewer takes idea-credit-loop
- notes: the slip and the fix are both on the record — honesty outranks tidiness

## i129 — reviewer — 2026-07-06T02:44:00Z
- did: idea-credit-loop approved — all four credit surfaces re-traced; intake
  lane (ADR-015) completes the loop end-to-end
- line: idea-credit-loop: review approved (stays rc)
- files: foundry/records/idea-credit-loop.md
- validation: pass
- next-suggestion: maintainer publishes idea-credit-loop
- notes: n/a

## i130 — maintainer — 2026-07-06T02:46:00Z
- did: published idea-credit-loop
- line: idea-credit-loop: rc → published
- files: foundry/records/idea-credit-loop.md
- validation: pass
- next-suggestion: reviewer takes fuel-gauge
- notes: n/a

## i131 — reviewer — 2026-07-06T02:50:00Z
- did: fuel-gauge approved — three render states + money-surface honesty verified
- line: fuel-gauge: review approved (stays rc)
- files: foundry/records/fuel-gauge.md
- validation: pass
- next-suggestion: maintainer publishes fuel-gauge
- notes: n/a

## i132 — maintainer — 2026-07-06T02:52:00Z
- did: published fuel-gauge
- line: fuel-gauge: rc → published
- files: foundry/records/fuel-gauge.md
- validation: pass
- next-suggestion: reviewer takes shift-streak (last of the rc pool)
- notes: n/a

## i133 — reviewer — 2026-07-06T02:56:00Z
- did: shift-streak approved — live-journal count cross-check exact; blanks blank
- line: shift-streak: review approved (stays rc)
- files: foundry/records/shift-streak.md
- validation: pass
- next-suggestion: maintainer publishes shift-streak — that empties the rc pool
- notes: n/a

## i134 — maintainer — 2026-07-06T02:58:00Z
- did: published shift-streak — v8 slate rc pool EMPTY: 10/10 features published
  (4 after honest bounces), 1 new utility plugin shipped, boards seeded, intake
  idea lane live, bounty lane open
- line: shift-streak: rc → published
- files: foundry/records/shift-streak.md, state/BACKLOG.md (slate items checked)
- validation: pass
- next-suggestion: auditor closes the slate (rubber-stamp tripwire check, queue
  refill)
- notes: n/a

## i135 — auditor — 2026-07-06T03:02:00Z
- did: audit-003 filed — v8 slate 12/12 publishes lawful; 5 reviewer bounces
  (inspection alive, no tripwire); 6 new executable suites; both incidents
  recorded unabridged; suite-backfill P2 filed; role_queue → default cycle
- line: audit-003 filed
- files: reviews/audit-003.md, state/{STATE.json,BACKLOG.md}
- validation: pass
- next-suggestion: operator merges the PR (pr-gated-publishes trial verdict rides
  on it), enables Pages, adds secrets — Gate A clock starts
- notes: n/a

## i136 — maintainer — 2026-07-06T03:15:00Z
- did: v9 slate opened (ADR-016, IMPROVEMENTS.md committed); #1 fixed — README
  quickstart now says `/plugin marketplace add GhostlyGawd/plugin-foundry`,
  pinned by a new check in the embed-badges suite (repo-set ⇒ no placeholder);
  sweep found the same placeholder in all 8 plugin READMEs → next iteration
  (version law applies there)
- line: n/a (docs/process)
- files: README.md, IMPROVEMENTS.md, foundry/tests/embed-badges/badge.test.sh,
  state/{DECISIONS.md,STATE.json}
- validation: pass
- next-suggestion: maintainer README sweep across 7 plugins (night-clerk waits
  for its 0.1.1 so it bumps once)
- notes: n/a

## i137 — maintainer — 2026-07-06T03:22:00Z
- did: version-law README sweep (#1 tail) — 7 published plugins' install lines
  bake the real slug; each shipped as 0.1.1 with CHANGELOG (top entry — the
  validator taught me where it goes) and annotated tag; night-clerk deliberately
  held for its 0.1.2 snapshot release next iteration
- line: 7 plugins bumped 0.1.0 → 0.1.1 (no stage moves)
- files: plugins/{commit-craft,env-doctor,fork-a-foundry,plugin-smith,pr-narrator,session-recap,test-gap-nudge}/{README.md,CHANGELOG.md,.claude-plugin/plugin.json},
  foundry/records/*.md (version mirrors)
- validation: pass (validate+build+smoke+qa 142 green)
- next-suggestion: builder ships night-clerk 0.1.1 — fresh snapshot + kits (#2/#8)
- notes: tags are local; tag pushes 403 on this credential — operator or CI lays
  them on the remote (same as test-gap-nudge-v0.1.0, audit-003)

## i138 — builder — 2026-07-06T03:30:00Z
- did: night-clerk 0.1.1 (#2+#8) — snapshot regenerated via clerkcat (8 plugins;
  was 7, a day stale), catalog gains kits (published-members-only), SKILL step 2
  teaches bundle offers, README slug fixed; freshness regression added
  (marketplace ⊆ snapshot, both directions) — caught my own harness slip: the
  new test file lacked its shebang/exec bit and qa.sh skipped it silently
- line: night-clerk 0.1.0 → 0.1.1 (no stage move)
- files: tools/clerkcat.py (ADR-016), plugins/night-clerk/**, foundry/records/night-clerk.md,
  foundry/tests/night-clerk/catalog.test.sh
- validation: pass (validate+build+smoke+qa 11/11 night-clerk)
- next-suggestion: builder lands the validator freshness law so drift goes red
  at commit time
- notes: n/a

## i139 — builder — 2026-07-06T03:36:00Z
- did: validator freshness law (ADR-016 #2) — published shelf ⊆ night-clerk
  snapshot, ghosts flagged too; skips cleanly if the clerk is ever unpublished;
  negative probe run (removed a snapshot entry → validator RED with a
  run-clerkcat hint → restored)
- line: n/a (tools; ADR-016 is the prior-iteration record)
- files: tools/validate.py
- validation: pass (green after restore; red proven during probe)
- next-suggestion: maintainer hygiene pass (#3)
- notes: drift class from IMPROVEMENTS #2 is now structurally extinct

## i140 — maintainer — 2026-07-06T03:40:00Z
- did: backlog hygiene (#3) — closed three done/overtaken items (per-plugin pages
  exist as certificates; shift-streak and weekly-shipnote both published in v8)
  with pointers; merged STATE.json's twin note/notes keys into one
- line: n/a (state hygiene)
- files: state/{BACKLOG.md,STATE.json}
- validation: pass
- next-suggestion: maintainer curates the solo dev kit (#4)
- notes: n/a

## i141 — maintainer — 2026-07-06T03:45:00Z
- did: solo-dev kit curated (#4) — env-doctor + test-gap-nudge + session-recap;
  the uncovered half of the shelf now has a bundle; clerk snapshot regenerated in
  the same iteration as night-clerk 0.1.2 (kits ride the catalog, so kit changes
  are version-law events for the clerk now — noted as standing duty)
- line: night-clerk 0.1.1 → 0.1.2 (no stage move)
- files: foundry/kits.json, plugins/night-clerk/{data/catalog.json,CHANGELOG.md,.claude-plugin/plugin.json},
  foundry/records/night-clerk.md
- validation: pass (kits suite 3/3, clerk suite 11/11, strict validate)
- next-suggestion: builder lands OG meta (#5, ADR-016 template authorization)
- notes: starter-kits experiment (review 2026-07-26) now measures 3 kits, 7 of 8
  plugins covered

## i142 — builder — 2026-07-06T03:52:00Z
- did: OG/twitter meta (#5) on the window and all 38 certificates — titles,
  descriptions, and the live "N shipped · shift iM" line all derived at build
  time from the same substantiated data as the badge (dark-pattern law holds on
  the share surface); twitter:card summary; og:url from pages_url
- line: n/a (site template, ADR-016 authorization)
- files: tools/build.py, site/** (regenerated)
- validation: pass
- next-suggestion: builder adds copy-to-clipboard (#6)
- notes: shares of the window and any certificate now unfurl with real numbers

## i143 — builder — 2026-07-06T03:57:00Z
- did: copy-to-clipboard (#6) — click any .install block (shelf cards and kits)
  to copy it whole, "copied ✓" flash for 1.4s; delegated handler so re-rendered
  blocks keep working; degrades silently without a secure context, where
  user-select:all remains the fallback
- line: n/a (site template, ADR-016 authorization)
- files: tools/build.py, site/index.html (regenerated)
- validation: pass
- next-suggestion: growth files the pr-gated-publishes verdict (#7)
- notes: n/a

## i144 — growth — 2026-07-06T04:03:00Z
- did: pr-gated-publishes interim verdict (#7) — directed slates ride PRs
  (ADR-017, codifying PR #9's zero-cost veto data); cron default honestly
  deferred to the spec's own mode:pr terms; successor backlog item filed
- line: pr-gated-publishes: trial log added (stays spec — armed, not finished)
- files: foundry/records/pr-gated-publishes.md, state/{DECISIONS.md,BACKLOG.md}
- validation: pass
- next-suggestion: designer polish pass (#9 — saga ellipsis + report-cap link)
- notes: no default flipped on proxy data — the experiment keeps its integrity

## i145 — designer — 2026-07-06T04:10:00Z
- did: polish pass (#9) — saga/ADR truncations now clip at a word boundary with a
  visible ellipsis (clip() helper); certificates over the 8-report cap link
  "all N reports →" to the label search (probed with a 9-report fixture, then
  restored); both P3 nits closed
- line: n/a (site template, ADR-016 authorization)
- files: tools/build.py, state/BACKLOG.md, site/** (regenerated)
- validation: pass
- next-suggestion: qa suite backfill ×2 (#10)
- notes: n/a

## i146 — qa — 2026-07-06T04:15:00Z
- did: suite backfill 1/2 (#10) — saga-page gets executable checks for its
  honesty claims (ADR count, invented-milestone guard, ellipsis regression,
  STATE sync); 4/4 green
- line: n/a (published record gains its suite; no stage move)
- files: foundry/tests/saga-page/saga.test.sh, foundry/records/saga-page.md
- validation: pass
- next-suggestion: qa backfills field-reports (the no-inline law deserves a test)
- notes: n/a

## i147 — qa — 2026-07-06T04:20:00Z
- did: suite backfill 2/2 for this slate (#10) — field-reports' no-inline law
  pinned with a hostile fixture; 4/4 green; remaining unsuited features stay on
  the P2 (one per qa pass, standing)
- line: n/a (published record gains its suite)
- files: foundry/tests/field-reports/reports.test.sh, foundry/records/field-reports.md
- validation: pass
- next-suggestion: designer dark mode (#11)
- notes: n/a

## i148 — designer — 2026-07-06T04:30:00Z
- did: dark mode (#11, ADR-016) — "night shift" variant of the warm-paper brand
  via prefers-color-scheme on every generated surface: window (9-var palette +
  active-chip + streak greens redrawn for dark), certificates (trust card moved
  off hardcoded paper hexes to vars), saga, embed ticker (hardcoded hexes →
  vars). Terminal panels (.term) stay dark in both schemes by design. Contrast
  spot-checked: ink/paper and dim/paper both clear 4.5:1 in dark.
- line: n/a (site template)
- files: tools/build.py, site/** (regenerated)
- validation: pass (validate + full qa 149 green)
- next-suggestion: builder ships the recorded-transcript pipeline (#12)
- notes: almanac pages render from their own template (monthly duty) — dark
  variant there rides the first almanac pass in August

## i149 — builder — 2026-07-06T04:42:00Z
- did: recorded-demo pipeline (#12) — monthly/dispatch workflow records headless
  sessions per foundry/demos/prompts/*.prompt (plugins load via the documented
  skills-directory mechanism, no invented CLI), writes dated transcripts to
  foundry/demos/<name>.txt; certificates flip "authored example" →
  "CI-recorded transcript — <date>" when a recording exists (probed both
  directions); no-credential and failed-run paths stay honest (labels don't lie);
  prompts seeded for commit-craft and test-gap-nudge
- line: n/a (workflow + template; ADR-016)
- files: .github/workflows/record-demos.yml, foundry/demos/prompts/*,
  tools/build.py
- validation: pass
- next-suggestion: builder ships tools/preflight.py + operator checklist (#13)
- notes: recordings are repo metadata (ADR-013 spirit) — no version bumps

## i150 — builder — 2026-07-06T04:50:00Z
- did: go-live assist pack (#13) — tools/preflight.py: read-only readiness pass
  (config, workflows, gates, funding state; secret NAMES only, never values) +
  the distilled 15-minute operator click-list ending at the first CI shift;
  OPERATIONS gains §0 pointing at it; live run shows 7 OK / 3 operator-optional
- line: n/a (tools, ADR-016; v9 slate items #1–#13 all built)
- files: tools/preflight.py, OPERATIONS.md
- validation: pass
- next-suggestion: auditor closes the v9 slate (audit-004), then push + PR
- notes: the only remaining unlocks are the operator's clicks — by design

## i151 — auditor — 2026-07-06T04:58:00Z
- did: audit-004 filed — v9 slate 13/13 lawful (9 releases under version law,
  2 ADRs, suites extended); self-caught incidents recorded; qa.sh silent-skip
  sharp edge filed P3; role_queue → default cycle
- line: audit-004 filed
- files: reviews/audit-004.md, state/{STATE.json,BACKLOG.md}
- validation: pass
- next-suggestion: operator runs tools/preflight.py and spends the 15 minutes
- notes: n/a

## i152 — auditor (directed) — 2026-07-06T20:45:00Z
- did: post-v9 discovery slate — IMPROVEMENTS.md refreshed (prior post-v8 slate
  fully built as v9 per audit-004; preserved in git history). 14 items across
  four lanes, all deduped against v9: user value on the shelf (update awareness,
  hook config knobs, clerk-on-window, READMEs on certificates), the untested
  gates (gates.yml PR CI, pytest for validate/build, qa.sh silent-skip, parser
  dedup), productization (SECURITY.md, hook debug mode, CI pin, release assets),
  differentiation (verified-by-foundry registry, foundry network).
- line: n/a (discovery only; nothing implemented)
- files: IMPROVEMENTS.md, state/STATE.json, state/JOURNAL.md (+ site/ regen)
- validation: pass
- next-suggestion: open the slate with #5 (gates.yml) — smallest effort, closes
  the mode:pr CI hole; ADR alongside per the two-iteration rule.
- notes: directed session riding a PR per ADR-017; role_queue untouched — the
  default cycle resumes at the next shift.

## i153 — maintainer (directed) — 2026-07-06T20:37:00Z
- did: ADR-018 filed — v10 slate opens; IMPROVEMENTS.md #1→#14 will be worked in
  order as directed iterations riding a PR (ADR-017 lane). Two-iteration rule:
  tools/template/workflow items apply from i154+.
- line: n/a (ADR only)
- files: state/DECISIONS.md, state/STATE.json, state/JOURNAL.md
- validation: pass
- next-suggestion: #1 — clerkcat.py version field + night-clerk whats-new (0.2.0).
- notes: full autonomy granted by operator; the veto window is the PR itself.

## i154 — builder (directed, v10 #1) — 2026-07-06T20:40:57Z
- did: night-clerk 0.2.0 — new `whats-new` skill (installed versions via
  `claude plugin list` vs shelf versions in the snapshot, exact
  `claude plugin update` lines, snapshot disclosure, never-invent; CLI facts
  verified against the official plugins reference); clerkcat.py now stamps each
  catalog entry with its record's version; suite +6 checks (semver present,
  catalog⇄record version drift, whats-new contract) — the drift check caught a
  real mid-iteration drift before commit; always-on re-measured 86 → 129 tok est.
- line: night-clerk stays published (version law: 0.2.0 + CHANGELOG + tag)
- files: tools/clerkcat.py, plugins/night-clerk/{.claude-plugin/plugin.json,
  CHANGELOG.md,README.md,skills/whats-new/SKILL.md,data/catalog.json},
  foundry/records/night-clerk.md, foundry/tests/night-clerk/*
- validation: pass (qa 17/17 incl. official validate; smoke green)
- next-suggestion: v10 #2 — hook config knobs (test-gap-nudge + commit-craft).
- notes: minor bump, not patch — a new skill is new surface.

## i155 — builder (directed, v10 #2) — 2026-07-06T20:44:04Z
- did: hook configurability convention — test-gap-nudge 0.2.0 gains
  TEST_GAP_NUDGE_EXTS (source-extension override, sanitized to [A-Za-z0-9|]);
  commit-craft 0.2.0 gains COMMIT_CRAFT_TYPES (type-list override, lowercase
  tokens only — regex injection structurally impossible). Both fail open on
  malformed values (empty → defaults); READMEs document the knobs; suites +7
  checks incl. hostile-value and injection probes, all green (17/17, 7/7).
- line: both stay published (version law: 0.2.0 ×2 + CHANGELOGs + tags)
- files: plugins/{test-gap-nudge,commit-craft}/*, foundry/records/{test-gap-nudge,commit-craft}.md, foundry/tests/{test-gap-nudge/acceptance,commit-craft/hook}.test.sh
- validation: pass (qa green, smoke green)
- next-suggestion: v10 #3 — storefront picker (template change under ADR-018).
- notes: knobs replace, not extend — one rule to document, one to test.

## i156 — maintainer (directed) — 2026-07-06T20:44:55Z
- did: night-clerk 0.2.1 — snapshot refresh after the v10 #2 hook bumps (catalog
  now says 0.2.0 for commit-craft and test-gap-nudge). The i154 version-drift
  check went red and forced this, exactly as designed; process note for future
  iterations: regenerate the catalog LAST, after the record bump, or the check
  trips on the clerk itself (bit me twice today).
- line: night-clerk stays published (version law: 0.2.1 + CHANGELOG + tag)
- files: plugins/night-clerk/{.claude-plugin/plugin.json,CHANGELOG.md,data/catalog.json}, foundry/records/night-clerk.md
- validation: pass (qa 17/17)
- next-suggestion: v10 #3 — storefront picker; and #10 should end with one
  clerk refresh in the same style.
- notes: any shelf version bump now implies a clerk patch — that's the price of
  a front desk that never lies about versions. Worth it.

## i157 — builder (directed, v10 #3) — 2026-07-06T20:48:29Z
- did: the front desk on the window — a picker above the shelf ("say what you're
  working on") that scores published plugins + kits against the query and answers
  with ≤3 real install blocks, the night-clerk's honesty rules intact (published
  only, honest empty answer + idea route, nothing invented, copy-to-clipboard
  free via the existing delegate). Template change under ADR-018; window v0.6.
  Verified in real Chromium: commit query → commit-craft, nonsense → honest
  empty, workflow query surfaces a kit, zero page errors.
- line: n/a (window feature)
- files: tools/build.py, site/* (regenerated)
- validation: pass (browser-verified; gates green)
- next-suggestion: v10 #4 — READMEs on certificate pages.
- notes: the picker is the clerk for people who haven't installed the clerk.

## i158 — builder (directed, v10 #4) — 2026-07-06T20:49:08Z
- did: certificate pages now open with the shipped README, verbatim and escaped
  ("README — exactly what installers receive") for plugin-kind records with an
  artifact on disk; feature certificates unaffected. The storefront is
  self-contained at the install decision — no more leaving for the file tree.
- line: n/a (window feature, ADR-018)
- files: tools/build.py, site/p/* (regenerated)
- validation: pass (assertions: present on 3 plugin pages, absent on feature page)
- next-suggestion: v10 #5 — gates.yml.
- notes: verbatim-in-pre over a hand-rolled markdown renderer: stdlib-only law,
  and a README that must read well as plain text is a good constraint anyway.

## i159 — builder (directed, v10 #5) — 2026-07-06T20:50:14Z
- did: .github/workflows/gates.yml — validate.py + build.py now run on every PR
  and non-main push (main already gets them via deploy-site.yml), plus a
  generated-output sync check: rebuild, restore the three measured
  timestamp-volatile files (data.json, index.html, feed.xml), fail on any other
  site/ or INDEX.md diff. Both directions simulated locally: in-sync tree
  passes, doctored queue.html fails.
- line: n/a (workflow, ADR-018)
- files: .github/workflows/gates.yml
- validation: pass
- next-suggestion: v10 #6 — the gate tests themselves.
- notes: mode:pr shifts finally get checked before the human veto — the veto
  window was reviewing unvalidated diffs until now.

## i160 — qa (directed, v10 #6) — 2026-07-06T20:52:39Z
- did: the gates get their own gate — foundry/tests/_tools/: fixture.py builds a
  minimal VALID foundry (published plugin, record, artifact, suite, marketplace);
  gates.test.sh proves baseline green then breaks one law per case and asserts
  the exact error fires: missing section, bad semver, version drift, unlisted
  publish, unknown hook event, banned .* matcher, unquoted plugin root,
  unterminated front matter, lost exec bits (suite + shipped script), missing
  review approval, orphan artifact — and build.py runs green on the fixture.
  14/14; rides qa.sh like every other suite, so gates.yml runs it in CI when
  tests change.
- line: n/a (test infrastructure, ADR-018)
- files: foundry/tests/_tools/{fixture.py,gates.test.sh}
- validation: pass (full qa green)
- next-suggestion: v10 #7 — qa.sh per-file exec-bit fail (validator covers the
  zero-executables case; the one-lost-chmod case is qa.sh's to catch).
- notes: the fixture pattern means future validator laws ship with a red/green
  proof instead of a promise.

## i161 — builder (directed, v10 #7) — 2026-07-06T20:53:43Z
- did: qa.sh silent-skip fixed (audit-004 P3) — a *.test.sh that exists but lost
  its exec bit is now an explicit FAIL with the chmod hint, at every stage; the
  validator keeps owning the zero-executables case at rc+. Proven red (chmod -x
  a real suite → harness fails) then green (179 ok / 0 fail).
- line: n/a (tools, ADR-018)
- files: tools/qa.sh
- validation: pass
- next-suggestion: v10 #8 — parse_front_matter dedup into tools/lib.py (the
  _tools fixtures now guard the refactor).
- notes: also updates BACKLOG — the P3 filed at i151 closes with this.

## i162 — builder (directed, v10 #8) — 2026-07-06T20:55:54Z
- did: one parser, one truth — parse_front_matter extracted to tools/lib.py
  (strict mode with error reporting for validate.py; lenient for build.py and
  clerkcat.py, whose hand-rolled regex variant is gone too). Gate fixtures
  guarded the refactor: 179/179 green, clerkcat output byte-identical so no
  night-clerk bump owed.
- line: n/a (tools, ADR-018)
- files: tools/{lib.py,validate.py,build.py,clerkcat.py}
- validation: pass (full qa green; catalog diff empty)
- next-suggestion: v10 #9 — SECURITY.md.
- notes: three parsers had already drifted (clerkcat parsed tags as a string);
  the drift class is now extinct the same way the catalog one was.

## i163 — maintainer (directed, v10 #9) — 2026-07-06T20:56:39Z
- did: root SECURITY.md — GitHub-recognized policy: private vulnerability
  reporting path (Security → advisories), public bug lane for non-exploitable
  defects with the LOOP.md priority promise, supported-versions statement
  (latest published only, updates ride semver), and the hook-safety law
  restated as user-facing commitments (fail-open, no network, narrow matchers,
  zero secrets) with the commit-craft guard exception disclosed honestly.
- line: n/a (docs/policy)
- files: SECURITY.md
- validation: pass
- next-suggestion: v10 #10 — hook debug mode (ends with a clerk catalog refresh).
- notes: charter/SECURITY.md stays the internal law; root SECURITY.md is its
  public face — same posture, different audience.

## i164 — builder (directed, v10 #10) — 2026-07-06T20:58:38Z
- did: opt-in debug trails for both fail-open hooks — test-gap-nudge 0.3.0
  (TEST_GAP_NUDGE_DEBUG=1 → why-silent/why-nudged log in TMPDIR) and
  commit-craft 0.3.0 (COMMIT_CRAFT_DEBUG=1 → pass reason or BLOCK + enforced
  list). Debug-off proven byte-identical (no log file, same output, same exit
  codes) by new suite checks; 19/19 and 9/9 green, smoke green.
- line: both stay published (version law: 0.3.0 ×2 + CHANGELOGs + tags)
- files: plugins/{test-gap-nudge,commit-craft}/*, records ×2, suites ×2
- validation: pass
- next-suggestion: clerk catalog refresh (i156 style), then v10 #11.
- notes: "fails silently by design" now has a diagnosable mode — the organic-bug
  lane Gate B waits on needs users who can SEE what a hook decided.

## i165 — maintainer (directed) — 2026-07-06T20:58:59Z
- did: night-clerk 0.2.2 — catalog refresh after the v10 #10 hook bumps
  (0.3.0 ×2 on the shelf). Regenerated after the record bump this time; drift
  check green on the first run.
- line: night-clerk stays published (version law: 0.2.2 + CHANGELOG + tag)
- files: plugins/night-clerk/{.claude-plugin/plugin.json,CHANGELOG.md,data/catalog.json}, foundry/records/night-clerk.md
- validation: pass (qa 17/17)
- next-suggestion: v10 #11 — pin the CI toolchain.
- notes: n/a

## i166 — builder (directed, v10 #11) — 2026-07-06T21:00:00Z
- did: CI toolchain pinned — .claude-code-version (2.1.201, the exact CLI every
  suite and smoke ran green against today) is now the single source; qa.yml
  (both jobs), record-demos.yml, and run-shift.yml install
  @anthropic-ai/claude-code@$(cat .claude-code-version) instead of floating
  latest. Bumps are now a deliberate one-line diff that CI re-verifies.
- line: n/a (workflows, ADR-018)
- files: .claude-code-version, .github/workflows/{qa,record-demos,run-shift}.yml
- validation: pass
- next-suggestion: v10 #12 — release assets.
- notes: a weekly re-verify that floats its own harness wasn't re-verifying —
  tested_with stamps now mean one thing.

## i167 — builder (directed, v10 #12) — 2026-07-06T21:01:13Z
- did: releases now carry the artifact — release-on-tag.yml zips plugins/<name>/
  exactly as installers receive it and attaches it plus the plugin's
  marketplace.json entry to every release; refuses to attach a ghost entry if
  the name isn't on the shelf. Steps simulated locally against
  night-clerk-v0.2.2 (zip 12 files, entry extracted); run block extracted from
  the YAML and bash -n clean.
- line: n/a (workflow, ADR-018; extends the releases-and-reverify feature)
- files: .github/workflows/release-on-tag.yml
- validation: pass
- next-suggestion: v10 #13 — verified-by-foundry enters the line as an idea.
- notes: rollback is now "download the zip from the last good release".

## i168 — ideator (directed, v10 #13) — 2026-07-06T21:04:12Z
- did: verified-by-foundry pitched — the verification machinery pointed outward:
  standalone doctor + composite Action any plugin repo can run in CI + a
  registry/hall that renders nothing until it has a first name. Deduped against
  records (plugin-smith's doctor skill is interactive and inward; this is CI
  and outward).
- line: verified-by-foundry → idea (record created)
- files: foundry/records/verified-by-foundry.md
- validation: pass
- next-suggestion: builder specs it (verbatim acceptance checks; Experiment).
- notes: the moat is the law book, not the badge.

## i169 — builder (directed, v10 #13) — 2026-07-06T21:04:39Z
- did: verified-by-foundry specced — doctor.py contract (standalone, one-plugin,
  law tables imported from validate.py so there is exactly one law book),
  composite-action interface, registry schema with the substantiated-numbers
  law (no public run link, no entry), and the renders-nothing-empty window
  section. Four executable acceptance checks.
- line: verified-by-foundry idea → spec
- files: foundry/records/verified-by-foundry.md
- validation: pass
- next-suggestion: builder builds (doctor.py + action + registry + window).
- notes: registry entries are maintainer-curated from public run links — the
  badge can't be self-awarded by a stranger's fork.

## i170 — builder (directed, v10 #13) — 2026-07-06T21:06:32Z
- did: verified-by-foundry built — doctor.py (8/8 shelf OK; hostile fixture:
  every law named), composite action, empty registry with the
  no-run-link-no-entry law inline, window section (renders nothing empty),
  README paste-block for third-party repos.
- line: verified-by-foundry spec → building (build complete in one pass)
- files: tools/doctor.py, .github/actions/foundry-doctor/action.yml,
  foundry/verified.json, tools/build.py, README.md, record, site/*
- validation: pass
- next-suggestion: qa runs the acceptance checks as an executable suite → rc.
- notes: doctor imports validate's tables — the law book stays singular.

## i171 — qa (directed, v10 #13) — 2026-07-06T21:07:19Z
- did: verified-by-foundry QA — acceptance checks 1–4 executable
  (foundry/tests/verified-by-foundry/, 12 checks green), adversarial probes on
  the doctor (no-manifest dir) and the action path. TEST VERDICT: pass.
- line: verified-by-foundry building → rc
- files: foundry/tests/verified-by-foundry/checks.test.sh, record
- validation: pass (qa 12/12)
- next-suggestion: reviewer for the publish gate.
- notes: check2 asserts each law is NAMED, not just that the doctor fails —
  a doctor that says "something's wrong" without saying what is no doctor.

## i172 — reviewer (directed, v10 #13) — 2026-07-06T21:08:28Z
- did: verified-by-foundry reviewed — approved with one required fix, applied
  and verified in-pass: honest-limits copy on every trust surface (README,
  window footer, action description) so "verified" cannot be read as "safe".
  Structure-not-intent is now stated wherever the badge appears.
- line: verified-by-foundry stays rc (review gate cleared; publish next)
- files: foundry/records/verified-by-foundry.md, README.md, tools/build.py,
  .github/actions/foundry-doctor/action.yml, site/*
- validation: pass (suite 12/12 after edits)
- next-suggestion: maintainer publishes.
- notes: a trust product that oversells is worse than none — the fix was the
  review's whole value.

## i173 — maintainer (directed, v10 #13) — 2026-07-06T21:08:47Z
- did: verified-by-foundry published. The foundry's machinery points outward
  for the first time: any plugin repo can run the doctor in CI with one
  paste-block; a public green run + issue earns a dated, run-linked listing.
- line: verified-by-foundry rc → published (v10 #13 complete: idea→published
  in five lawful stages, i168–i173)
- files: foundry/records/verified-by-foundry.md, site/*
- validation: pass
- next-suggestion: v10 #14 — foundry-network spec → building.
- notes: first registry entry will be the experiment's first data point.
