# Release FlaPol Style

## Purpose

Publish an immutable alpha or stable version from a verified `main` commit.

## Authority and impact

Creating a public tag is an external publication action. Perform this runbook
only when the user has authorized the release. A release does not authorize a
consumer deployment or migration.

## Preconditions

- Worktree scope is understood and contains no unrelated changes.
- Local `main` is reconciled with `origin/main`.
- Package version, changelog and public documentation agree.
- The proposed tag does not already exist locally or remotely.
- GitHub CLI authentication is valid without exposing token values.

## Verification

Run:

```sh
git status --short --branch
./scripts/verify.sh
git diff --check
```

Review the complete diff and commit only the intended files. Push the verified
commit to `main`, then wait for the `main` GitHub Actions workflow to pass,
including:

- pinned Vale installation and fixtures;
- coverage validation;
- minimum-supported Python tests;
- package installation; and
- installed-package registry smoke test.

Do not tag a red or still-running commit.

## Tag and verify

Create an annotated tag matching the package version:

```sh
git tag -a vX.Y.Z -m "FlaPol Style X.Y.Z"
git push origin vX.Y.Z
```

Wait for the tag-triggered workflow to pass. Verify that the annotated tag
ultimately points to the same commit that passed branch CI. Confirm the local
branch and remote-tracking branch are synchronized.

## Stop conditions

Stop before tagging if:

- tests, install or smoke checks fail;
- version or changelog text disagrees;
- the tag exists;
- the target commit differs from the reviewed commit; or
- remote state changed unexpectedly.

## Recovery

- Before tag publication: fix or revert the commit normally.
- After tag publication: do not move or delete the tag. Revert the defect on
  `main`, increment the version and publish a superseding release.
- Report the affected version, behavior and consumer impact plainly.
