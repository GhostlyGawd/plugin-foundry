#!/usr/bin/env python3
"""auth.py — the single auth surface (MASTER AUTH-1, ADR-031).

No agent, tool, or workflow interprets credentials directly; they ask this
module. Switching subscription → API billing is a secrets change, zero code:

  ANTHROPIC_API_KEY set            → mode "api"     (takes precedence — mirrors
                                                     Claude Code's own behavior)
  CLAUDE_CODE_OAUTH_TOKEN set      → mode "subscription"
  neither, interactive machine     → mode "local-login" (claude's keychain)
  neither, CI                      → FAIL LOUDLY with the remedy

## The four hard migration triggers (MASTER §2, Contradiction 3)
Any ONE of these → switch to API billing (set ANTHROPIC_API_KEY, remove the
OAuth secret) immediately:
  1. The OAuth token is rejected for CI/programmatic use.
  2. A weekly-limit lockout halts the loop for more than 1 day.
  3. Any third-party/untrusted input reaches the write-capable agent.
  4. The always-on loop goes public.

## Why `probe` exists
On 2026-07-07 a rejected token produced a 3-second claude exit whose error
went to a gitignored stdout log — the shift reported success while doing
nothing. `probe` reads a run log and classifies auth-shaped failures so
loop.sh can halt loudly on the FIRST one instead of silently streaking.

  auth.py check            exit 0 usable · 1 none-in-CI (prints the remedy)
  auth.py probe <log...>   exit 2 auth failure identified · 0 not auth-shaped

CI is detected via the CI env var (GitHub Actions sets it).
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

REMEDY_SUBSCRIPTION = """auth: REMEDY — the subscription token was rejected or expired.
  1. On a machine logged into an active Claude subscription: `claude setup-token`
  2. Update the CLAUDE_CODE_OAUTH_TOKEN Actions secret with the FULL value.
  3. Dispatch one shift to confirm, then delete the root STOP file.
  Or switch to API billing (migration trigger #1): set ANTHROPIC_API_KEY and
  remove the OAuth secret — no code changes needed (tools/auth.py is the only
  auth surface)."""

REMEDY_NONE = """auth: REMEDY — no credential is available in CI.
  Set ONE of these repository secrets:
    CLAUDE_CODE_OAUTH_TOKEN  (subscription; from `claude setup-token`)
    ANTHROPIC_API_KEY        (API billing; takes precedence if both are set)"""


def mode():
    """Resolve the active auth mode without ever printing a credential."""
    if os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return "api"
    if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "").strip():
        return "subscription"
    if not os.environ.get("CI", "").strip():
        return "local-login"
    return "none"


def cmd_check():
    m = mode()
    if m == "none":
        print("auth: FAIL — no credential in CI (loud by design; a silent "
              "no-op shift is worse than a red one)")
        print(REMEDY_NONE)
        return 1
    notes = {
        "api": "API billing (ANTHROPIC_API_KEY) — dollar governor is the law (ADR-008)",
        "subscription": "subscription token — quota governor v2 is the law (ADR-028)",
        "local-login": "no env credential; deferring to claude's own login state",
    }
    print(f"auth: OK — mode {m}: {notes[m]}")
    return 0


def cmd_probe(paths):
    text = ""
    for p in paths:
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                text += f.read().lower() + "\n"
        except OSError:
            continue
    if not text.strip():
        print("auth: probe — no log content to classify")
        return 0
    for sig in AUTH_SIGNATURES:
        m = re.search(sig, text)
        if m:
            print(f"auth: AUTH FAILURE identified in run log — matched /{sig}/ "
                  f"(…{m.group(0)[:80]}…)")
            print(REMEDY_SUBSCRIPTION if mode() != "api" else
                  "auth: REMEDY — rotate ANTHROPIC_API_KEY; the key was rejected.")
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
