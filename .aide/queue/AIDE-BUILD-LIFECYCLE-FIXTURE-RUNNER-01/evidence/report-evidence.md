# Report Evidence

Generated runner reports:

- `.aide/reports/lifecycle-fixture-runner/status.json`
- `.aide/reports/lifecycle-fixture-runner/status.md`
- `.aide/reports/lifecycle-fixture-runner/latest-run.json`
- `.aide/reports/lifecycle-fixture-runner/latest-run.md`
- `.aide/reports/lifecycle-fixture-runner/latest-verify.json`
- `.aide/reports/lifecycle-fixture-runner/latest-verify.md`
- `.aide/reports/lifecycle-fixture-runner/latest-transaction-plan.json`
- `.aide/reports/lifecycle-fixture-runner/latest-rollback-record.json`
- `.aide/reports/lifecycle-fixture-runner/run-report.json`
- `.aide/reports/lifecycle-fixture-runner/workspaces/latest/manual/with-managed-section.md`

Latest run evidence:

- `scenario_id`: `install-managed-section`
- `mode`: `apply-temp`
- `workspace_root`: `.aide/reports/lifecycle-fixture-runner/workspaces/latest`
- `preimage_hash`: `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60`
- `postimage_hash`: `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b`
- `canonical_fixture_mutated`: `false`
- `manual_content_preserved`: `true`
- `capability_label`: `fixture_temp_apply_only`

Latest verify evidence:

- result: `PASS`
- checks: 15
- verifies latest-run parsing, temp workspace presence, rollback record presence, temp target presence, expected postimage presence, canonical preimage presence, hash agreement, temp target content equality, canonical hash stability, temp-only mutation claim, and negative capability labels.
