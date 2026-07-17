#!/usr/bin/env python3
"""Interactive-session boundary and historical auth-failure classifier.

Model work is allowed only in a live, attended local session (ADR-032). This
module never reads an API key, OAuth token, browser session, or Codex credential.
The host application owns its local sign-in state.

  auth.py check            exit 0 for a local session, 1 in CI
  auth.py probe <log...>   exit 2 for an auth-shaped historical failure,
                           0 when no auth signature is present
"""
import os
import re
import sys

AUTH_SIGNATURES = (
    r"oauth token .*(expired|revoked|invalid|rejected)",
    r"token .*(expired|revoked|invalid)",
    r"authentication[_ ]error",
    r"invalid.*api.?key",
    r"\b401\b",
    r"not logged in",
    r"please run /login",
    r"credit balance is too low",
    r"oauth.*(denied|unauthorized)",
)

INTERACTIVE_REMEDY = """auth: REMEDY — keep model work local and attended.
  1. Open this repository in the interactive Codex or other coding-agent UI.
  2. Sign in through that application's normal local flow if prompted.
  3. Complete one reviewed task and submit it through a pull request.
  Never copy a local session credential into GitHub, CI, logs, or this repo."""


def mode():
    """Report only the execution context; never inspect credential state."""
    return "blocked-ci" if os.environ.get("CI", "").strip() else "interactive-local"


def cmd_check():
    current = mode()
    if current == "blocked-ci":
        print("auth: FAIL — CI/headless model execution is disabled (ADR-032)")
        print(INTERACTIVE_REMEDY)
        return 1
    print("auth: OK — mode interactive-local; the host application owns sign-in")
    return 0


def cmd_probe(paths):
    text = ""
    for path in paths:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text += handle.read().lower() + "\n"
        except OSError:
            continue
    if not text.strip():
        print("auth: probe — no log content to classify")
        return 0
    for signature in AUTH_SIGNATURES:
        match = re.search(signature, text)
        if match:
            print(f"auth: AUTH FAILURE identified in historical run log — matched "
                  f"/{signature}/ (…{match.group(0)[:80]}…)")
            print(INTERACTIVE_REMEDY)
            return 2
    print("auth: probe — failure is not auth-shaped (see the run log itself)")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in ("check", "probe"):
        print(__doc__)
        return 1
    if argv[0] == "check":
        return cmd_check()
    return cmd_probe(argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
