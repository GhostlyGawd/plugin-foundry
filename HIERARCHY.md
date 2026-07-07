# Visual Hierarchy Audit — the living window & its pages

Read-only audit of the generated catalog. There is no dev server; every screen is
emitted by `tools/build.py` (and `tools/almanac.py`), so the styles that decide
attention are the `<style>` blocks in those templates. Every claim below cites a
selector, token, or measured value from those blocks — line numbers are `tools/build.py`
unless noted.

The product has exactly two jobs to get done on this site: **find a plugin** and
**install it** (or commission the one that's missing). The audit measures whether the
pixels point there. Mostly they point at the machine's own telemetry instead.

---

## 1 — Screen table

| Screen / state | Should win (intended focal point) | Actually wins (by the styles) | The deciding styles |
|---|---|---|---|
| **Home — masthead / above the fold** (`header`…`.tools`) | The value prop + the search-your-task input | The brand H1 and the animated live pulse; the pitch itself is the *quietest* text | `header h1` 22px/ink/2px border (223) vs `.strap` value prop 12.5px `var(--dim)` (238); `.dot` motion `beat` (226,232) |
| **Home — the shelf** (`#grid`, `.tag`) | A plugin card; within it, its **title** and **install** | The repeated ink-filled `.install` block; the title is barely above body copy | `.install{background:var(--ink)}` 11.5px (323) is the highest-contrast fill, drawn ~35×; `.tag h2` only 15px (310) over 14px body (217) |
| **Home — telemetry band** (`.stats`, `.lanebtn`, `.tape`) | Nothing — this is supporting chrome | It out-sizes and out-moves the product: stats are the biggest numbers on the page and the ticker is the only moving thing | `.stat .n` 20px (277), `.lanebtn .n` 19px (288) — larger than any plugin title; `.tape .reel` 55s marquee (253) |
| **Search / clerk result** (`renderClerk`, `.kit`) | The one recommended plugin + its install line | Works — the `.kit` install block is the focal element | `.kit .install` inverted block (333); reasonable |
| **Empty state** (`#empty`) | The "suggest / commission it" recovery link | Fine, but styled `display:none` until triggered and only `var(--dim)` | `.empty{color:var(--dim); text-align:center}` (369) |
| **Plugin detail / certificate** (`p/*.html`) | **What it does + the install command** | The near-black example-transcript terminal; the install command is 12px inline `<code>` in a footer link list | `.term{background:#161310}` (847, darkest pixel on the site) vs install rendered inside `.links` 12px (877, 1035) |
| **Commission + Install duo** (`.duo`, `#request`, `#install`) | One primary: the commission CTA | Two filled attention magnets side by side — blue CTA and dark install blocks | `.cta{background:var(--stamp)}` (364) competes with `.install{background:var(--ink)}` (323) in the neighbouring panel |
| **Queue / Almanac** (`build_queue`, `almanac.py`) | Status of a commission / the month's ships | Legible, but a *different design language* — serif, hard-coded light palette, no dark mode | `body{font:15px/1.7 Georgia,serif; background:#F3ECDA}` (1250; almanac.py:52) |
| **404 / error** | The one link back to the window | Correct — single centred card, one link | `.card` centred grid, one `a` (1280-1288) |

---

## 2 — Findings (ranked, most attention mis-allocated first)

### F1 — The sales pitch is the smallest, dimmest text; the machine's telemetry is the biggest
The value proposition (`.strap`, "A plugin marketplace for Claude Code — two commands to
install anything") renders at **12.5px in `var(--dim)`** (line 238). The three telemetry
stats (`.stat .n`, shipped / on-the-line / 👍 / stars) render at **20px in `var(--ink)`**
(line 277), and the lane counters (`.lanebtn .n`) at **19px** (288). Measured against the
full type scale, only the masthead H1 (22px) is larger than the telemetry — and there are
**three** 20px numbers versus **zero** plugin titles above 15px. Importance is inverted:
the loudest, largest, highest-contrast type is spent on the workshop admiring its own
dashboard, while the reason to stay is whispered. *(Lenses 1, 3, 4.)*

### F2 — Motion is spent entirely on chrome
The only two animated elements on the home screen are the live pulse `.dot`
(`animation:beat`, 226/232) and the journal ticker `.tape .reel` (`animation:reel 55s`,
253). Motion is the strongest pre-attentive signal a page has — and both instances are
telemetry, not the shelf. Squint at the page and your eye is dragged to a scrolling
marquee of journal entries, never to a plugin. The grid, the actual product, is inert.
*(Lenses 1, 4, 7.)*

### F3 — "Primary" is applied dozens of times, so nothing is primary
The single highest-contrast treatment on the site is the inverted `.install` block
(`background:var(--ink); color:var(--paper)`, 323). It is rendered **once per published
card — ~35 times** — plus in kits, the front-desk clerk, and the install panel. A treatment
repeated 35× cannot signal "the action"; it becomes wallpaper. Meanwhile the genuine
convert-me button, `.cta` (`background:var(--stamp)`, 364), sits in the `.duo` *beside* a
panel full of these ink blocks (`#install`), so the two compete. Two filled primaries in
one row is zero primaries. *(Lens 2.)*

### F4 — On the detail page, the install command — the whole point — is invisible
`build_pages` puts the conversion action inside the `.links` list as plain inline code:
`install: <code>/plugin install …@mp</code>` (line 1035), and `.links` is **12px**
(877). Directly above it, the CI transcript renders in `.term` at `background:#161310`
(847) — the darkest, highest-contrast surface anywhere in the codebase — inside an
`<details open>`. The page reserves its maximum contrast for a *demo* and gives the
*install command* less weight than the surrounding link text. A visitor who decides "yes"
has to hunt for how. *(Lenses 1, 4, 5.)*

### F5 — The card title barely wins its own card
Inside `.tag`, the title `h2` is **15px** (310) against **14px** body (217) — a 1px
step. The elements around it borrow weight it should own: the `.ver` badge is a colored,
**`transform:rotate(-2deg)`** stamp (307-308) whose novelty pulls the eye to a *version
number*, and the `::before` faux binder-hole (302) adds decoration next to the title.
The card's own headline is the least-emphasized way importance is encoded on it. *(Lenses 1, 3.)*

### F6 — The masthead is a status bar wearing a storefront's clothes
`header` (221-235) packs the brand H1 beside `.pulse` (live dot), `iteration` and
`phase` counters, and an `.alarms` slot. Three of those five items are process telemetry
that a plugin shopper cannot act on. They share the top border-bottom:2px ink rule with
the title, so they read as peers of the brand. The most valuable strip of the page — the
first thing rendered — is half-consumed by the machine's internal state. *(Lenses 1, 6, 7.)*

### F7 — Everything is boxed, so boxing no longer means anything
`.tag`, `.col`, `.panel`, `.kit`, `.vrow`, `.hrow`, `.field`, `.trust`, `.stat`,
`.lanebtn` each carry their own `1px`/`1.5px solid var(--line)` border. When every group
is a bordered box, the border stops grouping — it's texture, not signal — and the eye gets
no help ranking a plugin card against a vote row against a stat cell. Whitespace, which
`build.py` almost never uses (padding is 8-16px throughout, gaps 6-14px), would separate
these for free without adding contrast noise. *(Lenses 6, 7.)*

### F8 — Emphasis is reinvented per page — three design languages
The same concept — "this is important" — is styled three incompatible ways:
- **index / detail / saga / embed / 404**: monospace, `--paper/--ink/--stamp` tokens,
  full `prefers-color-scheme:dark` support (206-213).
- **queue / almanac**: `Georgia, serif`, **hard-coded** `#F3ECDA` / `#2C2820`, **no dark
  mode** (1250; almanac.py:52-55) — these two pages will glow white in a dark viewport.
- **theater**: dark terminal, amber accent `#B07818` (1171-1178).

A call-to-action is a blue filled `.cta` on the home page and a `#7A4A12` serif underline
on the queue. There is no single convention for what "act here" looks like, so the visitor
re-learns the hierarchy on every navigation. *(Lens 8.)*

### F9 — The sticky jump-nav is 11 equal-weight links that never yield the viewport
`.jump` is `position:sticky; top:0` (240) with **11 anchors**, every one `.jump a`
identical `color:var(--ink)` (243). It permanently occupies the top of the scroll with a
row of same-weight targets — no priority among them, and it competes with `h3.rule`
section headers below (which are only 12px dim, 297). Persistent chrome with a flat
internal hierarchy. *(Lenses 5, 7.)*

---

## 3 — Fixes (ranked by attention reclaimed ÷ lines of CSS; demotions first)

Hierarchy is subtraction. Almost every fix below **quiets something that shouts**, which is
cheaper and safer than promoting signal.

| # | Fix | Change | Lines | Reclaims |
|---|---|---|---|---|
| 1 | **Demote telemetry type** | `.stat .n` 20→15px (277); `.lanebtn .n` 19→14px (288) so no dashboard number outsizes a plugin title | 2 | F1 — stops the biggest type advertising internal stats |
| 2 | **Stop spending motion on chrome** | Drop the `.dot` `beat` animation (232) and the `.tape .reel` marquee (253) for all users, not just reduced-motion; let the ticker sit static | ~2 | F2 — returns the eye's strongest cue to the grid |
| 3 | **Promote the plugin title** | `.tag h2` 15→18px + `font-weight:600` (310); this is the one *promotion* worth its bytes | 1 | F5 — the card's headline finally wins its card |
| 4 | **Quiet the version stamp** | Remove `transform:rotate(-2deg)` and the stamp border from `.ver` (307-308); make it dim text, not a colored badge | 1 | F5 — stops a version number out-shouting the title |
| 5 | **Make the detail install the loudest thing** | In `build_pages`, render the install command in an `.install` block at the top of the sheet instead of inline `<code>` in `.links` (1035); optionally collapse `.term` (`<details open>`→closed) | ~3 | F4 — the conversion action becomes the focal point it should be |
| 6 | **One primary in the duo** | Keep `.cta` filled (364); restyle the neighbouring `#install` blocks as quiet mono code (border only, no ink fill) so a single filled element leads the row | ~2 | F3 — resolves the two-primaries collision |
| 7 | **Thin the masthead** | Move `iteration`/`phase`/`.pulse` out of `header` into the existing `#pulse` telemetry section (221-235 markup); leave brand + value prop up top | markup | F6 — hands the most valuable strip back to the pitch |
| 8 | **Replace borders with space in one place** | Drop the border on `.stat`/`.lanebtn` dividers and lean on gap; prove the pattern, then spread it | ~2 | F7 — lets boxing mean "important" again |
| 9 | **Unify the outliers** | Give `queue`/`almanac`/`theater` the `--paper/--ink/--stamp` tokens + dark-mode block already used by index | ~6 | F8 — one emphasis vocabulary sitewide |

Highest leverage: **#1 and #2** — four lines that stop the loudest, only-moving elements
from being pure telemetry, instantly re-pointing the squint test at the shelf.

---

## 4 — The one rule this codebase should adopt

> **Size, contrast, and motion are reserved for the two things a visitor does here — find a
> plugin and install it. Telemetry never renders larger than a plugin title, and motion is
> never spent on chrome.**

The workshop's defining virtue is honesty — it shows its own machinery proudly. But pride in
the machinery has leaked into the *visual weight*: the dashboard is bigger, brighter, and the
only thing moving, while the shelf and the install command sit quiet. This one rule keeps the
telemetry (it is part of the brand) without letting it borrow the emphasis that belongs to the
product. Everything already has a place; this rule just decides who gets to be loud.

---

*Report only — no styles were changed. Which fixes should I make? I'd start with #1 and #2
(four lines, biggest reclaim), then #3–#5 for the shelf and detail conversion path.*
