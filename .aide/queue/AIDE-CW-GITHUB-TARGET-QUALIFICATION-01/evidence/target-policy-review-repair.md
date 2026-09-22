# Target-Policy Independent Review Repair

The exact review at `9bba1cecaec835b5299cf02718059a94ef4c08cb`
returned `REQUEST_CHANGES`. The first repair closed F-01, F-02 and F-04. Its
superseding rereview preserved F-03 because GitHub's required-workflow rule is
not documented for the user-owned `Julesc013/aide` target. Both review rounds
remain preserved in the independent Markdown and JSON records.

## Repairs

- F-01: the non-dev update rule now includes the required
  `update_allows_fetch_and_merge: false` parameter.
- F-02: broker and owner bypass identities must differ by immutable user id and
  case-insensitive login.
- F-03 first repair, rejected on rereview: the dev ruleset added GitHub's exact
  `workflows` rule, but that control is organization/enterprise scoped and the
  represented `push` trigger is not supported by that rule.
- F-04: canonical desired/current/plan bytes now bind repository id, explicit
  effective-rule records, and classic branch-protection presence or verified
  absence; drift blocks operation materialization.

## F-03 Follow-up Repair

- Removed the target-inapplicable `workflows` ruleset operation.
- Retained the documented destination-enforced strict status check bound to
  exact check name and GitHub App id.
- Extended each admitted required-check identity with exact workflow path and
  event.
- Extended the accepted provider observation with workflow run id/attempt,
  check run id, check suite id, workflow path/event, and candidate head.
- Required the durable decision contract to validate those exact local source
  facts before a check can satisfy the merge precondition.
- Classified workflow run/check identities as monitored and classified
  server-enforced exact workflow source plus same-app/name collision exclusion
  as unsupported. Neither is claimed as a GitHub destination guarantee.

## Boundary

The unresolved live plan still has zero operations. No API sender, credential,
workflow, settings mutation, hosted race, branch effect, merge, tag, or release
was added or executed. This follow-up requires superseding independent review.
