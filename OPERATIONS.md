# OPERATIONS — going live

The repo is the database, Actions are the factory, Pages is the window, Stripe is
the till. One-time human setup, then the machine runs on schedule.

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
Repo → Settings → Secrets and variables → Actions → new secret
**`ANTHROPIC_API_KEY`**. `run-shift.yml` then runs 3 loop iterations every 8 hours
(edit the cron to match your credit budget — every shift spends API tokens). Run one
manually first: Actions → *Run shift* → Run workflow. Halt anytime by committing a
`STOP` file; resume by deleting it.

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
- Shifts consume Anthropic API credits (cadence × iterations × model = your bill).
- Actions minutes and Pages are free for public repos; the Worker rides Cloudflare's
  free tier.
- The commission promise, everywhere it appears: priority + a serious attempt at the
  full bar — never guaranteed delivery. Refund policy is yours to set in Stripe.
