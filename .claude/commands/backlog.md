---
description: Steer the workshop in one sentence — add a correctly-formatted backlog item or pitch
---
The operator is steering. Their input follows this command; turn it into exactly
one correctly-formatted entry in @state/BACKLOG.md and change nothing else.

1. Classify the input:
   - starts with P0/P1/P2/P3 (or clearly a directive/task) → a **work item**;
   - reads like a plugin idea ("a hook that…", "something to…") → a **pitch**.
2. Work item → append under the current slate section (or `## Grow` if no slate
   is open) as `- [ ] P<n> (<best-fit role>) <text>` — priority from the input,
   default P2; pick the role from charter/ROLES.md by the nature of the work.
3. Pitch → append under `## Idea inbox (humans drop raw pitches here; Ideator
   formalizes)` as `- [ ] I-op (operator) <text>` — the Ideator formalizes it
   into a record on a later iteration, with credit.
4. Laws that bind this command: BACKLOG is check-off-don't-delete; max 3 new
   items per iteration (you are adding ONE); never touch other entries, the
   role_queue, or STATE.json. This is steering, not an iteration — no journal
   entry, no stage moves.
5. Echo the exact line you added and where, then stop. If the input is empty
   or you cannot classify it, ask — never guess a P0.
