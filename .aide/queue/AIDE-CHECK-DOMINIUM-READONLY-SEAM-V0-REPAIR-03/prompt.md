# Prompt Summary

Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` as a substantial CHECK-only task.

The check must independently verify that `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` closes all 15 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`, preserves closure of earlier findings, introduces no material regression, and keeps the seam offline, deterministic, and read-only.

Allowed changes are limited to this check task directory, `.aide/reports/dominium-readonly-seam-v0-repair-03-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

If no material defect remains, recommend exactly `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`. If any bounded material defect remains, recommend exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`. Do not repair implementation in this task.
