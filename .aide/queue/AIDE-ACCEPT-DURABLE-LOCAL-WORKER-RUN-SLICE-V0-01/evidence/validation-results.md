# Validation Results

All validation commands passed.

| Command | Result |
| --- | --- |
| `py -3 .aide/scripts/aide_lite.py durable-worker-run validate` | `PASS_WITH_WARNINGS`; validated true; error_count 0; process_call_count 1; all false-boundary fields remained false. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01` | PASS; classification complete; missing_evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01` | PASS; evidence available; missing evidence empty. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01` | PASS; classification complete; missing_evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01` | PASS; evidence available; missing evidence empty. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01` | PASS; classification complete; missing_evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01` | PASS; evidence available; missing evidence empty. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS. |
| `git diff --check` | PASS. |
| `git diff --cached --check` | PASS. |
| Scoped leak/path scan over this acceptance task and report files | PASS; no local absolute paths or secret-like assignment markers found. |

Worktree churn review:

- No unrelated generated files were modified.
- Dirty paths are limited to this acceptance task, its acceptance reports,
  `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
