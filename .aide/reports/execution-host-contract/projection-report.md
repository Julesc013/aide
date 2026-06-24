# ExecutionHost Contract Projection

- status: PASS_WITH_WARNINGS
- task_id: AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
- capability_label: execution_host_contract_v0
- accepted_provider_capability: registered_process_execution_provider_v0
- projection_only: true
- execution_host_runtime_implemented: false
- worker_execution_implemented: false
- provider_or_model_calls: none
- network_calls: none
- repository_mutation_performed: false
- recommended_next_task: AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01

## Projections Written

- .aide/reports/execution-host-contract/projections/execution-host-descriptor.json
- .aide/reports/execution-host-contract/projections/execution-host-run-binding.json
- .aide/reports/execution-host-contract/projections/execution-host-event.json
- .aide/reports/execution-host-contract/projections/execution-host-artifact.json
- .aide/reports/execution-host-contract/projections/execution-host-approval.json
- .aide/reports/execution-host-contract/projections/execution-host-usage.json

## Operations

- attach
- collect_artifacts
- create_run
- finish
- interrupt
- probe
- reconcile
- resolve_runtime_approval
- send_input
- stream_events

## Warnings

- ExecutionHost contract is projection-only; no live host, worker execution, runtime, or transport is implemented.
- Capability execution remains separate and is represented only by the accepted provider capability reference.
