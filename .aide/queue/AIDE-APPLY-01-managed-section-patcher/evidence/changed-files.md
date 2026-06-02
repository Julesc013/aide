# Changed Files

## Direct Queue Packet

- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/**`: task packet, ExecPlan, prompt copy, status, and evidence records.
- `.aide/queue/index.yaml`: registered AIDE-APPLY-01 as `needs_review`.
- `.aide/context/latest-task-packet.md`: points the next bounded task at `AIDE-CHECK-APPLY-01`.
- `.aide/context/latest-review-packet.md`: regenerated review packet for the review gate.

## Managed-Section Contract

- `.aide/policies/managed-section-markers.yaml`
- `.aide/policies/managed-sections.yaml`
- `.aide/apply/managed-section-operation.schema.json`
- `.aide/apply/managed-section-patch.schema.json`
- `.aide/apply/managed-section-conflict.schema.json`
- `.aide/apply/managed-section-report.schema.json`
- `.aide/examples/apply/managed-section*.json`
- `.aide/examples/apply/managed-section-fixtures/**`

## Implementation, Tests, And Docs

- `core/apply/**`: reusable managed-section parser, patch planner, fixture patcher, and tests.
- `.aide/scripts/aide_lite.py`: report-only `managed-section` commands, validation hooks, golden runners, and export-pack inclusion.
- `.aide/scripts/tests/test_aide_apply_01_managed_sections.py`
- `.aide/evals/golden-tasks/managed_section_*`
- `docs/reference/managed-section-patcher.md`
- `docs/reference/managed-section-operations.md`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`

## Generated Evidence

- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/task-os-*`
- `.aide/reports/capability-*`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/evals/runs/latest-golden-tasks.*`
- `.aide/export/aide-lite-pack-v0/**`

## Separate Direct User Request

- `.gitignore` was committed separately as `2204d99 chore(gitignore): ignore tmp scratch directory`.
- Local `tmp/**` archive files remain ignored and were not promoted.
