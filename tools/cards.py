#!/usr/bin/env python3
"""cards — kraft-styled SVG credit cards, one per credited contributor.
Empty hall generates nothing (empty-renders-nothing law). Self-contained SVG:
system fonts, no external requests."""
import html, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "site" / "card"

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="520" height="200" viewBox="0 0 520 200" role="img" aria-label="Nightshift Foundry contributor card for {login}">
<rect width="520" height="200" fill="#F3ECDA"/>
<rect x="6" y="6" width="508" height="188" fill="none" stroke="#2C2820" stroke-width="3"/>
<rect x="6" y="6" width="508" height="42" fill="#2C2820"/>
<text x="20" y="33" font-family="Georgia, serif" font-size="17" fill="#F3ECDA" letter-spacing="3">NIGHTSHIFT FOUNDRY · CONTRIBUTOR</text>
<text x="20" y="92" font-family="Georgia, serif" font-size="30" fill="#2C2820">@{login}</text>
<text x="20" y="128" font-family="Georgia, serif" font-size="15" fill="#5A5140">{credits}</text>
<text x="20" y="172" font-family="Georgia, serif" font-size="12" fill="#8A7E62">since {since} · every credit above is a line in an append-only ledger</text>
<circle cx="474" cy="96" r="26" fill="none" stroke="#B07818" stroke-width="3"/>
<text x="474" y="102" font-family="Georgia, serif" font-size="16" fill="#B07818" text-anchor="middle">NF</text>
</svg>
"""

def render(hall, records):
    since = {}
    for r in records:
        who = r.get("prospected_by")
        if who:
            d = r.get("created", "")
            since[who] = min(since.get(who, d) or d, d) if since.get(who) else d
    cards = {}
    for p in hall.get("prospectors", []):
        bits = [f"{p['total']} prospect{'s' if p['total'] != 1 else ''}"]
        if p["shipped"]:
            bits.append(f"{p['shipped']} shipped")
        cards[p["login"]] = (", ".join(bits), since.get(p["login"], "?"))
    for who in hall.get("patrons", []):
        c, s = cards.get(who, ("", "?"))
        cards[who] = ((c + ", " if c else "") + "patron", s)
    return cards

def write_all(hall, records):
    if CARD_DIR.exists():
        shutil.rmtree(CARD_DIR)
    cards = render(hall, records)
    if not cards:
        return {}
    CARD_DIR.mkdir(parents=True)
    out = {}
    for login, (credits, since) in cards.items():
        safe = re.sub(r"[^A-Za-z0-9_-]", "", login)
        if not safe:
            continue
        (CARD_DIR / f"{safe}.svg").write_text(SVG.format(
            login=html.escape(login), credits=html.escape(credits), since=html.escape(since)))
        out[login] = f"card/{safe}.svg"
    return out
