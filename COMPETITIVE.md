# COMPETITIVE — Gap Scan

*Brief 10 (Competitive Gap Scan). Unlike the SaaS-shaped funnel brief, this one fits
almost unchanged: `plugin-foundry` really is a Claude Code plugin marketplace with
real, findable rivals. Read the repo, searched the web; the only write is this file.
Evidence is cited inline. The ecosystem is <1 year old (Claude Code plugins launched
2025), so **catalog counts conflict by source and date — treat every number as
directional and dated, never precise.***

---

## 1 — Arena summary

**Category.** Third-party **Claude Code plugin discovery + distribution**: a GitHub repo
carrying `.claude-plugin/marketplace.json`, added with `/plugin marketplace add owner/repo`
and installed with `/plugin install <name>@<marketplace>`. Anthropic's own docs define
this exact two-step surface ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)).
Anyone can add any repo — there is **no gatekeeper on "add."** So the battleground is
**discovery and trust, not distribution rights.**

**Audience.** A Claude Code user (a developer) who wants ready-made skills / agents /
hooks / commands and will paste two commands to get them. Our specific wedge inside that
audience: people who feel the *signal-to-noise pain* of the mega-catalogs and want small,
single-job, trustworthy tools (our published line is repo-hygiene: commits, PRs, TODO
ledgers, test-gap nudges, dep-bump briefs — `.claude-plugin/marketplace.json`).

