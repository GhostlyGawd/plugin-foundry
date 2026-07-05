#!/usr/bin/env python3
"""relnotes — extract exactly one version's section from a CHANGELOG.
Usage: python3 tools/relnotes.py <changelog-path> <version>
Prints the section body (heading included); exits 1 if the version is absent —
a release with no notes is a release that does not happen."""
import pathlib, re, sys

def extract(text, version):
    pat = re.compile(rf"^## {re.escape(version)}\b.*?$", re.M)
    m = pat.search(text)
    if not m:
        return None
    start = m.start()
    nxt = re.compile(r"^## ", re.M).search(text, m.end())
    return text[start: nxt.start() if nxt else len(text)].rstrip() + "\n"

def main(argv):
    if len(argv) != 2:
        print("usage: relnotes.py <changelog-path> <version>", file=sys.stderr)
        return 2
    path, version = argv
    sec = extract(pathlib.Path(path).read_text(), version)
    if sec is None:
        print(f"relnotes: version {version} not found in {path}", file=sys.stderr)
        return 1
    print(sec, end="")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
