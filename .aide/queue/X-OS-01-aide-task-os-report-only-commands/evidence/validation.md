# Validation

Validation result: PASS_WITH_WARNINGS.

## Command Smoke

- `py -3 .aide/scripts/aide_lite.py task status`: PASS; wrote `.aide/reports/task-os-task-status.md`.
- `py -3 .aide/scripts/aide_lite.py task classify`: PASS; wrote task classification JSON/Markdown reports.
- `py -3 .aide/scripts/aide_lite.py task repair-plan`: PASS; wrote repair plan with `repair_executed: false`.
- `py -3 .aide/scripts/aide_lite.py task requeue-plan`: PASS; wrote requeue plan with `queue_mutation_applied: false`.
- `py -3 .aide/scripts/aide_lite.py task resume-plan`: PASS; wrote resume plan with `report_only: true`.
- `py -3 .aide/scripts/aide_lite.py blocker status`: PASS; wrote blocker status with `repair_executed: false`.
- `py -3 .aide/scripts/aide_lite.py blocker classify`: PASS; wrote blocker classification JSON/Markdown reports.
- `py -3 .aide/scripts/aide_lite.py wave status`: PASS; wrote wave status with `branch_mutation: false`.
- `py -3 .aide/scripts/aide_lite.py wave plan`: PASS; wrote wave plan with `branch_mutation: false`.
- `py -3 .aide/scripts/aide_lite.py checkpoint status`: PASS; wrote checkpoint status with `checkpoint_apply: false`.
- `py -3 .aide/scripts/aide_lite.py checkpoint plan`: PASS; wrote checkpoint plan with `checkpoint_apply: false`.

## Tests And Evals

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/tests/test_x_os_01_task_os_commands.py`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_command_surface_golden`: PASS, 18/18 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_task_status_report_golden`: PASS, 22/22 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_repair_requeue_resume_plan_golden`: PASS, 21/21 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_blocker_classification_golden`: PASS, 8/8 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_wave_checkpoint_plan_golden`: PASS, 26/26 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task task_os_report_only_no_apply_golden`: PASS, 28/28 checks.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 152/152 golden tasks, 0 warnings, 0 failures.

## Repo Validation

- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS after adding the expected latest golden run reports to the X-OS-01 allowed paths.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS; wrote `.aide/context/latest-review-packet.md`, budget status PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack`: PASS; included_files=724, checksum_count=727, provider/model calls none, network calls none.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary result PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "X-OS-02 - Capability Reality Ledger v0: ..."`: PASS; wrote `.aide/context/latest-task-packet.md`, approx_tokens=1129, budget status PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: report-only branch plan returned `blocked` because the worktree is dirty before commit; remote mutation false, push requested false, apply requested false.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; one warning: `.aide/generated/manifest.yaml` source fingerprint is stale.
- `git diff --check`: PASS.
- Boundary-aware targeted secret scan over X-OS-01 queue/evidence/docs/tests/reports: PASS, no matches.

## Warnings

- `review_gate`: expected; X-OS-01 stops at `needs_review`.
- `expected_dirty_pack_provenance`: expected before the structured X-OS-01 commit; `pack-status` recorded `DIRTY_SOURCE_RECORDED` with zero checksum or boundary problems.
- `assigned_next`: expected; latest task packet points to X-OS-02.
- `expected_generated_state`: root Harness v0 reported stale `.aide/generated/manifest.yaml`; not introduced by Task OS command behavior and not blocking this report-only task.
