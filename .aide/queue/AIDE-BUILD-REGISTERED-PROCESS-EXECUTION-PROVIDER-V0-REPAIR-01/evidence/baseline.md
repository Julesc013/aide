# Baseline

- source_build_task: `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`
- source_build_commit: `2137af3a68cc50a06b57fe1fd5ee5bc3af8e0924`
- source_build_result: `PASS_WITH_WARNINGS`
- source_check_task: `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`
- source_check_commit: `e1ae28892c34e66ac03e61f89efe635efa0641e0`
- source_check_result: `REQUEST_CHANGES`
- source_material_finding_count: `5`
- source_recommended_next_task: `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`
- repair_task_preexisting_on_disk: `false`
- baseline_git_status: `main...origin/main`

The source check preserved genericity and Dominium parity, but blocked reuse and
provider acceptance on five material safety findings.
