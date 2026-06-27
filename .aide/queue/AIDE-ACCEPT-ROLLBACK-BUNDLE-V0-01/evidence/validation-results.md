# Validation Results

Overall status: PASS

Command outcomes:

- `git status --short --branch`: PASS; worktree contained only acceptance-task changes.
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`: PASS; source build classified complete with `missing_evidence: 0`.
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`: PASS.
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`: PASS; source check classified complete with `missing_evidence: 0`.
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`: PASS.
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01`: PASS; acceptance classified complete with `missing_evidence: 0`.
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01`: PASS.
- JSON parse for `.aide/reports/rollback-bundle-v0-acceptance/*.json`: PASS.
- `py -3 -m compileall -q core\protocol\rollback_bundle.py .aide\scripts\tests\test_aide_rollback_bundle_v0.py .aide\scripts\aide_lite.py`: PASS.
- `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_rollback_bundle_v0.py`: PASS, 7 tests.
- `py -3 .aide\scripts\aide_lite.py rollback-bundle status`: PASS_WITH_WARNINGS; no apply/mutation flags implemented.
- `py -3 .aide\scripts\aide_lite.py rollback-bundle project`: PASS_WITH_WARNINGS.
- `py -3 .aide\scripts\aide_lite.py rollback-bundle validate`: PASS_WITH_WARNINGS; error count 0.
- Predecessor regression validation for DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord, and UpdatePlan status/project/validate commands: PASS or PASS_WITH_WARNINGS with exit code 0.
- `py -3 .aide\scripts\aide_lite.py ownership-ledger migrate-q43`: PASS_WITH_WARNINGS with exit code 0.
- Q43-Q48 no-apply/no-publish validators: PASS with exit code 0 for install, repair, upgrade, rollback, uninstall, release validate, and release draft-validate.
- `py -3 .aide\scripts\aide_lite.py validate`: PASS.
- Acceptance local absolute path scan: PASS; no hits.
- Acceptance secret-like assignment scan: PASS; no hits.
- Acceptance source-output misuse scan: PASS_WITH_NOTE; the only hit is the accepted fail-closed phrase `source latest output as target truth`, not a target-truth claim.
- Downstream path absence check: PASS; UpdateReceipt paths are absent.

No implementation files changed during acceptance validation.
