# Add or Reclassify a Rule

## Purpose

Turn a settled style decision into documented detection, correction or review
behavior without widening authority by accident.

## Prerequisites

- A concrete proposed rule and governing source.
- Current worktree and branch state inspected.
- Relevant current guide, decisions, coverage and implementation read.
- Any private source authorized for read-only use and kept outside the repository.

## Procedure

1. Establish authority and chronology.
   - Record the current ruling and date.
   - Confirm whether it supersedes older guidance.
   - Treat legacy code as evidence, not authority.
2. Assign or retain a stable namespaced rule ID.
3. Classify the action.
   - `AUTO_FIX`: one deterministic correction is proven.
   - `FLAG`: the condition is detectable but requires context.
   - `EDITOR_ONLY`: detection or correction is not safely deterministic.
   - Reference-only: documentation with no current implementation.
4. Assign profiles and contexts explicitly.
5. Classify quotation behavior for this exact rule.
   - Default to `speech_preserving=False`.
   - Apply the read-aloud test.
   - Require explicit AP or Florida Politics rendering authority.
   - Do not infer permission from registry membership.
6. Define protected behavior for code, URLs, link destinations, emails and
   malformed quote/code structure.
7. Add positive, negative, boundary, quotation, literal and idempotence tests.
8. Implement through the shared editing session so reports retain source offsets.
9. Update public registry data, coverage, provenance and API documentation.
10. Run `scripts/verify.sh`.

## Stop conditions

Stop and request a ruling when:

- the current house rule is genuinely unresolved;
- the transformation could change spoken words, meaning or factual content;
- entity identity or publication role is required but unavailable;
- provenance cannot be published safely; or
- a proposed automatic rule has more than one defensible result.

## Acceptance

The rule is ready for release consideration when tests prove intended behavior,
false positives, hard protection, quote policy, source coordinates and
idempotence, and public documentation describes exactly what exists.
