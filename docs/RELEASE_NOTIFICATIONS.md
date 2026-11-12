# Mandatory numbered-release notifications

Authority: Drew's Nov. 12, 2026 standing instruction, recorded in D-023.
Every published numbered release, including alpha, beta and release-candidate
tags, requires a consumer handoff. Ordinary commits and unpublished local
trials are outside this trigger. Notification is part of release closeout,
not an optional offer after publishing the tag.

## Refresh the recipients

Start from the maintained consumer/deployment inventory, then verify it against
current project registrations, active dependencies, adapter pins and available
runtime evidence. Look for separate installations behind similar tool names,
proxies, subprocess environments and workflow consumers of a shared service.
Do not freeze the inventory to the consumers known on the previous release.

Notify each verified consumer's existing owning-project chat and the inventory
owner. Coordinate which project changes each runtime or governing file so
multiple owners do not run competing upgrades. Preserve archived copies,
historical receipts and intentional rollback/comparison baselines. Record an
unreachable owner or uncertain installation explicitly instead of inventing a
recipient or claiming coverage. No new chat, email, Slack message or external
recipient is authorized merely by this standing project-notice rule.

## Required notice

- Released version, immutable tag, peeled commit and annotated tag identity.
- Branch/tag verification status and supporting links or evidence.
- Implemented scope by profile/rule family, intentional changes and exclusions.
- Required dates, identity/name context and relevant API/adapter requirements.
- Quotation/literal protections and the distinction between findings and fixes.
- Request for the owner to evaluate the release and advance active pins under
  its own authority, with representative checks, provenance and rollback.
- Clear statement that held experimental branches are not part of the release.

Send the normal upgrade notice after successful tag verification. If a tag has
already been published with failed or unresolved checks, give the current
status and hold instruction; follow up when verification changes. Never
present an unverified release as ready or move a tag to conceal a failure.

Drew has authorized these routine release notices in advance. Do not interrupt
each future release to ask again. This authority covers notification only;
consumer source changes, deployment, publication, credentials and permissions
remain governed by the owning project and the user's actual instructions.

## Required receipt and closeout

Record the released version and commit, inventory date, consumer/owner,
delivery date and location/reference, acknowledgment when observed, adoption
state, evidence of actual version/commit when verified, and any blocker or
next step. Keep private deployment details, chat identifiers and receipts in
appropriate private/local operating records rather than the public package.

The release closeout must account for every known current consumer: either a
notice was delivered or an unresolved handoff is recorded and surfaced to Drew.
Use precise states such as delivered, acknowledged, adoption in progress and
verified adopted. A receipt, file-pin edit or owner's intention is not proof
that an installed engine has changed.

This requirement does not make FlaPol Style wait for every consumer to deploy,
nor does it claim their adoption. It makes the release notice reliable and the
remaining consumer-owned work visible. Preserve unrelated copy, queues,
services and source material throughout.
