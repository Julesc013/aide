# Immutability And Determinism

Confirmed:

- acceptance did not modify `.aide/interop/exports/**`;
- acceptance did not modify `.aide/reports/interop-exports/**`;
- acceptance did not modify `.aide/reports/interop-exports-check/**`;
- accepted predecessor records remained unchanged;
- generated OKF pages remained unchanged;
- manifest/report order is stable and consistent between manifest and build
  report;
- repeated hash recomputation is stable.
