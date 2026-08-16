# Runbooks

Runbooks describe repeated, consequential procedures with prerequisites,
verification, stop conditions and recovery. They are not permission to publish
or mutate external state without an applicable user request.

- `add-or-reclassify-rule.md` — research, classify, implement and validate a rule
- `release.md` — cut and verify an immutable public release
- `downstream-handoff.md` — describe a released capability without claiming adoption

Automation must cite the runbook it implements. If the manual procedure changes,
update and reverify the runbook before changing automation.
