# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

## Objective

Independently verify `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` at commit `84a154c2f03b304a987a9f017cc48a0b22c3f6d6` against the 15 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`, preserving all earlier closure and the offline, deterministic, read-only boundary.

## Scope

This is a CHECK-only task. Allowed outputs are limited to this check task directory, `.aide/reports/dominium-readonly-seam-v0-repair-03-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Non-Goals

Do not repair implementation, modify public schemas, production code, tests, fixtures, current seam outputs, Repair 03 reports, Repair 03 evidence, historical task records, Dominium, Git branches/worktrees, GitHub, releases, providers, network surfaces, workers, runtime, Workbench, bridge runtime, services, PreviewSession, PatchTransaction apply, or downstream WorkUnit validation.

## Work Packages

1. Verify live source-chain and replacement-gate preconditions.
2. Create task-local independent harnesses under `evidence/tools/`.
3. Check the 15 Repair 03 finding closures without using Repair 03 disposition as proof.
4. Resample earlier findings and review report consistency.
5. Probe public schema, fixture replay, conformance evidence, operation trace, guard evidence, runtime manifest, portability isolation, typed refusal, and Dominium immutability.
6. Run applicable validation commands, restore out-of-scope generated churn, and write evidence/reports.
7. Stop at `needs_review` with either `PASS_WITH_WARNINGS` and acceptance as the next task, or `REQUEST_CHANGES` and Repair 04 as the next task.

## Validation Intent

Use source-chain inspection, task inspect/evidence, Git object checks, JSON parsing, independent schema/source inspection, independent fixture replay, actual CLI refusal probes, command validation, Dominium state comparison, focused seam tests, broad validation, diff checks, secret-like scan, and commit-policy validation.

## Progress

- 2026-06-22: Initial live baseline verified on `main` with a clean worktree. Repair 03 exists at `84a154c2f03b304a987a9f017cc48a0b22c3f6d6`, predecessor evidence reports `missing_evidence: 0`, and the Repair 03 check/Repair 04/acceptance folders were absent before scaffold.
- 2026-06-22: Check task packet created and registered.
- 2026-06-22: Independent harness completed with `REQUEST_CHANGES`, 12 material findings, and 3 warnings.
- 2026-06-22: Validation matrix ran through compileall, seam unittest discovery, seam CLI commands, task evidence checks, broad validation, secret-like scan, and commit policy check.

## Result

The check stops at `needs_review` with `REQUEST_CHANGES`.

Recommended next task: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.

Material findings remain in schema discrimination and bounded extensions, fixture replay value/index/key strictness, conformance proof paths, operation aggregation and static guard evidence, portability required output comparison, and arbitrary unsupported CLI verb handling.

## Recovery

If interrupted, rerun `git status --short --branch`, inspect this `status.yaml`, restore any generated churn outside the allowlist, and continue from the first incomplete work package. Treat production seam commands as system-under-test invocations only; do not stage their generated output if they rewrite forbidden paths.

## Exit Criteria

Stop at `needs_review` only after material assertions are recorded, evidence files are present, queue evidence reports no missing required surfaces, no out-of-scope file drift remains, and exactly one next task is selected.

Exit criteria were met for this check task with a failing implementation result: the task produced complete evidence, did not repair the seam, preserved scope, and selected exactly one next task.
