# Audit 007 — the v12 slate (IMPROVEMENTS v12 1.1–4.2, i197–i212)

Auditor pass closing v12 (ADR-021) — the first slate built against a LIVE
window. Directed: "Build all in order until complete."

## Outcome: 13 built, 1 blocked-with-recipe

- **Built:** ops-guard (labels + failure catcher), dep-bump-brief published
  (ninth plugin, full idea→published walk, i199–i203), release bodies
  (lineage + install), og:image (real Chromium shot of the window), intake
  hostile-fixture suite (11 checks, all defenses held first run), backlog
  hygiene (9 items evidenced closed), governor suite (budget halt + metrics
  honesty, 9 checks), shift-zero feedback, 404 + sitemap(43 URLs) + robots,
  verified badges (delist kills the badge).
- **Blocked:** 4.1 genesis ceremony — create_repository 403; no session or
  workflow token can create repos. Verified, journaled (i212), P1 unblock
  recipe in BACKLOG; the ADR-021 blessing survives for the finishing session.

## Lawfulness

- One task/commit/journal ×16 iterations (i197–i212); two amended
  in-iteration with fixed-then-pass journaled (i198 YAML block scalar,
  i201 line-wrap grep) — both times the defect was caught by our own checks
  post-commit and amended before push.
- Version law: dep-bump-brief 0.1.0 + night-clerk 0.2.4 (catalog regenerated
  LAST; drift check green first run). Tags to be cut via release dispatch
  post-merge — TAGS-PENDING stays empty by design; preflight's drift check
  will name them until the dispatches run.
- Two-iteration rule: ADR-021 i197, changes from i198. Genesis exception
  scoped in the ADR (one repo, this slate) — exercised, denied, expired
  unused except for the attempt itself.
- Reviews stayed genuine: dep-bump-brief's review put the memory-leak
  question on the record; the tripwire stands.

## Test posture at close

qa: 34 _tools checks (gates 14, intake 11, governor 9) + per-plugin suites;
full harness green. The three most safety-critical tools (validate, intake,
budget) are all now fixture-tested against hostile input.

## Operator actions outstanding

1. The Claude secret (unchanged — the only Gate A blocker).
2. One empty public repo to unblock the genesis ceremony (4.1).
3. Optional: budget var, GoatCounter, FUNDING handle.

## Verdict

v12: 13/14 built lawfully, 1 blocked at a permission boundary the repo
cannot cross by construction — filed, not fudged.
