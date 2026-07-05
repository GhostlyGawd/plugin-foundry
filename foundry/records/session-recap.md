---
name: session-recap
title: Session Recap
category: context
stage: idea
version: null
components: [skills, hooks]
one_liner: Writes a structured recap when a session ends and recalls it when the next one starts.
tags: [memory, sessions, continuity]
created: 2026-07-04
updated: 2026-07-04
---

# Session Recap

Context evaporates between sessions; yesterday's decisions get re-derived today.

## Pitch
- **Job:** continuity across sessions without hand-written notes.
- **User:** anyone running multi-day work in one repo.
- **Components:** a Stop/SessionEnd hook appending a dated recap stub to a project
  log file, plus a `recall` skill that reads and summarizes recent entries on demand.
- **Why a plugin:** it's an event (hook) + a retrieval prompt (skill) — a natural
  bundle; also a clean exercise of hook-safety law (writes one project-local file,
  documented loudly).
