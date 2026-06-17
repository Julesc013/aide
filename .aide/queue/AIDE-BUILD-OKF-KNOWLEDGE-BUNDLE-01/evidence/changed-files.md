# Changed Files

## Implementation

- `core/knowledge/__init__.py`: adds knowledge helper package export.
- `core/knowledge/okf_bundle.py`: adds deterministic OKF-compatible projection, frontmatter parsing/validation, report generation, lint, and validation.
- `.aide/scripts/aide_lite.py`: adds thin `okf status/project/validate/lint` dispatch.
- `.aide/scripts/tests/test_aide_okf_knowledge_bundle.py`: adds focused OKF bundle tests.

## Generated Knowledge And Reports

- `.aide/knowledge/okf/**`: generated OKF-compatible markdown bundle.
- `.aide/reports/okf/**`: generated projection, validation, lint, concept index, link index, status, future-work, and unfinished-work reports.

## Queue And Logs

- `.aide/queue/AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01/**`: task packet and evidence.
- `.aide/queue/index.yaml`: records the new task.
- `PLANS.md`: records the plan entry.
- `IMPLEMENT.md`: records the execution log entry.
