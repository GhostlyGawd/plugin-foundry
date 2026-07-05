#!/usr/bin/env python3
"""alarm.py — tripwire self-issues (ADR-010). Opens an `ops-alarm` issue at this
repo so halts and P0 audits notify the operator natively. Idempotent by title;
degrades to a log line without gh. Usage: alarm.py "<title>" "<body>"."""
import subprocess
import sys


def main(title, body):
    try:
        existing = subprocess.run(
            ["gh", "issue", "list", "--label", "ops-alarm", "--state", "open",
             "--search", title, "--json", "title"],
            capture_output=True, text=True, check=True).stdout
        if title in existing:
            print(f"alarm: already open — {title}")
            return 0
        subprocess.run(
            ["gh", "issue", "create", "--title", title, "--label", "ops-alarm",
             "--body", body + "\n\n_Opened automatically by tools/alarm.py — close when resolved; "
             "the window shows an amber state while any ops-alarm is open._"],
            capture_output=True, text=True, check=True)
        print(f"alarm: opened — {title}")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"alarm (no gh context, logged only): {title} — {body}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""))
