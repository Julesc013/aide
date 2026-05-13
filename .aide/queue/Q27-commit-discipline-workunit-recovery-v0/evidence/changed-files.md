# Q27 Changed Files

Status: COMPLETE FOR REVIEW.

## Queue Governance

- `.aide/queue/index.yaml`: reopened Q27 implementation entry and moved it to review.
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/task.yaml`: canonical Q27 task packet.
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/ExecPlan.md`: restartable execution plan.
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/prompt.md`: Q27 redo prompt summary.
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/status.yaml`: final `needs_review` status.
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/evidence/*.md`: final evidence.

## Commit And Recovery Policy

- `.aide/policies/commit-messages.yaml`: structured Conventional Commit policy with required Markdown headings, changelog categories, validation tokens, trailers, and automation commands.
- `.aide/policies/task-resumption.yaml`: repeated-prompt and out-of-order task resumption policy.
- `.aide/policies/work-units.yaml`: WorkUnit identity, idempotency, state, evidence, no-op, recovery, and blocked semantics.
- `.aide/policies/recovery.yaml`: recovery profiles for duplicate, partial, stale, dirty, failed, conflicting, missing, and destructive states.
- `.aide/hooks/commit-msg`: opt-in local hook template.
- `.aide/git/commit-template.md`: reusable structured commit template.
- `.aide/git/README.md`: local Git governance entrypoint.

## Reports And Changelog Artifacts

- `.aide/reports/aide-commit-message-standard.md`: human-readable commit standard.
- `.aide/reports/aide-task-resumption-standard.md`: human-readable task resumption standard.
- `.aide/reports/aide-workunit-recovery-standard.md`: human-readable WorkUnit recovery standard.
- `.aide/changelog/CHANGELOG.preview.md`: deterministic preview changelog.
- `.aide/changelog/RELEASE_NOTES.preview.md`: deterministic preview release notes.
- `.aide/changelog/changelog.preview.json`: machine-readable preview data.
- `.aide/changelog/malformed-commits.md`: malformed commit audit output.

## AIDE Lite Tooling

- `.aide/scripts/aide_lite.py`: added commit, changelog, and task command families; Q27 validation anchors; Q27 golden checks; export-pack integration; and short task-id resolution for compact task packets.
- `.aide/commands/catalog.yaml`: documented Q27 command surfaces.

## Tests And Golden Tasks

- `.aide/scripts/tests/test_q27_commit_recovery.py`: commit parser, changelog, task recovery, hook/template, and no-op coverage.
- `.aide/scripts/tests/test_golden_tasks.py`: updated catalog-size expectation for expanded golden tasks.
- `.aide/evals/golden-tasks/catalog.yaml`: registered Q27 golden tasks.
- `.aide/evals/golden-tasks/commit_message_standard_golden/**`: commit standard golden task.
- `.aide/evals/golden-tasks/task_resumption_standard_golden/**`: task resumption golden task.
- `.aide/evals/golden-tasks/workunit_idempotency_golden/**`: WorkUnit idempotency golden task.
- `.aide/evals/golden-tasks/changelog_preview_golden/**`: changelog preview golden task.
- `.aide/evals/runs/latest-golden-tasks.json`: regenerated golden task run.
- `.aide/evals/runs/latest-golden-tasks.md`: regenerated golden task report.

## Documentation

- `README.md`: compact Q27 capability note.
- `ROADMAP.md`: Q27 phase position.
- `PLANS.md`: Q27 implementation record.
- `IMPLEMENT.md`: Q27 execution log.
- `DOCUMENTATION.md`: Q27 documentation index entry.
- `AGENTS.md`: Q27 agent guidance.
- `docs/reference/commit-discipline.md`: structured commit reference.
- `docs/reference/workunit-idempotency.md`: WorkUnit and recovery reference.
- `docs/reference/changelog-preview.md`: changelog preview reference.
- `docs/reference/README.md`: reference index entry.

## Generated And Exported Artifacts

- `.aide/context/latest-task-packet.md`: regenerated for Q28 Git Workflow Policy v0.
- `.aide/export/aide-lite-pack-v0/**`: regenerated portable pack with Q27 policies, hook/template, docs, tests, and golden tasks.
