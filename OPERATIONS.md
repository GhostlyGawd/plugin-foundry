# OPERATIONS — current operating mode

The repository is the database, GitHub Pages is the window, and model work is
interactive-only. GitHub Actions handles deterministic validation, security,
packaging, deployment, and maintenance; it does not invoke an LLM.

## 0 · Preflight

Run `python3 tools/preflight.py` for a read-only repository check. Add `--issue` to
render the same facts as a GitHub checklist. The preflight never reads, requests,
or provisions a model credential.

## 1 · Put a fork on GitHub

```bash
cd pluginfoundry && git init -q && git add -A
git commit -m "loop(i0/genesis): seed the workshop"
gh repo create <you>/pluginfoundry --public --source . --push
```

Keep `main` protected by pull requests, Gates, and CodeQL. Never push model-created
changes directly to the default branch.

## 2 · Turn on the window

Repo → Settings → Pages → Source: **GitHub Actions**. Set `repo` and `pages_url` in
`foundry/site-config.json`, then merge a green pull request. `deploy-site.yml`
publishes the generated static site without a model credential.

## 3 · Run an attended model session

The `Run shift` and `Record demo transcripts` workflows are disabled in repository
settings and are inert, schedule-free pause notices in the tracked tree. Do not add
a model API key, OAuth token, browser session, `auth.json`, or subscription token to
GitHub.

From a trusted local checkout:

```bash
codex
# or ./loop.sh, which verifies an interactive terminal before opening Codex
```

Use the coding agent's normal local sign-in. Ask it to read `LOOP.md`, complete one
task, run the required gates, and propose a pull request. Keep the session attended
and review tool calls. `codex exec`, `claude -p`, schedulers, background services,
and CI model calls are outside the current operating policy.

Resuming unattended model execution requires a new reviewed ADR, explicit operator
approval, and a supported credential and billing design. Re-enabling a workflow is
not sufficient.

## 4 · Optional request box

Follow `services/commission-worker/README.md` for the Stripe Payment Link →
Cloudflare Worker → GitHub issue path. A commission buys priority and a serious
attempt, never guaranteed delivery. The next attended session handles queued work.

## 5 · Observe and steer

- The site shows the plugin shelf, public records, and the explicit paused status.
- Git history and `state/JOURNAL.md` are the audit trail.
- Put pitches in `state/BACKLOG.md § Idea inbox` or use the issue templates.
- Merge approves a change; closing its pull request vetoes it.

## 6 · Optional low-data instruments

- GoatCounter is optional. Without it, pageview fields remain honestly null.
- Voting uses GitHub issue reactions.
- The static site uses no analytics or tracking by default; see `PRIVACY.md`.

## 7 · Automation boundary

Still active: Gates, CodeQL, Dependabot/Renovate, Pages deployment, release/tag
handling, weekly deterministic verification, shipnotes, ops guard, and the
deterministic orchestrator. Any repository mutation still proposes a pull request.

Paused: every model-backed GitHub workflow and every headless local loop.

## 8 · Costs and credentials

Interactive model usage is governed by the signed-in host account. The repository
stores no model credential and makes no claim that a subscription session is a
reusable CI token. GitHub Actions and Pages usage remain subject to GitHub's plan;
the optional Worker remains subject to Cloudflare's plan.
