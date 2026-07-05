# BRAND — Identity (pre-brand)

**Status: PRE-BRAND.** "The Foundry" is a codename. The catalog ships as an unbranded
*job-traveler card* — the kraft tag riveted to work moving down a line — until the
workshop earns its name. The system chooses its own identity; that's the point.

## The name — NIGHTSHIFT FOUNDRY (ADR-011)

```
 _  _ ___ ___ _  _ _____ ___ _  _ ___ ___ _____
| \| |_ _/ __| || |_   _/ __| || |_ _| __|_   _|
| .` || | (_ | __ | | | \__ \ __ || || _|  | |
|_|\_|___\___|_||_| |_| |___/_||_|___|_|   |_|  F O U N D R Y
```

Why it holds: the whole operation runs in *shifts* while no one is on the floor —
the name says what the product is (a factory on the night shift) in vocabulary the
system already speaks (shifts, ON AIR, the floor). Ownable, implies no affiliation
with Anthropic, reads at every size. The marketplace slug stays `foundry` forever
(names-are-forever law); install lines never change.

## The Naming Ceremony (Designer, bootstrap item B7 — deliberately early)
The marketplace name travels with every install instruction
(`/plugin install x@NAME`), and published plugin slugs are immutable — so the
ceremony happens before anything spreads:
1. ≥ 8 candidates; test each: pronounceable, collision-scarce, meaningful to
   *plugins/workshops/lines*, comfortable after the `@` in an install command.
2. Choose; record shortlist + reasoning as an ADR.
3. Set `name` in state/STATE.json AND in `.claude-plugin/marketplace.json`; update
   README + catalog header + every install snippet.
4. ASCII wordmark (must survive a terminal) plus styled catalog form.
5. Brand v1 here: 4–6 named palette hexes, type roles, voice (3 adjectives + 3
   banned clichés — "supercharge" is pre-banned), one signature element.

## Standing constraints (survive any rebrand)
- The pipeline strip (stage counts) stays legible at a glance, whatever the brand.
- Install commands render as copyable code, always.
- Voice: specific over clever; a plugin card says what fires and when, not adjectives.
- Rebrands after anything is published require an Auditor-endorsed ADR and never
  rename published plugin slugs.

## Themes of the month
On the Designer's first pass of each calendar month: pick a theme (one noun-phrase +
one sentence of intent), record it as an ADR, set it in `state/STATE.json` under
`theme` as `{"name": …, "month": "YYYY-MM", "note": …}`. The Ideator biases pitches
toward it; the site banners it; the Auditor's monthly read notes whether the theme
produced anything worth keeping. From v5 the community picks it: three candidates
posted as `theme-vote` issues, 👍 decides (see ROLES § designer). Themes steer taste — they never excuse breaking the
quality bar or bumping commissions.
