# Q30 Changed Files

## Queue And Evidence

- `.aide/queue/Q30-aide-dev-main-policy-sync/**`: Q30 task packet, ExecPlan, status, prompt, and evidence.
- `.aide/queue/index.yaml`: Q30 queue entry.

## AIDE Branch Policy

- `.aide/git/aide-branch-policy.yaml`: AIDE-specific branch policy with `main` canonical, `dev` integration, task prefixes, live no-mutation rule, and promotion gates.
- `.aide/git/aide-dev-main-plan.json`: generated non-mutating dev/main plan from current branch topology.
- `.aide/git/aide-dev-main-plan.md`: human-readable dev/main plan.
- `.aide/git/workflow-detection.json`: refreshed report-only workflow detection.
- `.aide/git/workflow-detection.md`: refreshed workflow detection summary.
- `.aide/git/latest-helper-plan.json`: refreshed helper plan from live repo dry-run state.
- `.aide/git/latest-helper-plan.md`: refreshed helper plan summary.

## AIDE Lite Commands And Tests

- `.aide/scripts/aide_lite.py`: Q30 branch-policy validation, dev/main plan generation, Git command integration, golden task checks, and selftest fixture alignment.
- `.aide/scripts/tests/test_q30_aide_dev_main_policy.py`: tests for AIDE branch policy, missing/present `dev`, promotion gates, no-live-mutation posture, and Q30 golden tasks.

## Golden Tasks

- `.aide/evals/golden-tasks/aide_dev_main_policy_golden/**`: Q30 policy golden task.
- `.aide/evals/golden-tasks/aide_branch_plan_golden/**`: Q30 plan golden task.
- `.aide/evals/golden-tasks/catalog.yaml`: catalog entries for Q30 golden tasks.
- `.aide/evals/runs/latest-golden-tasks.json`: regenerated golden task report, 22/22 PASS.
- `.aide/evals/runs/latest-golden-tasks.md`: regenerated golden task report.

## Export Pack And Generated Packets

- `.aide/export/aide-lite-pack-v0/**`: regenerated AIDE Lite Pack with updated generic Git workflow support and updated helper script while excluding Q30 AIDE-local policy tests/goldens.
- `.aide/context/latest-task-packet.md`: regenerated Q31 compact task packet.
- `.aide/changelog/**`: regenerated changelog and release-note previews.

## Documentation And State Truth

- `.aide/profile.yaml`: current focus updated to Q30 implemented/awaiting review.
- `.aide/commands/catalog.yaml`: command catalog updated for Q30 dev/main plan reporting.
- `AGENTS.md`: branch workflow guidance updated for Q30 missing-`dev` posture.
- `README.md`: Q30 current-state summary and reference link.
- `ROADMAP.md`: Q30 completed-phase and Q31 next-phase guidance.
- `PLANS.md`: Q30 plan entry.
- `IMPLEMENT.md`: Q30 implementation log entry.
- `DOCUMENTATION.md`: Q30 docs and test references.
- `docs/reference/aide-dev-main-workflow.md`: new AIDE-specific dev/main workflow guide.
- `docs/reference/git-workflow-policy.md`: Q30 AIDE-specific posture note.
- `docs/reference/branch-roles.md`: Q30 AIDE repo role note.
- `docs/reference/promotion-policy.md`: Q30 future live-promotion boundary note.
- `docs/reference/README.md`: new reference-doc link.
- `docs/roadmap/queue-roadmap.md`: Q26-Q30 queue summary rows.
