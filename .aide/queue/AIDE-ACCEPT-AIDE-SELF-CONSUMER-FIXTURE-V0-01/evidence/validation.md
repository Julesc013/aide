# Validation

Validation outcome: `ACCEPTED_WITH_WARNINGS`.

The acceptance validation confirms:

- build task result remains `PASS_WITH_WARNINGS`;
- check task result remains `PASS_WITH_WARNINGS`;
- material finding count remains `0`;
- missing evidence remains `0`;
- focused self-consumer fixture tests pass;
- DistributionApplyEngine verification passes with warnings only;
- Q43-Q48 no-apply/no-publish validators pass;
- broad validation passes;
- predecessor and acceptance task evidence is complete;
- safety scans and diff checks pass.

The only accepted warning debt is stale operator-facing `distribution-apply` routing/status text. This is non-material to the fixture capability because it does not widen apply authority or change boundary flags.
