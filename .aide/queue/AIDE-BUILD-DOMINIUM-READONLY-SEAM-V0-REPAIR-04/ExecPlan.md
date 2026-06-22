# AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

## Objective

Repair the 12 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` without redesigning the AIDE-Dominium seam or implementing later runtime, WorkUnit validation, provider, worker, network, or mutation behavior.

## Scope

This task is limited to the existing offline read-only seam schema, helpers, validator, conformance evidence, operation auditability, portability proof, typed refusal surface, focused tests, generated seam artifacts, Repair 04 reports, queue packet, and root planning/execution logs.

## Non-Goals

Do not accept the seam, run the independent Repair 04 check, modify Dominium, invoke Dominium commands, implement Host runtime, Workbench, bridge runtime, services, databases, network transport, provider/model calls, worker dispatch, PatchTransaction apply, PreviewSession, rollback, target repository mutation, branch/worktree automation, GitHub mutation, release, promotion, or the WorkUnit validation slice.

## Allowed Paths

Use the allowlist in `task.yaml`. Historical build, check, Repair 01, Repair 02, Repair 03, and check-report roots are read-only evidence for this task.

## Work Packages

1. Baseline and preservation: verify live queue truth, predecessor evidence, Repair 03 findings, absence of downstream replacement, and before hashes for historical roots.
2. Schema convergence: add a real `SeamRecord` union, preserve kind-specific schemas, and bound authority-changing extension values.
3. Fixture replay convergence: require `value` for add/replace/append, reject unicode decimal indexes, and reject the complete forbidden executable-key set.
4. Conformance convergence: prove unsupported operations through actual CLI dispatch, surround actual seam operations with no-write evidence, and exercise guard code paths.
5. Operation auditability convergence: preserve semantic aggregate dimensions and make guard reports recomputable rather than static.
6. Portability and refusal convergence: compare the complete child output set and route arbitrary unsupported verbs through typed refusal output.
7. Reports and evidence: regenerate seam artifacts, write Repair 04 reports, add focused tests, and stop at `needs_review`.

## Validation

Run focused Dominium seam tests through Repair 04, source and behavior probes for the 12 findings, seam CLI `status/snapshot/project/validate/diff/demo`, task inspect/evidence, broad `validate`, diff checks, secret-like scan, and commit policy check where practical. If an aggregate command is too slow, run the relevant suites individually and record the substitution.

## Progress

- 2026-06-22: Live queue baseline verified. Repair 03 check reports `REQUEST_CHANGES`, 12 material findings, and recommends this task. No Repair 04 build or check task directory existed before this scaffold.
- 2026-06-22: Task packet created and registered.
- 2026-06-22: Implemented schema union and extension bounds, strict fixture replay, actual CLI unsupported-operation probes, no-write operation evidence, exercised guard evidence, semantic operation aggregation, complete portability output comparison, and arbitrary unsupported-verb typed refusal routing.
- 2026-06-22: Regenerated current seam outputs and Repair 04 report/evidence roots. Focused Repair 04 tests, targeted prior repair/base tests, seam commands, and standalone portability proof passed; older full portability-heavy suites exceeded timeout and were replaced by targeted plus standalone coverage.

## Decisions

- Unsupported operation proof remains typed refusal evidence for the read-only seam; it does not authorize runtime execution, workers, providers, network calls, or repository mutation.
- Independent Repair 04 verification is intentionally deferred to `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.

## Recovery

If interrupted, re-run the baseline checks first, inspect `status.yaml`, preserve historical evidence roots, and continue from the first incomplete work package. Do not treat generated artifacts as canonical unless validation and evidence identify them as regenerated outputs for this task.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS` only when all 12 finding dispositions are complete, focused and broad validation pass or are honestly recorded with blockers, historical evidence remains unchanged, Dominium remains unchanged, and the only recommended next task is `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.

## Retrospective

Repair 04 closes the authorized findings in the build surface and records the remaining risks: full older Repair 02/03 suites are portability-heavy and exceeded the interactive timeout, non-Windows platforms were not separately executed, and acceptance still requires an independent check.
