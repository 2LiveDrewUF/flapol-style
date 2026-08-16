# Ownership and Publication Boundary

## Project ownership

Drew owns project administration, repository maintenance and release
decisions. Repository-owned source is published under the MIT License.

The license does not grant rights to third-party trademarks, article content,
private newsroom material, AP Stylebook text or other material merely described
by the project.

## Public repository contents

Appropriate public material includes:

- original source code and tests;
- concise house rules and derived implementation facts;
- public registries and nonprivate fixtures;
- coverage and provenance records;
- public operating documentation; and
- release metadata.

## Restricted source material

Do not commit or reproduce:

- the AP Stylebook e-book or substantial AP entry text;
- private Slack exports or private discussion transcripts;
- unpublished Florida Politics copy except a minimal authorized fixture;
- private Newsroom Tools code, data or registries;
- credentials, tokens, cookies, SSH material or secret values; or
- third-party data whose license or provenance does not permit publication.

Restricted sources may establish a derived rule when access is authorized. The
public record should name the source and summarize the adopted result without
publishing the restricted source itself.

## Florida Politics and AP authority

Florida Politics house guidance is editorial authority for house departures;
it is not automatically repository-owned intellectual property in every source
form. AP material remains governed by AP's rights and terms. This project
publishes interoperable rules, not a substitute Stylebook.

## Newsroom Tools boundary

Newsroom Tools is a separate, private Drew-owned project. It owns Streamlet,
product-specific formatting, current people and officeholder registries,
deployment, shadow comparison, release adoption and retirement of legacy code.

FlaPol Style may publish a versioned interface and inspect authorized legacy
behavior read-only. It must not claim that Newsroom Tools has adopted a release
or modify Newsroom Tools while operating in this project.

## Credentials and authenticated tools

Use existing authenticated GitHub tooling without recording credential values.
Authentication state is environmental and must be rechecked when needed. No
secret belongs in source, documentation, fixtures, logs or release notes.

## Mixed or uncertain material

When ownership or publication rights are unclear, treat the material as
restricted until resolved. Record the derived decision only when it can be
published without leaking the source.
