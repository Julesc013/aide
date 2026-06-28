# Validation Results

Result: `PASS_WITH_WARNINGS`

- Compile checks passed.
- Focused DistributionApplyEngine tests passed: `9` tests.
- `distribution-apply status/plan/run/verify` passed.
- Required adversarial fixture scenarios refused with expected reason codes.
- Direct validator probes for non-accepted context, operation-not-in-UpdatePlan, and operation-lacking-RollbackBundle-coverage refused with expected reason codes.
- Predecessor validations through UpdateReceipt passed.
- Q43-Q48 no-apply/no-publish validators passed.
- Broad `py -3 .aide/scripts/aide_lite.py validate` passed.
- Task inspect/evidence completed with `missing_evidence: 0` after check evidence was written.
- Path, credential-pattern, source-output misuse, and diff checks passed.

Warnings:

- DistributionApplyEngine v0 is not accepted by this check.
- Acceptance must be a separate queue task.
