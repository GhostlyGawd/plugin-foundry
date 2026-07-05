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
