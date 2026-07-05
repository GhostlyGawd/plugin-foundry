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
