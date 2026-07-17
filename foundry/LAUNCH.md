# LAUNCH — the concentrated-window playbook (MASTER Stage 3 + §11, ADR-031)

**Operator-executed.** Every post here goes out under *your* identity, from *your*
accounts, on *your* go. The factory prepared the kit to the repo's edge (constitution
Art. I §7 — never impersonate the operator); the desk holds the go-items. Nothing in
here fires autonomously.

**The one rule that beats the rest:** star *velocity*, not totals, drives GitHub
Trending. Concentrate everything into one 24–48h window, **Tue–Thu morning ET**. A slow
drip does not trend.

**Before you post, run `python3 tools/vishot.py narrate`** and paste the current numbers
into the copy below — they must match the live badge (`site/quality.json`). Never post a
number this repo can't substantiate (growth-honesty law). As of this writing the
substantiated headline is: **10 plugins shipped · 86% passed QA first try · 5 builds
bounced-and-fixed in public · 236 recorded iterations**.

---

## T-minus checklist (the 4 weeks before)

- [ ] README first screen final (hook → replay → counter → fork line → org chart) — **done** (GAP-A4).
- [ ] Live window deployed with the quality counter above the fold — **done** (GAP-A/A2); confirm Pages is live.
- [ ] The proof GIF/replay renders in the README on GitHub — **done** (`foundry/assets/replay.svg`, SMIL works in READMEs).
- [ ] `marketplace.json` valid so community crawlers index it — **done** (validator law).
- [ ] Submit to awesome-claude-code + Anthropic community marketplace — prefilled in `foundry/SUBMISSIONS.md` (desk `d-0001`).
- [ ] Pre-write the 2–3 evergreen posts (below).
- [ ] Warm up (don't spam) r/ClaudeAI, r/ClaudeCode, the Anthropic Discord — be a real participant first.

## T-0 — everything in one window (Tue–Thu AM ET)

### Show HN
**Title (factual, no marketing-speak):**
> Show HN: An AI-run software company in a repo that ships cross-host AI plugins

**Body:**
> plugin-foundry is a GitHub repo that runs itself as a small software company. A
> PR-gated Codex workflow invents, builds, tests, reviews, and publishes plugins from one
> shared source to host-native packages for Codex, Claude Code, Gemini CLI, Cursor, and
> GitHub Copilot — and the repo *is* the marketplace they ship to. It's governed by a
> written constitution, a guard that blocks forbidden actions, and a keyless landing job.
>
> It shows its work: every plugin has a public "birth certificate" (the full idea → build
> → QA → review → publish trail), and the headline number is computed only from the repo's
> own records — right now 10 plugins shipped, 86% passed QA on the first try, 5 builds
> bounced by the review gate and fixed in public. The bounces are the point; the gates
> visibly block bad builds.
>
> You can fork the whole company in one command (`fork-a-foundry`).
>
> Honest limits: hosted shifts need a project-scoped OpenAI API key and remain deliberately
> STOP-gated until an operator provisions it and approves a green dry run; the plugins are
> single-job and small; and I'm the human board member, steering by exception. Happy to
> answer anything.

**Rules:** reply to *every* comment for the first 2 hours — velocity in the first 60–90 min
decides the front page. **Never ask for upvotes.** If AI-slop hostility shows up, lead with
the constitution / gates / single-writer story — that fear *is* the opening.

### Reddit (each tailored, GIF/replay-led, be first to comment)
- **r/ClaudeAI** (~990k) — lead with the replay and "it caught its own bug." Community-first tone.
- **r/ClaudeCode** — lead with the two-command install and the fork loop; this crowd builds.
- **r/SideProject** — lead with the "AI runs a company in a repo" premise.
- **r/coolgithubprojects** — the repo + one-line pitch.
Obey each sub's 90/10 self-promo rule; you've been participating for weeks by now.

### X thread
1. The premise + the replay GIF: "I built a repo that runs itself as a software company…"
2. The proof counter (substantiated), the birth-certificate idea.
3. The governance story (constitution, guard, single-writer) — why it doesn't go rogue.
4. The fork loop: `fork-a-foundry`, one command → your own foundry. Link.

### Submit (their intake forms only — never a PR from the factory)
- awesome-claude-code — prefilled link in `foundry/SUBMISSIONS.md`.
- Anthropic community marketplace — form at https://code.claude.com/docs/en/discover-plugins (the single biggest credibility unlock).

## T+1 to T+2 weeks
- Newsletters: **Console** (curates OSS *before* it blows up), TLDR, Changelog, Pointer, ClaudeLog.
- A YouTube demo (screen-record a real shift).
- Publish the evergreen posts.
- **Pursue the official Anthropic marketplace** — put acceptance above the fold when it lands.

---

## Evergreen posts (problem-first, pre-write these)
1. *"We're about to drown in AI-generated plugins. Here's the governance that stops one repo from being part of the problem."* (constitution, guard, the visible bounce.)
2. *"A quality number you can't fake: how the foundry computes 86% first-try from its own records."*
3. *"Single-writer, multi-agent: why the factory's writes are serialized"* (the Cognition/Anthropic debate resolution).

## The thresholds that change the plan (§11)
- **<50 stars/day at launch** → the *story/README* is the problem, not the channels. Re-test the one-liner and the replay before spending more launch capital.
- **Hits GitHub Trending** → immediately double down on newsletters + the official-marketplace application to convert the spike into a base.
- **AI-slop hostility in comments** → pivot messaging to lead with constitution/gates/single-writer.
- **Accepted to Anthropic's official marketplace** → that becomes the headline credibility asset, above the fold.

## Anti-patterns (constitution-backed)
- ❌ **Never buy stars.** Detected, removed, fatal to credibility with this exact audience.
- ❌ **Never auto-open PRs against other people's repos** (Art. I §1).
- ❌ Don't hide the AI-generated nature — **lead with the governance story**; the honest "here's how we prevent it going rogue" framing is what converts skeptics.
