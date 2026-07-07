# Dep-Bump Brief

One skill, `dep-brief`: point it at a dependabot/renovate branch and get a
plain-language review brief — `old → new` with semver distance, the **real
files in your repo** that use each bumped package (your "what to check" list),
and changelog notes read honestly: if a changelog isn't reachable, the brief
says `changelog not checked` instead of guessing.

## Install

```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install dep-bump-brief@foundry
```

## Recipes
- "review this dependabot PR" → per-bump brief + risk line, pasteable into the review
- "what changed in this bump?" → old → new, semver distance, your usage sites
- "is this lodash bump safe?" → MAJOR/minor/patch flag + the files that import it

## Honest disclosures
- **Never invents version facts.** Changelog content appears only when the
  changelog was actually read; otherwise you get `changelog not checked`.
- Reads your repo (git diff + grep) and, when available, public changelogs.
  Writes nothing.
- Covers js / python / rust / go manifests; anything else, it says so.

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update dep-bump-brief`
- **Disable / re-enable:** `claude plugin disable dep-bump-brief` / `claude plugin enable dep-bump-brief` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall dep-bump-brief` — removes everything the plugin added
