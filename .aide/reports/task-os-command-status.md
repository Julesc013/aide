# Task OS Command Status

- command: `task-os command status registry`
- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `ec3d8c1797b9a32fec1878ded11b3c376b5f0079`
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
- `task next-plan`
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
- current_toml_state: absent
- current_task_id: none
- current_task_status: absent
- latest_indexed_task_id: AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01
- latest_indexed_task_status: needs_review
- latest_task_packet_id: AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01
- latest_task_packet_status: needs_review
- selected_next_workunit: AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning
- next_recommended_action: AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning
- next_recommended_reason: AIDE-APPLY-02 is accepted with notes and Task OS current/latest truth is review-gated; the next safe WorkUnit is planning-only lifecycle scoping, not lifecycle apply execution.
- aide_apply_00_next_packet_ready: false
- aide_apply_lifecycle_plan_ready: true
- lifecycle_apply_authorized: false
