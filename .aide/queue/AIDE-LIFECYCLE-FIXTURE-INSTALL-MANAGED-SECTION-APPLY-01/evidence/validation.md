# Validation

## Result

`BLOCKED_WITH_VALIDATION_PASS`

## Commands

- `git diff --check` - PASS.
- JSON parse of `.aide/reports/lifecycle-fixture-install-managed-section-apply/blocker-report.json` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01` - PASS for blocked classification; 13 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01` - PASS; 13 evidence files listed, none missing.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- Boundary scan for forbidden true mutation markers - PASS by no matches.
- Diff check over fixture targets, generated plans, expected reports, and `core/**` - PASS by no changed paths.

## Not Run

- Fixture apply dry-run - NOT_RUN because mutation authority is missing.
- Fixture apply execution - NOT_RUN because mutation authority is missing.
- Rollback dry-run and rollback apply - NOT_RUN because first apply did not execute.
- Token/quality ledger prompt-pack task - NOT_RUN because the requested all-green mutation proof chain is blocked at the first mutation authority gate.
