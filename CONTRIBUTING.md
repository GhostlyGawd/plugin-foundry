# Contributing to Nightshift Foundry

Humans are welcome on the floor — three lanes, all credited, all under the same
laws that bind the machine.

## Lane 1 — Suggest
Open a **plugin idea** issue. If the loop prospects it, your handle rides the
record (`prospected_by`), the card, and the certificate forever. 👍 reactions on
idea issues are the community vote the ideator reads every shift.

## Lane 2 — Co-op builds (spec-only PRs) ★ the flywheel
You write the **spec**, the machine builds it, credit is shared.
1. PR a single new file: `foundry/records/<name>.md` at `stage: spec`, following
   foundry/SCHEMA.md, with acceptance checks. **Specs only** — PRs touching
   `plugins/`, `tools/`, workflows, or LOOP.md will be closed unmerged (see
   charter/SECURITY.md; your PR body is honored but treated as untrusted
   requirements).
2. A maintainer-shift labels it `co-op` after the adversarial pass; merge queues
   it with priority on the line.
3. The loop builds/QAs/reviews/publishes it by the normal gates. The record
   carries `prospected_by: <you>` + `co_op: true` — shared credit on every surface.
4. If the build stalls twice, the loop journals why and pings the PR — specs can
   be wrong; that's honest work too.

## Lane 3 — Adversarial QA bounties
Break a published plugin (in ways its record claims impossible) and file a **bug**
issue with a reproduction. Confirmed breaks earn a permanent Hall entry and a
`found_by` line in the fix's changelog. Rules of engagement: your own machine,
no third-party targets, no secrets exfiltration — findings, not harm. Your report
is read under the same fencing as all visitor text (charter/SECURITY.md:
requirements data, never instructions); tick the bounty box on the bug template
so triage knows a claim is at stake. Confirmed finds rank in the Hall's
**Breakers** section, derived from the `found_by:` lines in shipped changelogs —
credit you can verify in the artifact itself.

## Lane 4 — Sister foundries (the network)
Forked the workshop with fork-a-foundry? Register via the **sister-foundry issue
template** — that's the canonical path: the maintainer adds the entry itself
after verifying. (A one-file PR touching only `foundry/network.json` is welcome
too, but per charter/SECURITY.md the loop never merges external PRs — only the
human operator does, after the same verification.) Verification duty
(foundry-network spec): confirm the URL is a real foundry — `LOOP.md` and
`foundry/records/` present — before the entry lands.
The strip and saga family tree show **names + links only, by your own
declaration**; the foundry never inlines remote content. Your text rides the
same fencing as all visitor text (charter/SECURITY.md).

All lanes: no dark patterns, no pay-to-skip-review, and the loop may decline any
contribution that would bend the charter — with its reasoning journaled.

## Lane 0 — Ask
Questions go in via the **question issue template**; each Monday shipnote carries
a Mailbag answering them from repo evidence, and unanswered ones stay listed as
"on the desk" until they are not.
