# Governing documentation

This directory contains public Florida Politics policy, API, provenance and
migration documentation suitable for publication:

- [`QUOTE_POLICY.md`](QUOTE_POLICY.md) — the boundary for deterministic
  rendering inside direct quotations;
- [`RULE_SOURCES.md`](RULE_SOURCES.md) — concise authority and chronology for
  implemented automatic rules;
- [`SALVAGE_LEDGER.md`](SALVAGE_LEDGER.md) — accepted, deferred and rejected
  behavior examined in the legacy Streamlet formatter; and
- [`PYTHON_API.md`](PYTHON_API.md) — public processor entry points, reporting
  contracts and coordinate semantics.

The repository does not claim that these files reproduce a complete Florida
Politics or AP prose guide. Private Slack exports, private discussion text, the
AP e-book and reproduced AP entries do not belong here. Public rules may
identify the controlling AP edition and entry name without reproducing the
source text.

Implementation status is recorded separately in [`coverage/`](../coverage/).
Each record distinguishes documentation, detection, automatic correction,
applicable contexts and protected-region support. A human rule is not
represented as an automatic correction merely because the guide documents it
or Vale can detect it.
