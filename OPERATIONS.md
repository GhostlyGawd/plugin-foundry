# OPERATIONS — going live

The repo is the database, Actions are the factory, Pages is the window, Stripe is
the till. One-time human setup, then the machine runs on schedule.

## 0 · Preflight (run this first)
`python3 tools/preflight.py` — one read-only pass that checks everything
checkable from inside the repo (including release-tag drift: local tags the
remote never received) and prints the exact click-list for the rest.
`python3 tools/preflight.py --issue` renders the same facts as a GitHub
checklist and, when `gh` is available, opens/updates a single
`ops: go-live checklist` issue (label `ops-golive`) — tick it from your phone.

## 1 · Put it on GitHub
```bash
cd pluginfoundry && git init -q && git add -A
git commit -m "loop(i0/genesis): seed the workshop"
gh repo create <you>/pluginfoundry --public --source . --push   # public → free Pages,
                                                                # easy marketplace add
```

## 2 · Turn on the window (GitHub Pages)
Repo → Settings → Pages → Source: **GitHub Actions**. Then fill
`foundry/site-config.json`:
- `repo`: `<you>/pluginfoundry`
- `pages_url`: `https://<you>.github.io/pluginfoundry`
Commit + push → `deploy-site.yml` ships the site. It now redeploys on every push —
i.e., every time the AI works.

## 3 · Turn on the factory (scheduled shifts)
On a machine where Claude Code is logged into your Claude subscription (Pro/Max/
Team/Enterprise), run `claude setup-token` and copy the one-year OAuth token it
prints. Repo → Settings → Secrets and variables → Actions → new secret
**`CLAUDE_CODE_OAUTH_TOKEN`** with that value. `run-shift.yml` then runs 3 loop
iterations every 8 hours (edit the cron to match your plan's usage limits — every
shift consumes subscription usage). Run one manually first: Actions → *Run shift*
→ Run workflow. Halt anytime by committing a `STOP` file; resume by deleting it.
Renew the token before it expires (~1 year) or shifts start failing loudly.

## 4 · Open the request box (optional, ~15 min)
Follow `services/commission-worker/README.md` (Stripe Payment Link → Cloudflare
Worker → issues). Paste the payment link into `foundry/site-config.json` →
`stripe_payment_link`. The site's request box goes live on the next deploy; the next
shift starts queueing paid commissions.

## 5 · Watch it
- The site: hero shows the live pulse, last-shift age, journal ticker, roadmap lanes.
- The raw feed: commit history + `state/JOURNAL.md` are the unabridged broadcast.
- Steer: P0s and pitches in `state/BACKLOG.md`; veto by revert; `STOP` to pause.

## 6 · Optional instruments
- **Pageviews without surveillance:** create a free GoatCounter site (no cookies, no
  consent banner needed), put its name in `foundry/site-config.json →
  goatcounter_site`, add the count script per their docs to the window (growth-role
  task, via ADR since it's a template change), and add an Actions secret
  `GOATCOUNTER_TOKEN` so metrics.py can read totals. Skip it and those fields stay
  honestly null.
- **Voting needs nothing:** it's GitHub issues + 👍 reactions; metrics.py already
  reads them with the workflow's own token.

## 7 · Governor & veto (optional, recommended)
- **Spend ceiling:** repo → Settings → Secrets and variables → Actions → *Variables*
  → `LOOP_MONTHLY_BUDGET_USD` (e.g. `25`). Shifts self-skip once the month's ledger
  (`state/BUDGET.jsonl`) hits it; `python3 tools/budget.py report` anytime.
- **Veto window:** dispatch a shift with `mode: pr` and the work lands as a pull
  request — merge to approve, close to veto (leave a note). The pr-gated-publishes
  experiment decides whether scheduled shifts switch over.
- **Subscribe:** the window serves `feed.xml` (Atom) — ships, as they happen.

## 8 · Community & fuel (optional wiring)
- **Sponsor button:** edit `.github/FUNDING.yml` (uncomment `github: [your-handle]`)
  and enroll in GitHub Sponsors. The window's fuel gauge reads the ledger; set
  `monthly_budget_usd` in foundry/site-config.json to mirror your Actions variable
  so the gauge shows a cap bar. Shipnotes credit fuel — never invent it.
- **Shipnote:** posts itself Mondays (shipnote.yml). Watch the repo to receive it.
- **Commission tiers:** when ready, create the rush/sponsor Stripe links and follow
  foundry/records/commission-tiers.md — the worker maps link → label.

## Costs & candor
- Shifts run on your Claude subscription (cadence × iterations × model = your usage;
  the BUDGET.jsonl ledger records Claude Code's computed per-iteration cost, which
  under subscription auth is a usage gauge, not a separate bill).
- Actions minutes and Pages are free for public repos; the Worker rides Cloudflare's
  free tier.
- The commission promise, everywhere it appears: priority + a serious attempt at the
  full bar — never guaranteed delivery. Refund policy is yours to set in Stripe.

## 9 · Auth — one surface, swappable (AUTH-1, ADR-031)

`tools/auth.py` is the only place credentials are interpreted. Modes:
`ANTHROPIC_API_KEY` → **api** (takes precedence, dollar governor rules) ·
`CLAUDE_CODE_OAUTH_TOKEN` → **subscription** (quota governor v2 rules) ·
neither on your laptop → **local-login** (claude's own keychain) · neither in
CI → the shift **fails loudly with the remedy** (never a silent no-op — the
2026-07-07 lesson). `auth.py probe <log>` classifies a failed run as
auth-shaped or not; loop.sh halts on the FIRST auth failure.

**Migration to API billing is a secrets change, zero code:** add
`ANTHROPIC_API_KEY`, remove the OAuth secret. Do it the moment ANY of the four
hard triggers fires (MASTER.md §2): token rejected in CI · weekly-limit lockout
>1 day · third-party input reaches the write-capable agent · the always-on
loop goes public.
