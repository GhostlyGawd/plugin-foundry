#!/usr/bin/env python3
"""restamp — weekly re-verification stamps for published records.
Runs the full qa suites; records whose suites pass get verified: <today>.
Metadata-only writes (ADR-013): no version bump, no plugin files touched.
RESTAMP_DRY=1 prints intent without writing.
Pure helpers (parse_failed, stamp_text) are unit-tested; main() is CI-run only —
suites must never call main(), or qa would recurse into qa."""
import datetime, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def parse_failed(qa_stdout):
    """Suite names with at least one fail line."""
    return set(re.findall(r"^\s*\[([\w-]+)\] fail:", qa_stdout, re.M))


def stamp_text(t, today):
    """Update or insert verified: in a record's front matter. Returns new text
    (unchanged if the record already carries today's stamp)."""
    if re.search(r"^verified: ", t, re.M):
        return re.sub(r"^verified: .*$", f"verified: {today}", t, count=1, flags=re.M)
    return t.replace("components:", f"verified: {today}\ncomponents:", 1)


def main():
    dry = os.environ.get("RESTAMP_DRY") == "1"
    qa = subprocess.run(["bash", "tools/qa.sh"], capture_output=True, text=True, cwd=ROOT)
    failed = parse_failed(qa.stdout)
    today = datetime.date.today().isoformat()
    stamped, held = [], []
    for p in sorted((ROOT / "foundry" / "records").glob("*.md")):
        t = p.read_text()
        if not re.search(r"^stage: published$", t, re.M):
            continue
        name = re.search(r"^name: (.+)$", t, re.M).group(1)
        if not (ROOT / "foundry" / "tests" / name).is_dir():
            continue
        if name in failed:
            held.append(name)
            continue
        t2 = stamp_text(t, today)
        if t2 != t:
            stamped.append(name)
            if not dry:
                p.write_text(t2)
    mode = "DRY " if dry else ""
    print(f"restamp {mode}→ stamped {len(stamped)}: {', '.join(stamped) or '—'}"
          + (f" · FAILED suites (alarm these): {', '.join(sorted(held))}" if held else ""))
    return 1 if held else 0


if __name__ == "__main__":
    sys.exit(main())
