# Startup Checklist

## Established project state

- [x] Canonical local checkout created at `/Users/drew/DrewGPT/FlaPol Style`.
- [x] Public remote confirmed as `https://github.com/2LiveDrewUF/flapol-style.git`.
- [x] Default branch confirmed as `main`.
- [x] Existing history and annotated release tags preserved.
- [x] `v0.1.0a4` confirmed as the current release on 2026-08-18.
- [x] Public branch and tag CI confirmed green for `v0.1.0a4`.
- [x] Project, ownership, decision, runbook, system and script governance added.

## Begin every work session

1. Read `PROJECT.md`, `AGENTS.md` and the relevant accepted decisions.
2. Run `git status --short --branch` before editing.
3. Fetch or otherwise verify current remote state when drift matters.
4. Identify whether the task is rule research, implementation, release work,
   consumer handoff or documentation only.
5. Read the relevant runbook before changing behavior or publishing anything.
6. Preserve unrelated user changes; do not assume a dirty worktree is yours.

## Current operating baseline

- Package API version: `0.1.0a4`
- Current quote model: rule-level `speech_preserving`, false by default
- Current release channel: annotated Git tag in the public GitHub repository
- Hosted services: none
- Managed production systems: none
- Known downstream consumer candidate: Newsroom Tools, which owns its own
  integration, testing, deployment and legacy retirement

Reobserve drift-prone facts before relying on this snapshot.

## Next useful work

- Continue rule-family salvage using `runbooks/add-or-reclassify-rule.md`.
- Give downstream consumers a released capability matrix and require their own
  shadow comparison before retirement.
- Add automation only after a manual procedure has repeated enough to be
  boring, bounded and demonstrably recoverable.
