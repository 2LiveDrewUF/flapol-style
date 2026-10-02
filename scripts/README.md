# Scripts

Scripts automate bounded, mature portions of an accepted runbook.

- `verify.sh` performs nonpublishing local validation and reports when the
  pinned Vale portion must be left to GitHub Actions.
- `refresh_officeholder_book.py --checked-on YYYY-MM-DD` fetches the accepted
  narrow roster from its official sources and writes a review candidate. It
  validates complete seat counts and preserves vacancies. A successful fetch
  is not adjudication: review the generated diff and staleness dates before
  committing it.

There is intentionally no push, tag or release script yet. Release publication
still contains meaningful checkpoints between local verification, branch CI,
tag creation and tag CI. Automating those checkpoints before the process is
boring and stable would produce a very efficient foot-gun.
