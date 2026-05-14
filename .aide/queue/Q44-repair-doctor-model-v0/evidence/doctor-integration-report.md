# Doctor Integration Report

## Policy

`.aide/policies/doctor.yaml` defines repair doctor behavior:

- doctor output may cite the latest repair report.
- doctor may recommend reviewing a repair plan.
- doctor must not apply repair.
- doctor remains conservative and advisory.

## AIDE Lite Integration

`py -3 .aide/scripts/aide_lite.py doctor` now reports repair plan/report
availability when Q44 outputs exist. It does not fail solely because repair
warnings exist and does not perform repair actions.

## Repair Doctor

Command: `py -3 .aide/scripts/aide_lite.py repair doctor`

- report path: `.aide/repair/latest-doctor-repair-report.json`
- markdown path: `.aide/repair/latest-doctor-repair-report.md`
- doctor_status: `WARN`
- repair_recommended: true
- blocking issues: 0
- no_apply: true

## Boundary

Repair doctor is advisory only. It performs no repair apply, overwrite,
delete, migration, install, upgrade, rollback, or target mutation.
