# Current GitHub Target Observation

Date: 2026-09-22

## Environment and method

- Windows identity: `BLACKGLASS-WIN1\Jules`.
- Authenticated GitHub account: `Julesc013` (`User`, id `30209022`).
- GitHub CLI: `2.96.0`.
- Explicit REST API version: `2022-11-28`.
- Repository: public `Julesc013/aide`, id `1192621212`.
- Operation class: credentialed read-only observations. No settings, refs,
  workflows, credentials or repository content were changed.

The machine-readable adjacent JSON records the selected bounded responses.
Its SHA-256 is
`2791c4c625e9cfa3514ca6fbdb02cf98ef238baaee2012d56554821b4612e8d2`.
Authentication status was checked in the real Windows user context before the
queries. No token value is recorded.

## Observed state

- `main`: `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.
- `dev`: `d37219026462d5670f7a724980faf07e30abb85f`.
- Repository rulesets: none returned.
- Effective rules for `main`: none returned.
- Effective rules for `dev`: none returned.
- `dev` branch protection: HTTP 404, `Branch not protected`.
- Actions workflows: zero returned.
- Merge settings permit merge, squash and rebase; auto-merge is disabled.
- The observed account has repository admin permission.

## Qualification result

`FAIL_CLOSED_FOR_HOSTED_EFFECTS`. The current target cannot establish the
planned strict required-check, no-bypass, non-dev update-denial or workflow
provenance predicates. The owner/admin credential is not a restricted broker
principal and must not be repurposed as one merely because it is available.

The implemented expected-head `sha` remains a documented endpoint predicate,
but no hosted request was sent. No base, target-ref, actor, ruleset, policy or
principal guarantee is qualified by this observation.

## Next review subject

Prepare an exact non-mutating desired policy/workflow/principal proposal that
preserves separately identified owner operations and leaves unresolved IDs as
apply blockers. Independent review must bind that proposal and the actual
principal/app identities before any settings installation or hosted mutation.
