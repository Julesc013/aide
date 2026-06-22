# AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

## Objective

Repair the 15 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` without redesigning the AIDE-Dominium seam or implementing later runtime, WorkUnit validation, provider, worker, network, or mutation behavior.

## Scope

This task is limited to the existing offline read-only seam schema, helpers, validator, conformance evidence, operation auditability, portability proof, typed refusal surface, focused tests, generated seam artifacts, Repair 03 reports, queue packet, and root planning/execution logs.

## Non-Goals

Do not accept the seam, run the independent Repair 03 check, modify Dominium, invoke Dominium commands, implement Host runtime, Workbench, bridge runtime, services, databases, network transport, provider/model calls, worker dispatch, PatchTransaction apply, PreviewSession, rollback, target repository mutation, branch/worktree automation, GitHub mutation, release, or promotion.

## Allowed Paths

Use the allowlist in `task.yaml`. Historical build, check, Repair 01, Repair 02, and check-report roots are read-only evidence for this task.

## Work Packages

1. Baseline and preservation: verify live queue truth, predecessor evidence, Repair 02 findings, absence of downstream replacement, and before hashes for historical roots.
2. Schema hardening: make kind-specific specs explicit, use portable kind discrimination, close unbounded authority-changing fields, and require all false-boundary facts as `const false`.
3. Fixture replay hardening: enforce strict add/remove/replace/append, canonical array indexes, pointer validation, and executable-content rejection.
4. Conformance evidence: consume explicit evidence bundles, prove unsupported operations through actual CLI probes, prove no-write with before/after Dominium state, and use guard evidence for network/provider/worker/mutation claims.
5. Operation auditability: write complete `operation-trace.json`, recomputable ledger aggregates, correct Git classification, separate guard-conformance evidence, and truthful coverage statuses.
6. Portability isolation: drive portable copies from the serialized manifest, verify manifest hashes and AST import closure, sanitize environment, use isolated processes, compare complete output sets, and scan for local absolute path leaks.
7. Typed refusal and reports: route unsupported verbs through one typed refusal handler, regenerate seam artifacts, write Repair 03 disposition reports, expand focused tests, and stop at `needs_review`.

## Validation

Run the focused Dominium seam test suites, direct regression probes for all 15 findings, seam CLI `status/snapshot/project/validate/diff/demo`, task inspect/evidence, broad `validate`, diff checks, secret-like scan, and commit policy check where practical. If an aggregate command is too slow, run the relevant suites individually and record the substitution.

## Progress

- 2026-06-22: Live queue baseline verified. Repair 02 check still reports `REQUEST_CHANGES`, 15 material findings, and recommends this task. No Repair 03 task directory existed before this scaffold.
- 2026-06-22: Task packet created and registered.
- 2026-06-22: Implemented schema, fixture replay, conformance evidence, operation ledger, portability, and typed refusal hardening for the 15 material findings.
- 2026-06-22: Regenerated the seam bundle, fixtures, bridge manifest, conformance evidence, operation trace, guard conformance, and Repair 03 report set.
- 2026-06-22: Focused seam tests, Repair 01/02/03 regression suites, seam CLI validation, immutability checks, broad validation, and diff checks passed or were recorded with warnings. The task is stopped at `needs_review` with `PASS_WITH_WARNINGS`.

## Decisions

- Unsupported operation proof remains typed refusal evidence for the read-only seam; it does not authorize runtime execution, workers, providers, network calls, or repository mutation.
- Independent Repair 03 verification is intentionally deferred to `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.

## Recovery

If interrupted, re-run the baseline checks first, inspect `status.yaml`, preserve historical evidence roots, and continue from the first incomplete work package. Do not treat generated artifacts as canonical unless validation and evidence identify them as regenerated outputs for this task.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS` only when all 15 finding dispositions are complete, focused and broad validation pass or are honestly recorded with blockers, historical evidence remains unchanged, Dominium remains unchanged, and the only recommended next task is `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.

## Retrospective

Repair 03 closes the authorized findings in the build surface and records the remaining risks: local Dominium is behind `origin/main`, cross-platform execution was not rerun outside Windows, and acceptance still requires an independent check.
