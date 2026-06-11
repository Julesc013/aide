# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git diff --check` - PASS.
- JSON parse of `authority-packet.json` and `authority-decision.json` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01` - PASS; classification complete, 15 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01` - PASS; 15 evidence files listed, none missing.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks. One parallel run returned `MemoryError`; serial rerun passed.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- Boundary scan for unauthorized true execution/mutation markers - PASS by no matches.
- Diff check over fixture targets, generated plans, expected reports, and `core/**` - PASS by no changed paths.

## Not Run

- Fixture apply execution - NOT_RUN because this is an authority task only.
- Rollback execution - NOT_RUN because this task does not authorize rollback execution.

## Warning Classification

- Global `task next-plan` selector lag remains non-blocking; task-local next batch selects `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01-RETRY`.
- `transaction status` refreshed `.aide/reports/current-aide-roadmap.md`; that out-of-scope generated churn was restored before commit.
