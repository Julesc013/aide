# Validation

Validation must prove:

- focused fixture tests pass;
- DistributionApplyEngine remains accepted and fixture-only;
- Q43-Q48 no-apply/no-publish validators still pass;
- broad AIDE validation passes;
- task inspect/evidence finds no missing evidence;
- no secrets, prompt/response transcript leakage, host-local paths, or source-output dependencies were introduced;
- diff and commit-message checks pass.

Final command results are recorded in `validation-results.md`.
