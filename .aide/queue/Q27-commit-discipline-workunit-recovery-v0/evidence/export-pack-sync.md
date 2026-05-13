# Q27 Export Pack Sync

Status: COMPLETE FOR REVIEW.

## Exported Q27 Files

- `.aide/policies/commit-messages.yaml`
- `.aide/policies/task-resumption.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/recovery.yaml`
- `.aide/hooks/commit-msg`
- `.aide/git/commit-template.md`
- `.aide/git/README.md`
- `.aide/reports/aide-commit-message-standard.md`
- `.aide/reports/aide-task-resumption-standard.md`
- `.aide/reports/aide-workunit-recovery-standard.md`
- `.aide/evals/golden-tasks/commit_message_standard_golden/**`
- `.aide/evals/golden-tasks/task_resumption_standard_golden/**`
- `.aide/evals/golden-tasks/workunit_idempotency_golden/**`
- `.aide/evals/golden-tasks/changelog_preview_golden/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q27_commit_recovery.py`
- `.aide/scripts/tests/test_golden_tasks.py`
- `docs/reference/commit-discipline.md`
- `docs/reference/workunit-idempotency.md`
- `docs/reference/changelog-preview.md`

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- Included files: 144.
- Checksum count: 147.
- Checksums valid: true.
- Boundary result: PASS.
- Provenance result: `DIRTY_SOURCE_RECORDED` during implementation, as expected before the final commit.
- Provider/model calls: none.
- Network calls: none.

## Target Import Implications

- Future Eureka/Dominium imports receive commit discipline policy, WorkUnit recovery policy, hook/template files, command support, docs, tests, and golden tasks.
- Source repo generated changelog previews are not target truth; target repos must generate their own previews from local commit history.
- The hook is exported as a template and remains opt-in.
