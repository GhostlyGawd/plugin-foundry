# AGENTS — the agent contract (MASTER.md P0.1, ADR-026)

Every ops agent in this workshop — the briefing writer, the scout, the tripwire
auditor, eventually the whole back office — conforms to one contract. The contract
is what makes the constitution (charter/CONSTITUTION.md) enforceable and the
single-writer discipline (tools/orchestrator.py) real. Under ADR-032 the model-backed
product loop is dormant and may run only in a live, attended interactive session.
Deterministic agents may still use the orchestrator. Every mutation proposes a pull
request, and no agent writes to `main` directly.

## The manifest

An agent lives at `foundry/agents/<agent-id>/` with an `agent.json` manifest.
The schema is `foundry/agents/schema.json`; the loader in `tools/lib.py` enforces
it plus the hard rules below; `foundry/agents/registry.json` is generated — never
hand-edited.

Required fields:

| Field | Values | Meaning |
|---|---|---|
| `id` | slug (= directory name) | immutable identity; also keys `identities.json` |
| `role` | free text | one line: what this agent is for |
| `trigger` | `schedule` \| `dispatch` \| `event` | how it wakes |
| `trust_tier` | `trusted` \| `ingests_untrusted` | does third-party text reach its prompt? |
| `quota_tier` | `product` \| `high` \| `low` | who eats first when quota thins |
| `capability` | `read_only` \| `proposes` \| `writes:<glob>` | the most it may do |
| `outputs` | list of paths/artifacts | where its work lands |
| `heartbeat` | `{"interval_hours": N}` | staleness threshold for liveness alarms |

Optional fields: `description`, `prompt` (path to its prompt file), `workflow`
(the Actions workflow that runs it), `gates` (checks its output must pass),
`lands_via` (`orchestrator` — required for any `writes:` capability), `fenced`
(true — required for any `ingests_untrusted` agent).

## The four hard rules

1. **No agent pushes to `main` directly.** Ops-agent mutations flow through the
   orchestrator (single writer), and the orchestrator proposes its batch as a PR.
   In the manifest, `capability: writes:<glob>` is only lawful with
   `lands_via: "orchestrator"`. The dormant product loop `foundry-loop` is the
   manifest routing exception: when an operator invokes it in an attended session,
   that session proposes a branch and pull request. GitHub Actions cannot invoke a
   model. The protected branch requires Gates and CodeQL for every path.
2. **Untrusted input is fenced before it reaches a prompt.** `ingests_untrusted`
   agents must declare `fenced: true` and are barred from `writes:` capability
   entirely — the read/act split. An agent that reads the world does not, in the
   same pass, hold a pen (MASTER.md G2; the lethal-trifecta mitigation).
3. **Writes pass the gates.** Any `writes:` agent must list `"guard"` and
   `"validate_state"` in `gates` — tools/guard.py (constitution) and
   tools/validate_state.py rule on every proposed changeset before it lands.
4. **Every agent is accountable.** Every agent heartbeats (P0.9) and commits
   under its own identity with an `Agent: <id>` trailer (P0.3). `foundry-loop`
   authorship is reserved for the product loop.

## Quota tiers (P0.6)

`product` (the plugin-building loop) has first claim when model execution is enabled;
ADR-032 currently keeps it dormant. `high` = safety/trust agents
(guard-adjacent, tripwire, red-team). `low` = perception/comms (scout, briefing,
shipnotes). Under rate-limit pressure the allocator sheds `low`, then `high`,
**never `product`** — when active, the factory ships before it talks.

## Orchestrator precedence (P0.7)

Highest wins: **guard veto → product loop → safety/trust → governance/steering →
docs/comms/perception.** Ties break by timestamp; the lower-priority writer of a
conflicting file defers and re-queues. No agent edits its own governing rule —
changes to an agent's manifest, prompt, or the rules that bind it route to the
owner's desk (charter/CONSTITUTION.md).
