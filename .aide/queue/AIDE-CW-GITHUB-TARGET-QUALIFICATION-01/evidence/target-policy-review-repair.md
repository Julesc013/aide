# Target-Policy Independent Review Repair

The exact review at `9bba1cecaec835b5299cf02718059a94ef4c08cb`
returned `REQUEST_CHANGES`. All four findings are preserved in its Markdown and
JSON records.

## Repairs

- F-01: the non-dev update rule now includes the required
  `update_allows_fetch_and_merge: false` parameter.
- F-02: broker and owner bypass identities must differ by immutable user id and
  case-insensitive login.
- F-03: the dev ruleset now includes GitHub's exact `workflows` rule bound to
  path, repository id, source ref, and source commit, in addition to the
  app-bound named status check.
- F-04: canonical desired/current/plan bytes now bind repository id, explicit
  effective-rule records, and classic branch-protection presence or verified
  absence; drift blocks operation materialization.

## Boundary

The unresolved live plan still has zero operations. No API sender, credential,
workflow, settings mutation, hosted race, branch effect, merge, tag, or release
was added or executed. This repair requires superseding independent review.
