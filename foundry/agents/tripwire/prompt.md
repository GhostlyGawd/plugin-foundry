# tripwire agent — prompt
tools/tripwire.py detected a rubber-stamp streak (5 clean QA passes, or 5 approvals
with no bounce, or 4 'keep' verdicts). A perfect streak means the inspection went
soft, not that the work got perfect. Write a fresh ADVERSARIAL re-audit into
reviews/ that lists concrete attacks you ATTEMPTED against the recent approvals
(injection, hook-safety, version-law, honesty) and what you found. Propose it; do
not rubber-stamp your own re-audit.
