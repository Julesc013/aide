# ExecPlan: AIDE-CHECK-RECONCILER-REPORTS-01

## Objective

Perform an independent check-only review of `AIDE-BUILD-RECONCILER-REPORTS-01` and determine whether the report-only Reconciler slice is coherent, bounded, validated, and honest about non-capabilities.

## Scope

Allowed write scope is limited to this check task directory, `.aide/reports/reconciler-check/**`, `.aide/queue/index.yaml`, and the root planning/execution logs required for substantial queue work. The checked implementation, generated Reconciler build reports, protocol records, OKF pages, helper code, and tests are read-only for this check.

## Dependencies

- `AIDE-BUILD-RECONCILER-REPORTS-01` is present, indexed, and stopped at `needs_review`.
- Reconciler build reports exist under `.aide/reports/reconciler/`.
- The Reconciler CLI exposes only report-only `status`, `report`, and `validate` behavior.
- Predecessor OKF, EventRecord, ReferenceID, TestJob, WorkerRun, EvidencePacket, WorkUnit queue, and ContractEnvelope validation surfaces remain available.

## Plan

1. Inspect live repo state and governing queue policy.
2. Review the build task evidence, generated reports, command behavior, tests, and no-overclaiming boundaries.
3. Record independent review evidence for implementation scope, taxonomy, findings, drift treatment, OKF/protocol/reference/event compatibility, CLI behavior, validation, and forbidden operations.
4. Publish aggregate check reports under `.aide/reports/reconciler-check/`.
5. Stop at `needs_review` with `PASS_WITH_WARNINGS` and recommend `AIDE-ACCEPT-RECONCILER-REPORTS-01`.

## Verification Intent

Run focused Reconciler CLI checks, focused Reconciler unittest discovery, JSON parsing for build and check reports, predecessor validators, task inspect/evidence checks for the build and check tasks, broad `validate`, and Git whitespace checks. Generated report churn outside the check deliverable is restored after validation.

## Exit Criteria

- Check artifacts exist with complete evidence.
- `check-report.json` and build Reconciler JSON reports parse.
- Review result is `PASS_WITH_WARNINGS`.
- The check does not repair or mutate Reconciler implementation, OKF pages, protocol reports, ReferenceID/EventRecord artifacts, queue acceptance state, or generated latest task packets.
- The recommended next task is exactly `AIDE-ACCEPT-RECONCILER-REPORTS-01`.
- CapabilityManifest is not recommended directly from this check.

## Current Status

Completed and awaiting review.
