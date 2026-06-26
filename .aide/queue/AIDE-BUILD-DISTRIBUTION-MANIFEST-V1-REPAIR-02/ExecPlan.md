# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02 ExecPlan

## Objective

Repair exactly the four remaining material findings from
`AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01` without accepting
`distribution_manifest_v1` or beginning any downstream distribution object.

## Scope

Allowed edits are limited to the DistributionManifest v1 helper/schema/tests,
fixture corpus, task-local evidence, Repair 02 reports, queue index, and
planning/execution logs.

## Findings

1. Reject future-major protocol ranges unless explicitly supported by v1 law.
2. Classify forbidden export-pack target-root members under the `files/` prefix.
3. Record forbidden directory members instead of filtering them into a clean
   directory digest.
4. Add direct invalid future-major protocol fixtures.

## Validation Intent

Run focused DistributionManifest tests, DistributionManifest project/validate,
legacy distribution planning validators, broad AIDE validation, diff checks,
path/secret scans, queue task inspect/evidence, and commit policy after commit.

## Stop Conditions

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02` if the repair passes.
Stop earlier if scope, validation, evidence, or worktree cleanliness fails.
