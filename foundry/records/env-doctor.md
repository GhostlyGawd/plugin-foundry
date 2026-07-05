---
name: env-doctor
title: Env Doctor
category: quality
stage: idea
version: null
components: [hooks]
one_liner: Checks the toolchain against the project's declared versions at session start and warns early.
tags: [environment, onboarding, hooks]
created: 2026-07-04
updated: 2026-07-04
---

# Env Doctor

Half of "it doesn't work" is a version mismatch discovered twenty minutes in.

## Pitch
- **Job:** surface toolchain drift in the first second of a session.
- **User:** teams with .tool-versions/.nvmrc/pinned runtimes.
- **Components:** one SessionStart command hook running a read-only script that
  compares installed versions to declared ones and prints warnings.
- **Why a plugin:** SessionStart is exactly what hooks exist for; read-only by
  design, so a good showcase of the safety bar.
