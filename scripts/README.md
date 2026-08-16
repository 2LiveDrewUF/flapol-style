# Scripts

Scripts automate bounded, mature portions of an accepted runbook.

- `verify.sh` performs nonpublishing local validation and reports when the
  pinned Vale portion must be left to GitHub Actions.

There is intentionally no push, tag or release script yet. Release publication
still contains meaningful checkpoints between local verification, branch CI,
tag creation and tag CI. Automating those checkpoints before the process is
boring and stable would produce a very efficient foot-gun.