**The rivals a prospective user actually compares (one line each):**
- **Anthropic Official** (`claude-plugins-official`) — the curated, *pre-installed* directory, "official, Anthropic-managed, high quality." ([github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official))
- **Anthropic Community** (`claude-plugins-community`) — Anthropic-operated firehose of third-party plugins passed through **automated safety screening + commit-SHA pinning**. Our closest structural mirror. ([discover-plugins](https://code.claude.com/docs/en/discover-plugins))
- **davila7 / claude-code-templates** (aitmpl.com) — the community "de facto package manager": a CLI + web catalog with a live session/monitoring dashboard. ~28.5k stars. ([github.com/davila7/claude-code-templates](https://github.com/davila7/claude-code-templates))
- **wshobson / agents** — big single-author curated marketplace across many harnesses; ~36.6k stars but **"no releases, catalog churns fast."** ([rywalker.com/research/wshobson-agents](https://rywalker.com/research/wshobson-agents))
- **hesreallyhim / awesome-claude-code** — the strictest curated **list** (browse-only, no `marketplace.json`); submissions by issue-form, **PRs banned**. ([CONTRIBUTING.md](https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md))

**Adjacent (shapes buyer trust, not a direct rival):** MCP server registries — Smithery
(~7k, freemium, **pays creators $0**), Glama (~52k, automated), PulseMCP (~21k), the
official MCP registry (metadata-only, preview Sept 2025). They catalog *servers that wire
AI to SaaS*; they do **not** catalog local workflow/skill plugins like ours. Overlap =
connector plugins only. ([truefoundry.com/blog/best-mcp-registries](https://www.truefoundry.com/blog/best-mcp-registries))

---

## 2 — Comparison table

*(us = Nightshift Foundry. ✓ = has it, ~ = partial, ✗ = absent. Counts dated mid-2026.)*

| Capability | **Us** | Anthropic Official | Anthropic Community | davila7 | wshobson | awesome-cc |
|---|---|---|---|---|---|---|
| Native `/plugin` 2-step install | ✓ | ✓ (pre-added, ~1 step) | ✓ | ✗ (own `npx` installer) | ✓ | ✗ (list only) |
| Catalog size | 10, focused | 36→101, curated | hundreds, screened | 100–400+ | 88 plugins | hundreds |
| Curation model | **autonomous AI loop + roles** | Anthropic discretion | automated screening | community PRs | single author | issue-form + discretion |
| Quality/usefulness gate before publish | ✓ **TEST + REVIEW verdict** | ~ (opaque) | ✗ (screens *safety*, not usefulness) | ✗ | ✗ | ~ (bot checks *form*, not quality) |
| Integrity (commit-SHA pinning) | ✗ **(gap)** | ~ | ✓ | ✗ | ✗ | n/a |
| Versioning (semver + CHANGELOG) | ✓ **(house law)** | ~ | ~ | ✗ | ✗ ("no releases") | n/a |
| Public, legible process | ✓ **(living window, journal, per-shift cost)** | ✗ | ✗ | ~ (dashboard) | ✗ | ✗ |
| Autonomous origination (AI *builds* the plugins) | ✓ **(unique)** | ✗ | ✗ | ✗ | ✗ | ✗ |
| Portable "verify your plugin" CI badge | ✓ **(foundry-doctor action)** | ✗ | ✗ | ✗ | ✗ | ✗ |
| Monetization | ~ commission ($5.99, not yet wired) + sponsors | ✗ | ✗ | sponsors + BMC | ✗ | ✗ |

Sources for the rival cells: [discover-plugins](https://code.claude.com/docs/en/discover-plugins),
[wshobson README](https://github.com/wshobson/agents), [rywalker](https://rywalker.com/research/wshobson-agents),
[aitmpl](https://www.aitmpl.com), [awesome-cc CONTRIBUTING](https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md).

---

## 3 — Table stakes (ranked by user expectation)

The market minimum a plugin shopper assumes exists. Match these; don't over-invest past them.

| # | Table stake | Evidence it's expected | Us today | Effort to close |
|---|---|---|---|---|
| 1 | Two-command install, copy-pasteable in the README | every native rival shows it verbatim ([discover-plugins](https://code.claude.com/docs/en/discover-plugins)) | ✓ met | — |
| 2 | Free to browse and install | no rival charges for the plugins themselves ([wshobson](https://github.com/wshobson/agents), [aitmpl](https://www.aitmpl.com)) | ✓ met | — |
| 3 | Per-plugin trust disclosure — *what installs, token cost, is it safe* | Anthropic surfaces context-token cost + a "Will install" component list + a "trust before installing" warning ([discover-plugins](https://code.claude.com/docs/en/discover-plugins)) | ~ partial — we have token-cost badges + provenance pages, but the "exactly what will install" inventory isn't front-and-center (see `HIERARCHY.md` F4) | **S–M** |
| 4 | A freshness / maintenance signal | stale lists are the #5 recurring complaint ([claudefa.st](https://claudefa.st/blog/tools/resources/awesome-claude-code)) | ✓ met and then some — continuous loop + last-shift pulse | — |
| 5 | Browsable category taxonomy | both Anthropic marketplaces + davila7 organize this way ([discover-plugins](https://code.claude.com/docs/en/discover-plugins)) | ✓ met (`foundry/categories.json`) | — |
| 6 | Some install-integrity story (SHA pinning) | Anthropic Community pins every plugin to a commit SHA ([discover-plugins](https://code.claude.com/docs/en/discover-plugins)) | ✗ **gap** — single-repo self-hosting lowers the risk, but it's the one stake a security-minded shopper will miss | **M** |

The only real stakes we *lack* are **#3 (make "what installs + its cost" unmissable)** and
**#6 (integrity pinning)**. Everything else is met.

---

## 4 — Differentiation bets

Three moves that turn a **cited rival weakness** into an advantage using something **real in
this repo**. Each traces to a spec'd or shipped capability, not a wish.

**Bet 1 — "Every plugin shows its work."** *Exploits the ecosystem's #1 complaint — no quality
verification; plugins that look polished but output wrong data ([buildtolaunch](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review)).*
Anthropic Community screens for *safety, not usefulness*; awesome-cc's bot validates *form, not
quality*; MCP registries make "no attempt to evaluate quality." We already gate every publish on
**TEST VERDICT: pass + REVIEW: approved** (CLAUDE.md non-negotiable #6), and every plugin has a
**provenance "birth certificate"** page and a **token-cost badge**. The bet: promote a per-plugin
**"tested + reviewed" trust card to the primary card element** (today it's buried — `HIERARCHY.md`
F4), making visible exactly the assurance every rival keeps in a black box. *Ties to: `trust-card`,
`token-cost-badges`, `demo-transcripts` records.*

**Bet 2 — "The marketplace that's never stale, and proves it."** *Exploits stale-list + no-versioning
churn ([rywalker](https://rywalker.com/research/wshobson-agents), [claudefa.st](https://claudefa.st/blog/tools/resources/awesome-claude-code)).*
wshobson has "no releases"; dead lists lose trust. We run a **scheduled loop** with a **semver +
CHANGELOG law** (CLAUDE.md #4) and a live last-shift pulse, a shift-streak heatmap, and a weekly
shipnote. The bet: lead the pitch with **freshness + version discipline** — "maintained, versioned,
and here's the proof" — and *tie the loud telemetry to plugin freshness* so the window's motion
finally advertises the shelf instead of itself (the fix `HIERARCHY.md` already prescribes). *Ties to:
`shift-streak`, `weekly-shipnote`, `releases-and-reverify` records.*

**Bet 3 — "Verify your own plugin against the same laws" as a distribution flywheel.** *Exploits the
total absence of a portable per-plugin verification badge anywhere in the arena.* We already ship the
**`foundry-doctor` GitHub Action** + a **dated verified listing** + an **embeddable badge** (README
"Verify YOUR plugin"). No rival — not even Anthropic — offers a public, portable structural-verification
badge for a Claude Code plugin. The bet: push **verified-by-foundry** as a growth wedge — other repos
run the action, earn a badge, and their badge links back — a trust network the autonomous loop can run
without human sales effort. *Ties to: `verified-by-foundry`, `embed-badges`, `foundry-network`,
`cross-foundry-exchange` records.*

---

## 5 — Do-not-copy list

Things rivals do that would **break** an autonomous single-operator AI workshop:

- **Mega-catalogs / automated star-aggregation** (Glama ~52k, aggregators indexing 14k+ *unverified* plugins). Volume is precisely the pain users cite ([buildtolaunch](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review)); copying it destroys the single-job quality thesis that is our whole differentiation.
- **Paid hosted infrastructure** (Smithery's hosted-server tier). Needs ops/SRE and carries uptime + security liability; wrong shape for a loop that only knows how to ship a git repo. ([truefoundry](https://www.truefoundry.com/blog/best-mcp-registries))
- **Multi-harness sprawl** (wshobson targeting Cursor/Copilot/Gemini/Codex). Multiplies the test surface with no releases — already a cited pain. Own one harness (Claude Code) deeply. ([rywalker](https://rywalker.com/research/wshobson-agents))
- **Ad-monetized directory** (aggregators running sold-out ad slots at 300k visitors/mo). Requires a sales motion and audience scale a niche workshop won't have, and it muddies the transparency brand.
- **PR-based open contribution at scale** (davila7). Merging community PRs is a human review burden that contradicts "autonomous single operator" — awesome-cc even *bans PRs* to stay sane ([CONTRIBUTING.md](https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md)). Our idea-inbox + commission lane is the right shape: intake, don't merge.
- **⚠ Caution (not quite do-not-copy) — per-plugin paid commissions.** *No one* in this space sells per plugin; creators use sponsors / Buy-Me-a-Coffee, and Smithery pays creators nothing. Charging for AI-generated-on-demand plugins imports quality + liability + refund expectations the loop must be able to honor. It's genuinely novel, but it's a differentiator *and* a risk — see `REVENUE.md` (next stage) for the full treatment. ([mcpize.com/alternatives/smithery](https://mcpize.com/alternatives/smithery), [agent37.com/blog/monetize-claude-code-skills](https://www.agent37.com/blog/monetize-claude-code-skills))

---

## Note on evidence quality

Catalog counts move fast and disagree across sources — the official marketplace was reported
at 36 (Dec 2025), then 55+, then 101 (Mar 2026) inside four months; MCP registry sizes span
7k–52k. All rival numbers above are **directional and dated**, cited to a source, and should be
re-checked before any external claim. Where a source couldn't be verified it's marked `~`.

---

*Report only — no changes made. Which moves should we make? My ranking: **Bet 1** (trust card
front-and-center — cheapest, attacks the #1 complaint), then **Bet 3** (verified-by-foundry
flywheel — already built, just needs promotion), then **Bet 2** (freshness positioning). I'd also
close table stake #3 alongside Bet 1 since they're the same surface. Say which, and I'll open them
as backlog items on the normal line — not implement here, given the operator STOP.*
