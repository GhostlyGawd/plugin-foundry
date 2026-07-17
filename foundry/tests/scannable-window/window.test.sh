#!/usr/bin/env bash
set -u

python3 - <<'PY'
import json
import pathlib
import re

html = pathlib.Path("site/index.html").read_text(encoding="utf-8")
data = json.loads(pathlib.Path("site/data.json").read_text(encoding="utf-8"))
index = json.loads(pathlib.Path("site/downloads/index.json").read_text(encoding="utf-8"))

hosts = {"claude-code", "codex", "gemini-cli", "cursor", "github-copilot"}
buttons = set(re.findall(r"\{id:'([^']+)', name:'[^']+'", html))
print(("ok: " if buttons == hosts else "fail: ") + "five host choices render from one selector")

packages = data.get("packages", [])
complete = len(packages) == 10 and all(set(p.get("packages", {})) == hosts for p in packages)
same = packages == index.get("plugins", [])
files = all((pathlib.Path("site/downloads") / pkg["file"]).is_file()
            for plugin in packages for pkg in plugin["packages"].values())
print(("ok: " if complete and same and files else "fail: ") +
      "site data exposes all 50 digest-indexed native packages")

a11y = ('role="group" aria-label="Choose a coding-agent host"' in html and
        'aria-pressed="' in html and 'aria-live="polite"' in html and
        'section[id]{scroll-margin-top:72px}' in html)
print(("ok: " if a11y else "fail: ") + "host selector and anchored sections are keyboard-readable")

privacy = ('<script src=' not in html and 'localStorage' not in html and
           'sessionStorage' not in html and 'No analytics or tracking.' in html)
print(("ok: " if privacy else "fail: ") + "host choice adds no tracking, storage, or remote script")

portable = ("Everything happens inside Claude Code" not in html and
            "Claude Code is Anthropic's AI coding assistant" not in html and
            "Pick your host. Get the native package." in html)
print(("ok: " if portable else "fail: ") + "primary product journey is cross-host")
PY

if command -v node >/dev/null 2>&1; then
  python3 - <<'PY' | node --check - >/dev/null \
    && echo "ok: storefront script parses" \
    || echo "fail: storefront script syntax"
import re, sys
script = re.search(r'<script>([\s\S]*)</script>', open('site/index.html', encoding='utf-8').read()).group(1)
sys.stdout.buffer.write(script.encode('utf-8'))
PY
else
  echo "skip: node absent; storefront script parse runs in CI"
fi
