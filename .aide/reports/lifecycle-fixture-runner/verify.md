# Lifecycle Fixture Verify

- result: PASS
- run_id: install-managed-section-apply-temp-latest
- capability_label: fixture_temp_apply_only
- target_repo_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Checks

- PASS: latest-run.json parses (.aide/reports/lifecycle-fixture-runner/latest-run.json)
- PASS: referenced temp workspace exists (C:/Projects/AIDE/aide/.aide/reports/lifecycle-fixture-runner/workspaces/latest)
- PASS: referenced rollback record exists (C:/Projects/AIDE/aide/.aide/reports/lifecycle-fixture-runner/latest-rollback-record.json)
- PASS: referenced temp target exists (C:/Projects/AIDE/aide/.aide/reports/lifecycle-fixture-runner/workspaces/latest/manual/with-managed-section.md)
- PASS: referenced expected postimage exists (C:/Projects/AIDE/aide/.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md)
- PASS: referenced canonical preimage exists (C:/Projects/AIDE/aide/.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md)
- PASS: report postimage hash matches temp file (sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b)
- PASS: expected postimage hash matches report (sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b)
- PASS: temp target content matches expected postimage (.aide/reports/lifecycle-fixture-runner/workspaces/latest/manual/with-managed-section.md)
- PASS: canonical fixture hash after run matches report (.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md)
- PASS: canonical fixture hash unchanged (sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60)
- PASS: run report records temp target mutation (temp only)
- PASS: run report records canonical fixture not mutated (canonical read-only)
- PASS: capability label is bounded (fixture_temp_apply_only)
- PASS: negative capability labels are explicit (active_repo_apply,target_repo_apply,general_lifecycle_apply,rollback_execution,uninstall_execution,release_ready,production_ready,service_ready,commander_ready,provider_adapter_ready)
- PASS: rollback execution is not implemented (report bounded)
- PASS: rollback was not executed (report bounded)
