# QCHECK Cross-Repo Adapter Readiness Audit ExecPlan

This checkpoint is a bounded report-first audit. It verifies AIDE state after
QFIX-01, QFIX-02, Q21, and Q24, and it checks whether Q22/Q23 target-pilot
evidence exists. It does not implement fixes.

## Scope

- Inspect AIDE git, queue, policy, export/import, adapter, generated-report, and
  validation state.
- Inspect local Eureka and Dominium repositories read-only if present.
- Run AIDE Harness, AIDE Lite, adapter, export-pack, gateway, provider, and test
  commands that are local and no-call.
- Write checkpoint audit reports under this queue directory.
- Add the checkpoint to `.aide/queue/index.yaml`.
- Commit audit artifacts if safe.

## Non-Goals

- No product implementation.
- No Q25 work.
- No Eureka or Dominium mutation.
- No adapter template fixes.
- No Gateway/provider/model/runtime work.
- No provider/model/network calls.
- No raw prompt, raw response, secret, or `.aide.local/` commits.

## Execution Steps

1. Inspect git and queue state.
2. Inspect QFIX-01, QFIX-02, Q21, and Q24 status/evidence.
3. Check whether Q22/Q23 evidence exists in AIDE.
4. Inspect local Eureka/Dominium repos read-only if available.
5. Run validation and command sweep.
6. Run test suites and secret/local-state checks.
7. Write main and supplemental reports.
8. Run final structural validation.
9. Commit audit artifacts if unrelated dirty work is not present.

## Current Finding Summary

AIDE Pack, AIDE Lite validation, and adapter compiler are locally working in the
AIDE repo. Q22/Q23 target-pilot evidence is absent from AIDE, and the available
local Eureka/Dominium repos do not show the Q21 pack imported. Eureka handover
is therefore conditional: AIDE is ready for a controlled Eureka import/handover
pilot, not for treating Eureka token-saving proof as already established.
