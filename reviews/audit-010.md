# Audit 010 — the MASTER.md org-pattern program (i218–i245)

Auditor close-out of the operator-directed program: *"build every line item in
that master document from end to end until 100% complete and accounted for."*
Method: staged slates (Stage 0–4) as directed PRs, per-item iterations, gates
green before every commit, self-merged on green CI under the ADR-031 mandate.
This audit verifies the claim, honestly — including where "accounted for" means
built-to-the-edge or deferred, not shipped-and-live.

## Outcome: every §14 line item accounted for

`state/PROGRAM.md` is the ledger. Final tally across MASTER.md §14:
- **BUILT + tested:** the moat (agent contract, constitution+guard, orchestrator,
  quota v2, auth, fence, identity, state validator, heartbeats) and the
  differentiators (spec-drift, tripwire, red-team, multi-harness export,
  durability doc, the quality number, replay, dogfood card, briefing, quarterly,
  ask, diagnostician, steer, naming, postmortems). 13 agents in the registry,
  all with identities + heartbeats. **~30 tools, each with an executable suite.**
- **BOUGHT + integrated to the edge (desk-gated install):** trust-fencing scanner
  (LLM Guard/Lakera seam), Renovate+Dependabot+Socket, CodeRabbit, Dosu,
  Mem0/Zep memory seam, Argos, promptfoo. Five app-installs queued as desk items
  d-0002…d-0005; Dependabot is native and live.
- **OPERATOR-gated (kit prepared, desk-queued):** the launch window (LAUNCH.md,
  d-0006), ecosystem submissions (SUBMISSIONS.md, d-0001). Posting under the
  operator's identity is theirs alone (constitution Art. I §7).
- **DEFERRED, tracked:** P2.3, P2.4, P3.6, P4.1 generator, P5.3, GAP-F, and the
  P4.4 night-clerk auto-responder (MASTER's own verdicts — nothing silently lost).
- Five new ADRs filed and in effect: 026 (contract), 027 (constitution+guard),
  028 (quota v2), 029 (owner's desk), 030 (evals) + 031 (program mandate).

## Definition-of-done (§14) — verified, with one honest caveat

| DoD | Status |
|---|---|
| Untrusted paths fenced; CI lint proves it | ✅ `validate_state.py` fails an unfenced `ingests_untrusted` prompt |
| Every human decision → one desk; nothing auto-merges | ✅ guard routes ratification to the desk; orchestrator honors it; 8 real items queued |
| Guard blocks schema edits / record deletion / self-rule / third-party PRs | ✅ 25/25 golden evals, merge-blocking |
| Quota v2 protects the product loop under pressure | ✅ product never sheds on pressure; ≥1.0 kill switch → desk |
| Every agent has identity + heartbeat; risky ones an eval fixture | ✅ 13/13 identities+heartbeats; guard/fence golden fixtures |
| The quality number is live + public | ✅ hero stat + `site/quality.json` badge (10 · 86% · 5 bounces) |
| ADRs 026–030 (+031) filed | ✅ |
| fork-a-foundry inherits the whole framework | ✅ v0.2.0 — a fork boots the company, not just the loop |
| **No workflow but the orchestrator + run-shift writes to main** | ⚠️ **partial — see below** |

**The one honest caveat (DoD "single writer"):** the orchestrator (P0.7) is built
and is the single-writer landing path *for the agent framework* — every agent
proposes to the outbox and the orchestrator serializes attributed commits. But
two **legacy product-loop workflows predate it and still commit to main
directly**: `record-demos.yml` (CI-recorded transcripts) and `qa.yml` (weekly
metadata-only re-verify stamps, ADR-013). `lay-tags.yml` pushes only tags (a
separate ref — the release ledger, not main content). These are product
machinery in the same class as the grandfathered `run-shift`, not ungoverned
agents — but the DoD as written is not 100% met until they either route through
the orchestrator or are explicitly grandfathered by an operator-ratified ADR.
Filed as a backlog item; not claimed as done.

## One thing working, one thing to watch

- **Working:** the desk is doing its job. Eight real operator decisions
  (submissions, five app-installs, launch, two quarterly recs) reached *one*
  ranked queue — the anti-firehose design (G4) proven on real load, not fixtures.
- **To watch (a real positive):** `tools/tripwire.py check` fires on the repo's
  own QA history — five clean zero-defect passes look like a rubber-stamp streak
  (LOOP.md rule 7). That is the tripwire working, and it is a genuine signal the
  next audit should honor with an adversarial re-audit, not suppress.

## Verdict

The program is **complete and accounted for** against MASTER.md §14, with the
single-writer DoD honestly marked partial (two legacy workflows to migrate). The
plugins remain the deliverable; the org pattern is now a built, tested, governed
artifact — and `fork-a-foundry` carries it, so the pattern propagates.
