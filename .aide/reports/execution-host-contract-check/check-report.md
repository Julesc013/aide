# ExecutionHost Contract Check Report

- source_task: AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
- source_commit: 4a1f1aa
- result: PASS_WITH_WARNINGS
- passed_assertions: 16
- failed_assertions: 0

## Assertions
- PASS: baseline.source_task_complete - Source build task is complete with missing evidence zero.
- PASS: baseline.no_superseding_task - No acceptance or LocalProcessExecutionHost task already supersedes this check.
- PASS: scope.source_commit_forbidden_paths - Source commit did not modify forbidden runtime, interop, host, or local-state paths.
- PASS: schema.kind_discrimination - Schema enumerates and oneOf-discriminates all ExecutionHost record/report kinds.
- PASS: schema.required_surface - Schema requires the canonical envelope fields.
- PASS: projection.complete_record_set - Exactly six ExecutionHost record projections are present.
- PASS: projection.false_boundary_set - Projection records preserve non-capabilities and false boundary fields.
- PASS: contract.capability_distinction - Descriptor keeps deterministic capability execution distinct from worker/session execution.
- PASS: contract.operation_set - Descriptor records the expected v0 worker/session operation names.
- PASS: source.no_runtime_imports - ExecutionHost protocol helper imports no process, network, or transport modules.
- PASS: source.no_runtime_call_tokens - ExecutionHost protocol helper contains no direct runtime/process/network call tokens.
- PASS: cli.projection_only_commands - AIDE Lite execution-host status/project/validate succeed and print projection-only boundary lines.
- PASS: cli.live_run_rejected - AIDE Lite parser rejects execution-host run; no live host run command is present.
- PASS: report.validation_truthful - Build validation report truthfully records projection-only pass with warnings and next check routing.
- PASS: determinism.commands_no_report_churn - ExecutionHost CLI status/project/validate leave watched source and report bytes unchanged.
- PASS: hygiene.no_absolute_paths_or_secrets - Build and check surfaces scanned so far contain no absolute local paths or secret-like values.
