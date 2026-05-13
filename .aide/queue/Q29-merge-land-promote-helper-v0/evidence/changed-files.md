# Q29 Changed Files

## Queue Governance

- `.aide/queue/Q29-merge-land-promote-helper-v0/task.yaml`: reopened Q29 as the active helper phase and ended at `needs_review`.
- `.aide/queue/Q29-merge-land-promote-helper-v0/status.yaml`: records implementation completion and pending review gate.
- `.aide/queue/Q29-merge-land-promote-helper-v0/ExecPlan.md`: restartable Q29 execution plan.
- `.aide/queue/Q29-merge-land-promote-helper-v0/prompt.md`: bounded implementation prompt.
- `.aide/queue/Q29-merge-land-promote-helper-v0/evidence/**`: final Q29 implementation, validation, safety, fixture, export, and risk evidence.
- `.aide/queue/index.yaml`: Q29 queue entry now points at `needs_review` / `review`.

## Helper Policy And Reports

- `.aide/git/helper-policy.yaml`: dry-run-first helper policy for sync, plan, land, promote, and prune.
- `.aide/git/helper-commands.md`: operator-facing command semantics and safety gates.
- `.aide/git/latest-helper-plan.json`: live-repo dry-run helper plan for current `main`.
- `.aide/git/latest-helper-plan.md`: human-readable live-repo helper plan.
- `.aide/git/workflow-detection.json`: regenerated current branch role and workflow report.
- `.aide/git/workflow-detection.md`: regenerated human-readable workflow report.

## AIDE Lite Commands And Tests

- `.aide/scripts/aide_lite.py`: added reusable Git helper safety model, dry-run/apply helper plan execution, command handlers, Q29 validation anchors, export integration, and Q29 golden task checks.
- `.aide/scripts/tests/test_q29_git_helper.py`: fixture Git repositories for land, promote, prune, dirty-tree, unknown-role, no-force-push, no-push, and report shape coverage.
- `.aide/scripts/tests/test_q28_git_workflow.py`: keeps Q28 command-surface checks compatible with the new Q29 Git subcommands.

## Golden Tasks

- `.aide/evals/golden-tasks/catalog.yaml`: added Q29 golden tasks.
- `.aide/evals/golden-tasks/git_helper_policy_golden/**`: helper policy anchor checks.
- `.aide/evals/golden-tasks/git_land_plan_golden/**`: task-to-dev dry-run plan checks.
- `.aide/evals/golden-tasks/git_promote_plan_golden/**`: dev-to-main dry-run plan checks.
- `.aide/evals/golden-tasks/git_prune_guard_golden/**`: prune containment and protected-role checks.
- `.aide/evals/golden-tasks/git_live_repo_no_mutation_golden/**`: live-repo no-mutation checks.
- `.aide/evals/runs/latest-golden-tasks.json`: regenerated 20/20 golden task run.
- `.aide/evals/runs/latest-golden-tasks.md`: regenerated human-readable golden task report.

## Documentation

- `README.md`: compact Q29 status and helper summary.
- `ROADMAP.md`: Q29 position and Q30 follow-up.
- `PLANS.md`: Q29 plan entry and validation summary.
- `IMPLEMENT.md`: execution log for helper policy, commands, fixtures, docs, and export.
- `DOCUMENTATION.md`: documentation index updated for Q29.
- `AGENTS.md`: branch-sensitive agent guidance now includes helper plan and no live merge/promote/prune rule.
- `docs/reference/README.md`: reference index includes Git helper workflow.
- `docs/reference/aide-lite.md`: command surface includes Q29 helper commands.
- `docs/reference/git-helper-workflow.md`: new Q29 helper workflow reference.
- `docs/reference/git-workflow-policy.md`: links Q28 policy to Q29 helper layer.
- `docs/reference/branch-roles.md`: branch roles now reference helper enforcement.
- `docs/reference/promotion-policy.md`: promotion policy now points at dry-run helper gates.

## Generated Artifacts

- `.aide/changelog/CHANGELOG.preview.md`: regenerated changelog preview.
- `.aide/changelog/RELEASE_NOTES.preview.md`: regenerated release notes preview.
- `.aide/changelog/changelog.preview.json`: regenerated structured preview.
- `.aide/changelog/malformed-commits.md`: regenerated malformed-commit report.
- `.aide/context/latest-task-packet.md`: regenerated for `Q30 AIDE Dev Main Policy Sync`.
- `.aide/export/aide-lite-pack-v0/**`: regenerated export pack with Q29 helper policy, docs, tests, and golden tasks.
