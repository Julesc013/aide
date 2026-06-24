# AIDE Self-Validation Process Adapter Check

- result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01`

## Assertions

- `baseline.head_is_source_commit`: `PASS`
- `source.provider_core_not_changed`: `PASS`
- `baseline.source_status_pass_with_warnings`: `PASS`
- `report.validation_clean`: `PASS`
- `source.adapter_uses_provider_without_defining_provider`: `PASS`
- `source.adapter_aide_specific`: `PASS`
- `source.no_shell_true`: `PASS`
- `process.exact_argv_shell_false`: `PASS`
- `process.axes_separated`: `PASS`
- `result.stdout_origin`: `PASS`
- `state.workspace_unchanged`: `PASS`
- `determinism.projection_digest`: `PASS`
- `behavior.fake_runner_success_once`: `PASS`
- `behavior.zero_launch_refusals`: `PASS`
- `churn.report_validate_no_churn`: `PASS`
- `recursion.direct_validate_not_recursive`: `PASS`
- `hygiene.no_committed_build_leaks`: `PASS`
- `boundary.provider_not_accepted`: `PASS`
- `boundary.provider_non_capabilities_preserved`: `PASS`
- `regression.focused_tests_pass`: `PASS`
