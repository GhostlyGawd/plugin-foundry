# VISION — North Star

The Foundry exists to run the best small plugin marketplace for Claude Code: every
plugin scoped to one job, prompt-crafted, token-thrifty, hook-safe, tested against its
own spec, and installable in two commands from this very repository.

A visitor should be able to open the catalog, read a plugin card, run
`/plugin marketplace add <this repo>` + `/plugin install <name>@<marketplace>`, and
trust what loads — because the workshop that built it also tried to break it.

## What "great" means here
- **One job per plugin.** Component count is a cost, not a feature list.
- **Descriptions are the product's front door.** Claude auto-invokes skills and agents
  from their descriptions; we write those like they decide everything, because they do.
- **Token thrift.** Always-on context cost is a budget line, not an afterthought.
- **Hooks are guests.** They run on strangers' machines and behave like it.
- **Version discipline.** Published means maintained: semver bumps, changelogs,
  deprecations with migration notes.
- **Dogfooded.** The Foundry works with its own tools and journals the friction.

## Milestones
- **M1 — Line proven.** Bootstrap done: commit-craft walked spec→published; two
  plugins live; brand v1 named; first audit filed.
- **M2 — Working marketplace.** 8 published plugins across ≥4 categories, at least
  one each shipping skills, agents, and hooks; every published plugin has survived a
  post-publish QA re-test; first deprecation handled cleanly.
- **M3 — Reference workshop.** 20+ published; token-cost budgets enforced in QA;
  shelf and deprecation notes teaching; outside users installing (README tells them how).

Counts are floors. The health metrics that matter: QA defect-find rate and reviewer
bounce rate — proof the line still inspects instead of waving through.
