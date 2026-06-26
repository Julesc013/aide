# Validation

Initial independent harness result:

- `py -3 .aide/queue/AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01/evidence/independent_check.py`: PASS

The harness generated `.aide/reports/ownership-ledger-v1-repair-01-check/check-report.json` with:

- result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`

Final outer validation commands are appended in `validation-results.md`.

Outer validation after queue/log updates:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01`: PASS; classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01`: PASS; missing evidence list empty.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- Strict changed-file absolute-path/secret scan: PASS after excluding a broad `sk-` false-positive pattern that matched ordinary task IDs.
