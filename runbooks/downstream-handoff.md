# Downstream Consumer Handoff

## Purpose

Tell a consuming project what a released version can replace without implying
that integration, deployment or retirement has occurred.

## Procedure

1. Identify an immutable released tag and verified commit.
2. List implemented rules by profile and stable rule ID.
3. Identify required caller context such as publication date or proper names.
4. List findings and editor-only outputs the consumer must surface or preserve.
5. State intentional differences from the consumer's legacy behavior.
6. Identify behavior that remains consumer-owned.
7. Recommend a shadow comparison against representative real inputs.
8. Retire one legacy rule family at a time only after the consumer validates
   parity or accepts the documented difference.

## Boundary

FlaPol Style can provide fixtures and diagnose package behavior. The consumer
owns dependency changes, adapters, application tests, deployment, rollback and
deletion of its legacy code.

Never say a consumer has adopted, deployed or retired behavior without current
evidence from that consumer's project.
