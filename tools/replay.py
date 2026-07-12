#!/usr/bin/env python3
"""replay.py — the proof artifact (MASTER GAP-A3, ADR-031).

Generates foundry/assets/replay.svg: a looping, SMIL-animated replay of a REAL
production arc from the records — idea → build → QA → **review gate blocks the
bad build** → fix + pinned regression → re-test → approved → published. Every
line is quoted or tightly paraphrased from foundry/records/starter-kits.md
(iterations i89–i93) and the frame is labeled REPLAY — the honesty laws allow
sped-up truth, never simulation. The gate-blocks frame is the point: it proves
autonomous + real + safe in one glance (the slop-skeptic converter).

Deterministic output (no clocks, no randomness) so builds don't churn.
SMIL animates in every browser and inside GitHub READMEs (no JS needed).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "foundry" / "assets" / "replay.svg"

# (badge, badge_color, lines, accent) — all facts from starter-kits.md
FRAMES = [
    ("SHIFT — ideator", "#8a6d3b",
     ["starter-kits — curated bundles of shelf plugins,",
      "one copy-block installs the whole kit"], "#221c14"),
    ("BUILD — builder", "#8a6d3b",
     ["kit rail built: renderKits() —",
      "only PUBLISHED members emit install lines;",
      "pending ones say “finishing on the line”"], "#221c14"),
    ("QA — three-tier pass", "#2e6b34",
     ["probed: empty kits array, only-unpublished kit,",
      "member-flag honesty  ·  defects: none",
      "TEST VERDICT: pass → rc"], "#2e6b34"),
    ("REVIEW i89 — GATE BLOCKS", "#a33327",
     ["REVIEW: bounced — multi-line kit copy-block",
      "collapses to one unrunnable line",
      "✖ does not ship"], "#a33327"),
    ("FIX i90 — builder", "#8a6d3b",
     ["scoped fix: .kit .install{white-space:pre}",
      "+ an EXECUTABLE regression pinning the i89 bounce"], "#221c14"),
    ("RE-TEST i91 · REVIEW i92", "#2e6b34",
     ["re-test: pass · regression suite green",
      "REVIEW: approved — bounce cured,",
      "regression executable, copy honest"], "#2e6b34"),
    ("PUBLISHED i93 — maintainer", "#1d5c8a",
     ["starter-kits v0.1.0 → live on the shelf",
      "marketplace.json synced · release tag laid",
      "✔ installed users receive it"], "#1d5c8a"),
]

W, H = 720, 200
DUR = 2.6          # seconds per frame
TOTAL = DUR * len(FRAMES)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame_svg(i, badge, badge_color, lines, accent):
    begin = i * DUR
    vis = (f'<animate attributeName="opacity" dur="{TOTAL}s" repeatCount="indefinite" '
           f'calcMode="discrete" keyTimes="0;{begin / TOTAL:.4f};{(begin + DUR) / TOTAL:.4f}" '
           f'values="{"1" if i == 0 else "0"};1;0"/>'
           if i < len(FRAMES) - 1 else
           f'<animate attributeName="opacity" dur="{TOTAL}s" repeatCount="indefinite" '
           f'calcMode="discrete" keyTimes="0;{begin / TOTAL:.4f}" values="0;1"/>')
    text = "".join(
        f'<text x="34" y="{96 + j * 24}" font-family="ui-monospace,Menlo,monospace" '
        f'font-size="15" fill="{accent}">{esc(ln)}</text>'
        for j, ln in enumerate(lines))
    return (f'<g opacity="0">{vis}'
            f'<rect x="24" y="52" rx="6" width="{len(badge) * 8 + 26}" height="24" fill="{badge_color}"/>'
            f'<text x="37" y="69" font-family="ui-monospace,Menlo,monospace" font-size="12.5" '
            f'font-weight="bold" fill="#f6efe2">{esc(badge)}</text>'
            f'{text}</g>')


def main():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace,Menlo,monospace" role="img" '
        f'aria-label="Replay of real foundry iterations i89-i93: the review gate blocks a bad build, the fix ships with a pinned regression.">',
        f'<rect width="{W}" height="{H}" rx="12" fill="#f6efe2"/>',
        f'<rect width="{W}" height="{H}" rx="12" fill="none" stroke="#d9c9a8" stroke-width="2"/>',
        f'<circle cx="24" cy="24" r="5" fill="#a33327"/>',
        f'<circle cx="42" cy="24" r="5" fill="#c9a227"/>',
        f'<circle cx="60" cy="24" r="5" fill="#2e6b34"/>',
        f'<text x="80" y="29" font-size="13" fill="#6b5d49">nightshift foundry · one plugin, walked down the line</text>',
    ]
    parts += [frame_svg(i, *f) for i, f in enumerate(FRAMES)]
    parts += [
        f'<text x="24" y="{H - 14}" font-size="11" fill="#6b5d49">'
        f'REPLAY · real iterations i89–i93 · every line from '
        f'foundry/records/starter-kits.md · sped up</text>',
        "</svg>",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(parts) + "\n")
    print(f"replay: wrote {OUT.relative_to(ROOT)} — {len(FRAMES)} frames, "
          f"{TOTAL:.0f}s loop, gate-block frame included")


if __name__ == "__main__":
    main()
