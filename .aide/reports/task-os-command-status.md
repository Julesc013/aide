# Task OS Command Status

- command: `task-os command status registry`
- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `4f426e7c42106e6e859aafb7a06896e3e7ce9b2a`
- mode: report_only
- task_execution: false
- repair_execution: false
- branch_mutation: false
- target_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Commands

- `task status`
- `task classify`
- `task repair-plan`
- `task requeue-plan`
- `task resume-plan`
- `blocker status`
- `blocker classify`
- `wave status`
- `wave plan`
- `checkpoint status`
- `checkpoint plan`

## Generated Reports

- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-task-status.md`
- `.aide/reports/task-os-task-classification.json`
- `.aide/reports/task-os-task-classification.md`
- `.aide/reports/task-os-repair-plan.md`
- `.aide/reports/task-os-requeue-plan.md`
- `.aide/reports/task-os-resume-plan.md`
- `.aide/reports/task-os-blocker-status.md`
- `.aide/reports/task-os-blocker-classification.json`
- `.aide/reports/task-os-blocker-classification.md`
- `.aide/reports/task-os-wave-status.md`
- `.aide/reports/task-os-wave-plan.md`
- `.aide/reports/task-os-checkpoint-status.md`
- `.aide/reports/task-os-checkpoint-plan.md`
- `.aide/reports/task-os-next-plan.md`

## Source Files Inspected

- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/reports/target-work-deferral.md`
- `.aide/reports/task-os-schema-status.md`
- `.aide/reports/task-os-policy-status.md`
- `.aide/reports/latest-warning-disposition.md`
- `.aide/policies/task-lifecycle.yaml`
- `.aide/policies/blockers.yaml`
- `.aide/policies/repair-loop.yaml`
- `.aide/policies/waves.yaml`
- `.aide/policies/checkpoints.yaml`
- `.aide/policies/dev-main-promotion.yaml`
- `.aide/policies/capability-reality.yaml`
- `.aide/tasks/workunit.schema.json`
- `.aide/tasks/task-attempt.schema.json`
- `.aide/tasks/blocker.schema.json`
- `.aide/tasks/repair-task.schema.json`
- `.aide/tasks/wave.schema.json`
- `.aide/tasks/checkpoint.schema.json`
- `.aide/ledgers/task-ledger.schema.json`
- `.aide/ledgers/blocker-ledger.schema.json`
- `.aide/ledgers/capability-ledger.schema.json`
- `.aide/ledgers/branch-provenance.schema.json`
- `.aide/ledgers/checkpoint-ledger.schema.json`

## Status

- command_surface: registered
- no_apply_boundary: enforced_by_report
- next_recommended_action: AIDE-APPLY-00 - Transaction Model
- next_recommended_reason: X-OS-02, AIDE-CHECK-OS-01, and AIDE-FIX-OS-03 are locally complete for review; the next packet may define the transaction model without applying it.
- aide_apply_00_next_packet_ready: true
