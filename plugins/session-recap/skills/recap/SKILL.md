---
name: recap
description: Write a durable handoff recap of this working session into SESSION-RECAP.md. Use when ending a session, handing work to someone else, or the user says recap this session, write a handoff, or where did we leave off.
---

# Recap the session

1. Gather evidence — never invent it:
   - `git status --short` and `git diff --stat` (and `git log --oneline -5` if commits landed)
   - decisions and conclusions actually reached in this conversation
   - anything explicitly deferred or left uncertain
2. APPEND to `SESSION-RECAP.md` (create if missing — never truncate or rewrite
   earlier sections):

```
## <YYYY-MM-DD HH:MM> — <one-line session title>
### What changed
### Decisions made
### Open questions
### Next steps
- [ ] ...
```

3. What-changed lines cite the evidence (file paths, commit subjects). Next steps
   are checkboxes a stranger could pick up cold.
4. Show the appended section and where it lives. If SESSION-RECAP.md exceeds ~10
   sections, offer (don't do unasked) to archive older ones to SESSION-ARCHIVE.md.
