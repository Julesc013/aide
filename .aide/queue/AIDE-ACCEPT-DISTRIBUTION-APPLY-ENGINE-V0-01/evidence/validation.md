# Validation

Acceptance validation must confirm:

- predecessor chain remains complete;
- latest repair-check remains `PASS_WITH_WARNINGS`;
- material finding count remains `0`;
- missing evidence remains `0`;
- DistributionApplyEngine focused tests pass;
- `distribution-apply status/plan/run/verify` passes;
- Q43-Q48 no-apply/no-publish validators pass;
- broad AIDE validation passes;
- task inspect/evidence commands can inspect the acceptance packet;
- path, secret, and source-output scans do not find leaks;
- diff and commit-policy checks pass.

The final command outcomes are recorded in `validation-results.md`.
