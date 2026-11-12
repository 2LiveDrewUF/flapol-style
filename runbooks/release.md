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

## Notify consumers — required for every numbered release

After tag CI passes, refresh the current consumer inventory and notify every
consuming project's existing owning chat using `runbooks/downstream-handoff.md`.
Include alpha, beta, release-candidate and stable numbered releases. Drew's
standing Nov. 12, 2026 instruction authorizes these notices without a new
permission request. Ordinary commits and local trial branches do not trigger
this release-notification requirement.

Include the immutable tag, peeled commit, annotated tag identity, verification
evidence, released changes, exclusions, caller requirements and checks needed
before adoption. Ask the owner to evaluate and advance its active pins under
its own authority. Preserve deliberate comparison/rollback baselines and
historical records. Do not bundle local experiments into the upgrade.

Record per-consumer delivery, acknowledgment, pending work and verified
adoption separately, following `docs/RELEASE_NOTIFICATIONS.md`. Release
closeout requires a delivered notice for each current consumer, or an explicit
unresolved handoff recorded and surfaced to Drew. No known consumer may be
silently omitted. A notice does not authorize deployment from this project.

If a numbered tag is already published but its checks fail or remain unresolved,
send an accurate status/hold notice rather than announcing a verified upgrade.
Follow up when that status changes; do not alter the immutable tag.

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
