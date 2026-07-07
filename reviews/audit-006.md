# Audit 006 — the v11 UX slate (IMPROVEMENTS v11 #1–#12, i180–i191)

Auditor pass closing the v11 slate (ADR-019). Directed session riding the
ADR-017 PR lane; operator directive: "more user friendly, easy to use, and
intuitive," built in order.

## Lawfulness

- **One task, one commit, one journal entry:** 12 iterations i180–i191, one
  commit each (i190 covers #10+#11 — one file, one rewrite, journaled as such).
- **Two-iteration ADR rule:** ADR-019 filed i180; template/tools/skill changes
  began i181. Honored.
- **Version law:** the #2 Manage sweep bumped all 8 published plugins
  (patch ×8) with same-iteration CHANGELOGs + annotated tags; the clerk
  catalog was regenerated LAST (drift check green on first run — the i156
  lesson held). #4 was deliberately scoped to the root README to avoid a
  bump cascade for one paragraph; scope note journaled.
- **Docs before invention:** the Manage section's lifecycle commands
  (`claude plugin update|disable|enable|uninstall`) were verified against the
  official plugins reference before writing.
- **Spec-is-law:** no item required a record stage move; all were window/docs/
  tools growth under existing published features.

## Verification quality

- Browser-verified in real Chromium: #8's unified input (single-word = filter
  only, task query = front-desk answer, nonsense = honest empty, reset) and
  #9's chips (feed + repo-substantiated releases href). #6's section order and
  #7's nav grouping asserted programmatically; #3's data plumbing asserted;
  inline JS re-parsed after every template change.
- #11's tag-drift check found a real defect on its first run: 15 local release
  tags the remote never received (the v10 close-out flagged this manually;
  now a machine catches it every preflight).

## UX principles held

- **Plain layer over lore, never lore removal** (ADR-019): strap leads with
  "A plugin marketplace for Claude Code"; backstage nav keeps Saga/Theater/
  Almanac with translating tooltips; "docs & history — the full paper trail"
  keeps both registers.
- **Honesty in affordances:** multi-line kit blocks admit slash commands run
  one at a time; the releases chip renders only with a configured repo; the
  front desk still never invents a plugin.

## State at close

validate: OK — 39 records, 34 published · build: OK · qa: 201 ok / 0 skip /
0 fail · smoke: 8/8 · preflight: TODO(operator) items unchanged plus the
tag-drift line (15 tags await `git push origin --tags`).

## Verdict

v11 slate: 12/12 built lawfully. Operator actions outstanding: merge the PR,
`git push origin --tags` (now 15 tags), and the standing preflight click-list
(`python3 tools/preflight.py --issue` renders it tickable).
