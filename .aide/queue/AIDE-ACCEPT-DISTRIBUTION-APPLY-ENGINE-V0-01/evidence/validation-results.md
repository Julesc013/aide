# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m compileall core/distribution .aide/scripts/tests/test_aide_distribution_apply_engine_v0.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_distribution_apply_engine_v0.py` | PASS, 9 tests |
| `py -3 .aide/scripts/aide_lite.py distribution-apply status` | PASS_WITH_WARNINGS, 46 scenarios |
| `py -3 .aide/scripts/aide_lite.py distribution-apply plan --scenario managed-file-update` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp` | PASS_WITH_WARNINGS, UpdateReceipt generated, rollback verified |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario missing-update-plan-binding --mode apply-temp` | PASS, refused with `distribution_apply_engine.update_plan_binding_missing`, no UpdateReceipt output |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario missing-rollback-bundle-binding --mode apply-temp` | PASS, refused with `distribution_apply_engine.rollback_bundle_binding_missing`, no UpdateReceipt output |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario mismatched-update-plan-rollback-bundle --mode apply-temp` | PASS, refused with `distribution_apply_engine.update_plan_rollback_bundle_mismatch`, no UpdateReceipt output |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario predecessor-source-distribution-mismatch --mode apply-temp` | PASS, refused with `distribution_apply_engine.predecessor_mismatch`, no UpdateReceipt output |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario run-without-accepted-context --mode apply-temp` | PASS, refused with `distribution_apply_engine.accepted_context_missing`, no UpdateReceipt output |
| `py -3 .aide/scripts/aide_lite.py distribution-apply verify` | PASS_WITH_WARNINGS, fixture matrix passed, material findings 0, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py update-receipt validate` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01` | PASS, evidence files 18, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01` | PASS, missing none |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS after commit `483d965b` |

Notes:

- `distribution-apply status/plan/verify` still print the build-era implementation recommendation to check the proposed engine. This acceptance does not modify implementation-owned routing text; the acceptance task, status, index, and acceptance reports recommend exactly `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.
- `update-receipt validate` still prints its phase-local no-DistributionApplyEngine boundary from the UpdateReceipt task scope. This acceptance does not reopen predecessor UpdateReceipt validation semantics.
- `commit check --latest` passed after the local commit existed; the evidence was amended into the same local commit.
