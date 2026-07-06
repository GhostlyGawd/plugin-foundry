# Audit #4 — the v9 slate: discovery report, built in order (i136–i151)

Auditor pass closing ADR-016. Source: IMPROVEMENTS.md (operator-commissioned
product discovery, 13 items). Second PR-gated slate (ADR-017 practice).

## What shipped, item by item
1. README front-door install line fixed + regression (i136).
   Sweep: the same placeholder in ALL 8 plugin READMEs → 7 plugins to 0.1.1
   under the version law, tagged (i137); night-clerk held for its own release.
2. night-clerk 0.1.1: snapshot regenerated (was a day stale, missing the 8th
   plugin) + freshness regression (i138); validator law — shelf ⊆ snapshot,
   probed red — makes the drift class extinct (i139).
3. Backlog hygiene: 3 done/overtaken items closed with pointers; STATE.json twin
   note keys merged (i140).
4. Solo-dev kit (env-doctor + test-gap-nudge + session-recap); night-clerk 0.1.2
   carries it — kit curation is now a clerk version-law event, noted (i141).
5. OG/twitter meta on the window + all 38 certificates, values build-derived
   (dark-pattern law holds on the share surface) (i142).
6. Copy-to-clipboard with "copied ✓" flash; selection fallback intact (i143).
7. pr-gated-publishes INTERIM verdict + ADR-017: directed slates ride PRs
   (proven on PR #9); cron default honestly deferred to the spec's own
   mode:pr terms — no default flipped on proxy data (i144).
8. (folded into #2/#4 — clerk snapshot carries kits.)
9. Polish: word-boundary ellipsis on saga truncations; "all N reports →" cap
   link, fixture-probed (i145).
10. Suite backfill ×2: saga-page (invented-milestone guard live) and
    field-reports (no-inline law pinned with a hostile fixture) (i146–147).
11. Dark mode ("night shift" palette) across window/certificates/saga/embed;
    contrast spot-checked; almanac rides its August pass (i148).
12. Recorded-demo pipeline: monthly workflow, documented skills-dir loading (no
    invented CLI), dated label flip probed both directions; honest-skip without
    credentials (i149).
13. tools/preflight.py + OPERATIONS §0: 7 OK / 3 operator-optional on the live
    run; the 15-minute click-list ends at the first CI shift (i150).

## Inspection health
- Gates green at every one of the 15 commits; full harness at close:
  validate OK (38 records, 32 published), qa 152+ checks, official strict PASS.
- Self-caught incidents (unabridged): a test file created without shebang/exec
  bit that qa.sh skipped silently (caught + fixed i138 — noted as a qa.sh
  sharp edge for a future ADR); one mangled CSS line and one mangled Python
  line caught by re-reading before commit (i148, i150).
- Tags created locally for 8 releases; tag pushes remain 403 (branch-scoped
  credential) — preflight step 6 hands this to the operator.

## Carried risks
- qa.sh silently ignores non-executable *.test.sh files — propose a warning in
  a future iteration (needs its own ADR for tools/).
- Kit changes now require night-clerk version bumps (coupling accepted i141 —
  the clerk must never lie about the shelf; revisit if kit churn grows).

## Verdict
v9 slate complete and lawful: 13/13 items, 9 plugin releases under version law,
2 ADRs, 4 new/extended executable suites. role_queue refilled with the ROLES.md
default cycle. The line's next real event is the operator's 15 minutes.
