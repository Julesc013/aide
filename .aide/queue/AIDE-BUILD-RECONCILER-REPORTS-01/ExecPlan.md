# AIDE-BUILD-RECONCILER-REPORTS-01 ExecPlan

## Objective

Implement the first Reconciler slice as deterministic report-only drift detection. The slice detects and reports queue, evidence, protocol report, ReferenceID, EventRecord, OKF, generated-context, source-hash, and overclaim risk classes without repairing or mutating source truth.

## Scope

Allowed writes are limited to the task directory, `.aide/reports/reconciler/**`, `core/reconciler/**`, the thin `aide_lite.py` dispatch, one focused unittest file, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Dependencies

- Accepted OKF knowledge bundle: `AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01`.
- Existing OKF projection and lint reports.
- Existing ReferenceID and EventRecord projection/validation reports.
- Queue policy requiring evidence and stop at `needs_review`.

## Implementation Plan

1. Add `core/reconciler/reconciler_reports.py` as the deterministic report-only helper.
2. Add `reconciler status`, `reconciler report`, and `reconciler validate` dispatch in `.aide/scripts/aide_lite.py`.
3. Add focused unit tests for findings, taxonomy, report-only boundary, CLI dispatch, JSON reports, and parser rejection of repair/runtime subcommands.
4. Generate `.aide/reports/reconciler/**`.
5. Record task evidence and stop at `needs_review`.

## Verification Intent

Run compile checks, focused Reconciler tests, Reconciler CLI status/report/validate, JSON parsing for the four JSON reports, predecessor validators, task inspect/evidence, broad validation, and git diff whitespace checks.

## Blockers

None. Known stale context and generated OKF report routing are expected warning-class Reconciler findings, not blockers for this report-only slice.

## Review Gate

Stop at `needs_review`. This task does not authorize Reconciler repair, source truth mutation, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, or promotion.
