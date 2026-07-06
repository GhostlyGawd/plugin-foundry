"""lib.py — shared helpers for the gates (v10 #8, ADR-018). One front-matter
parser, one truth: validate.py consumes it strictly (errors reported),
build.py and clerkcat.py leniently. The _tools fixture suite guards it."""


def parse_front_matter(text, errors=None, label=""):
    """Parse leading ``---`` front matter. Returns ``(meta, body)``.

    Pass ``errors`` (a list) for strict mode: malformed input appends
    ``f"{label}: <problem>"`` messages. Without it, parsing is lenient —
    problems are skipped and the function returns what it can.
    Values in ``[a, b]`` form become lists; inline ``  # comments`` after a
    value are stripped."""
    def err(msg):
        if errors is not None:
            errors.append(f"{label}: {msg}")

    if not text.startswith("---"):
        err("missing front matter")
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        err("unterminated front matter")
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            err(f"bad front matter line: {line!r}")
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.split(" #")[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = raw
    return meta, parts[2]
