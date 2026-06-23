# Baseline

- Branch at task start: `main`.
- Queue authority: `.aide/queue/index.yaml`.
- Source task: `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.
- Source result: `ACCEPTED_WITH_WARNINGS`.
- Source missing evidence: `0`.
- Source recommended next task: `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
- This build task did not exist in the live queue before materialization.
- No local `Dominium` checkout is required for this build; the authorized target
  is the temporary fixture workspace at
  `.aide/fixtures/dominium-workunit-validation-slice/workspace`.

The accepted seam warning that AIDE could not invoke Dominium commands remains
true for the seam itself. This task adds only the next narrower authority: one
fixture-backed local read-only `dominium.validation.run` capability invocation.
