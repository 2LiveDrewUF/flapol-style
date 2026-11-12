# Downstream Consumer Handoff

## Purpose

Tell a consuming project what a released version can replace without implying
that integration, deployment or retirement has occurred.

## Procedure

This handoff is mandatory for every published numbered release, including
prereleases, under D-023. Drew's standing instruction permits routine release
notices to existing owning-project chats; a new approval is not needed for
each notice. Consumer deployment remains a separate authority boundary.

Before composing notices, refresh the maintained consumer/deployment inventory
against current project registrations, active package/configuration pins and
available runtime evidence. Include direct installations, separate service
environments, wrapped/proxied tools and workflow projects that rely on a shared
engine. Notify the actual service owner and the dependent workflow owners,
with clear file/deployment ownership to avoid competing upgrades. Static lists,
old reports and archived checkouts are not proof of the current topology.

1. Identify an immutable released tag and verified commit.
2. List implemented rules by profile and stable rule ID.
3. Identify required caller context such as publication date or proper names.
4. List findings and editor-only outputs the consumer must surface or preserve.
5. State intentional differences from the consumer's legacy behavior.
6. Identify behavior that remains consumer-owned.
7. Recommend a shadow comparison against representative real inputs.
8. Retire one legacy rule family at a time only after the consumer validates
   parity or accepts the documented difference.
9. Deliver the version-specific notice to every verified consuming project's
   existing owning chat and inform the maintained inventory owner. Do not create
   new chats or use unrelated external communication channels by inference.
10. Save per-consumer delivery evidence and identify unresolved contacts or
    blocked handoffs explicitly. Distinguish sent, acknowledged, adoption in
    progress and verified adoption in the user-facing release closeout.

Use `docs/RELEASE_NOTIFICATIONS.md` for required notice and receipt fields.

## Boundary

FlaPol Style can provide fixtures and diagnose package behavior. The consumer
owns dependency changes, adapters, application tests, deployment, rollback and
deletion of its legacy code.

Never say a consumer has adopted, deployed or retired behavior without current
evidence from that consumer's project.
