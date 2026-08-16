# Repository and Release System

## Identity

- Local checkout: `/Users/drew/DrewGPT/FlaPol Style`
- Public remote: `https://github.com/2LiveDrewUF/flapol-style.git`
- Default branch: `main`
- CI workflow: `.github/workflows/test.yml`
- Release form: annotated `v`-prefixed Git tag

## Observed baseline

Observed 2026-08-16:

- Local `main` matched `origin/main` after the canonical checkout was created.
- Current release was `v0.1.0a3`.
- `v0.1.0a3` pointed to commit
  `bb24fb4ea3e744bd762f15c1f12ec3d2c726338f`.
- Branch and tag workflows for that commit completed successfully.

These are drift-prone facts. Reobserve before release or incident work.

## Authentication

GitHub authentication is external environment state. Use the authenticated
GitHub CLI or approved Git credential helper. Never record token, cookie, SSH
key or credential values here.

## Health

The repository is healthy for release purposes when:

- local and remote branch identity are reconciled;
- tests and coverage validation pass;
- the package installs under the minimum supported Python version;
- packaged JSON registries load outside the source tree; and
- every published release tag has a successful independent workflow.

## Recovery

The public GitHub repository is the off-machine source copy. A lost local
checkout can be recreated by cloning the public remote into the canonical
path. Unpushed local work is not recoverable from GitHub and must be committed
or backed up intentionally before risky local operations.

Published tags are immutable. Recover from a bad release through a revert and
new version, never by rewriting the tag.
