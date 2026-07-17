#!/usr/bin/env bash
# Repository/privacy boundary: generated pages must stay same-origin and every
# inline script must match the CSP hash emitted by tools/build.py.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO"

python3 - <<'PY' \
  && echo "ok: every generated HTML page has a matching script-hash CSP" \
  || echo "fail: generated HTML privacy/CSP baseline"
import base64, hashlib, pathlib, re

pages = sorted(pathlib.Path("site").rglob("*.html"))
assert pages
for path in pages:
    text = path.read_text(encoding="utf-8")
    assert text.count('name="referrer" content="no-referrer"') == 1, path
    match = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', text)
    assert match, path
    policy = match.group(1)
    assert "connect-src 'self'" in policy, path
    assert "object-src 'none'" in policy, path
    assert "script-src 'unsafe-inline'" not in policy, path
    scripts = re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", text, re.I)
    expected = {
        "sha256-" + base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode("ascii")
        for s in scripts
    }
    declared = set(re.findall(r"sha256-[A-Za-z0-9+/=]+", policy))
    assert declared == expected, (path, declared, expected)
PY

python3 - <<'PY' \
  && echo "ok: storefront makes no third-party resource or background request" \
  || echo "fail: storefront added a cross-origin resource/request"
import pathlib, re
bad = []
for path in pathlib.Path("site").rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    for pattern in (r'<(?:script|img|iframe)[^>]+src=["\']https?://',
                    r'url\(["\']?https?://', r'fetch\(["\']https?://'):
        if re.search(pattern, text, re.I):
            bad.append((str(path), pattern))
assert not bad, bad
PY

if grep -qi 'analytics' PRIVACY.md \
  && grep -q 'private vulnerability reporting' SECURITY.md \
  && grep -q 'privacy.html' site/index.html \
  && test -f site/privacy.html; then
  echo "ok: privacy and private-reporting disclosures are visible"
else
  echo "fail: privacy/security disclosure missing"
fi

if grep -qx '.env' .gitignore \
  && grep -qx '\*.pem' .gitignore \
  && grep -qx '\*.key' .gitignore \
  && grep -qx 'credentials.json' .gitignore; then
  echo "ok: common local credential artifacts are ignored"
else
  echo "fail: credential ignore baseline drifted"
fi
