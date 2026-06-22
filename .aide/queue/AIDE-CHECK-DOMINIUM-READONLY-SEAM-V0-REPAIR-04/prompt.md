# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.

Use `.aide/queue/index.yaml` as canonical queue truth. This is a CHECK-only task.

Independently verify that `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` closes the exact 12 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` without reopening earlier safety invariants or widening the offline read-only boundary.

Do not modify production code, schemas, tests, fixtures, generated seam outputs, Repair 04 reports/evidence, historical task records, or Dominium. Create independent tools only under this task's evidence directory.

If all material checks pass, stop at `needs_review` with `PASS_WITH_WARNINGS` and recommend exactly `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`. If a material defect remains, stop at `needs_review` with `REQUEST_CHANGES` and recommend exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
