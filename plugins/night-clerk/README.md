# Night Clerk

The marketplace's front desk, installed in your terminal. One skill, `clerk`:
ask "what plugin helps with X?" and get up to three real recommendations with
exact install lines — from a bundled catalog snapshot, never from imagination.

## Install
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install night-clerk@foundry
```

## Recipes
- "what plugin helps with commit messages?" → commit-craft, with the install line
- "browse the foundry" → the shelf, three at a time, snapshot date stated
- "find me a plugin for handoffs" → session-recap, or an honest "nothing fits yet" + the idea route

## Honest disclosures
The catalog is a **snapshot** (date stated in every answer), regenerated and
shipped with each clerk release; `/plugin marketplace update` pulls the freshest.
The clerk cannot install anything itself and will never invent a plugin.

See [CHANGELOG.md](./CHANGELOG.md).
