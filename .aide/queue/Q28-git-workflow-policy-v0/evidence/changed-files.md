# Q28 Changed Files

## Queue Governance

- `.aide/queue/index.yaml`: moved Q28 redo through implementation toward review.
- `.aide/queue/Q28-git-workflow-policy-v0/task.yaml`: Q28 task packet and acceptance anchors.
- `.aide/queue/Q28-git-workflow-policy-v0/ExecPlan.md`: restartable execution plan.
- `.aide/queue/Q28-git-workflow-policy-v0/prompt.md`: prompt summary.
- `.aide/queue/Q28-git-workflow-policy-v0/status.yaml`: final status target is `needs_review`.
- `.aide/queue/Q28-git-workflow-policy-v0/evidence/*.md`: Q28 evidence.

## Policy And Git Artifacts

- `.aide/policies/git-workflow.yaml`: default trunk-with-dev-integration branch model.
- `.aide/policies/branch-roles.yaml`: canonical, integration, task, review, release, hotfix, deploy, and unknown role semantics.
- `.aide/policies/promotion-rules.yaml`: task-to-dev, dev-to-main, release, hotfix, and deploy branch promotion gates.
- `.aide/policies/sync-policy.yaml`: multi-machine sync policy and report-only Q28 boundary.
- `.aide/policies/prune-policy.yaml`: prune only after containment, protected branch guards, and Q28 no-delete boundary.
- `.aide/policies/task-resumption.yaml`: branch-role preflight for resumed/repeated tasks.
- `.aide/policies/work-units.yaml`: branch-aware WorkUnit preflight and recovery notes.
- `.aide/git/README.md`: Git workflow artifact index.
- `.aide/git/branch-roles.md`: human-readable branch-role guide.
- `.aide/git/promotion-rules.md`: promotion gate guide.
- `.aide/git/sync-policy.md`: sync policy guide.
- `.aide/git/prune-policy.md`: prune policy guide.
- `.aide/git/project-profiles.yaml`: workflow profiles for AIDE, Eureka, Dominium, website, native-client, connector-heavy, data-snapshot, and unknown repos.
- `.aide/git/workflow-detection.json`: generated local report-only workflow detection.
- `.aide/git/workflow-detection.md`: generated human-readable detection report.

## AIDE Lite, Tests, And Golden Tasks

- `.aide/scripts/aide_lite.py`: added Q28 Git policy validators, branch-role classifiers, workflow detection, `git` commands, export-pack inclusion, validation anchors, selftest fixture coverage, and golden task runners.
- `.aide/scripts/tests/test_q28_git_workflow.py`: unit tests for branch role classification, workflow heuristics, report writing, command shape, and non-mutation.
- `.aide/evals/golden-tasks/catalog.yaml`: added Q28 golden task ids.
- `.aide/evals/golden-tasks/git_workflow_policy_golden/**`
- `.aide/evals/golden-tasks/branch_role_detection_golden/**`
- `.aide/evals/golden-tasks/promotion_rules_golden/**`
- `.aide/evals/golden-tasks/sync_policy_golden/**`
- `.aide/evals/golden-tasks/prune_policy_golden/**`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `.aide/commands/catalog.yaml`
- `docs/reference/README.md`
- `docs/reference/aide-lite.md`
- `docs/reference/git-workflow-policy.md`
- `docs/reference/branch-roles.md`
- `docs/reference/promotion-policy.md`

## Regenerated Artifacts

- `.aide/changelog/CHANGELOG.preview.md`
- `.aide/changelog/RELEASE_NOTES.preview.md`
- `.aide/changelog/changelog.preview.json`
- `.aide/changelog/malformed-commits.md`
- `.aide/context/latest-task-packet.md`: regenerated for Q29 Merge Land Promote Helper v0.
- `.aide/export/aide-lite-pack-v0/**`: regenerated portable pack with Q28 policies, docs, tests, and golden tasks.
