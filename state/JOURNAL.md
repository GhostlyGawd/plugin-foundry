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
