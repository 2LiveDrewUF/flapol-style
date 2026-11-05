# Scripts

Scripts automate bounded, mature portions of an accepted runbook.

- `verify.sh` performs nonpublishing local validation and reports when the
  pinned Vale portion must be left to GitHub Actions.
- `refresh_officeholder_book.py --checked-on YYYY-MM-DD` fetches the accepted
  narrow roster from its official sources and writes a review candidate. It
  validates complete seat counts and preserves vacancies. Add
  `--legislature-only` to refresh the 2026-2028 state House and Senate
  while carrying forward the prior term and other groups from the packaged
  book. Use `--output PATH` to write the candidate separately. Review the
  generated diff, name variants and staleness dates before committing it.
  A full refresh preserves incoming federal and executive records while
  the sitting groups are usable. At a transition, adjudicate the incoming
  entries, update the current office profile sources and archive the old
  snapshot before running the full refresh.

There is intentionally no push, tag or release script yet. Release publication
still contains meaningful checkpoints between local verification, branch CI,
tag creation and tag CI. Automating those checkpoints before the process is
boring and stable would produce a very efficient foot-gun.
