# ExecPlan: AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

## Objective

Independently check `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` at
commit `8d8f511c77388b96118eb530f5361090b66911c1`, with special attention to
the authority distinction between fixture-backed adapter execution and live
Dominium-owned command execution.

## Scope

Check-only. Do not modify implementation, tests, fixtures, generated build
reports, Dominium, protocols, or CLI behavior.

Allowed outputs are the check task packet, task-local evidence, check reports,
queue index registration, and root plan/log updates.

## Plan

1. Verify branch, worktree, source build task, and source commit.
2. Inspect the WorkUnit validation implementation and build reports.
3. Run a task-local independent harness that instruments the fixture executor,
   recomputes workspace digests, probes typed refusals, checks determinism,
   resolves evidence/event references, and scans for leakage.
4. Decide whether the build proves live Dominium command execution or only a
   fixture-backed adapter contract.
5. Record reports, evidence, warning disposition, and the exact next task.
6. Stop at `needs_review`.

## Progress

- [x] Baseline and source task checked.
- [x] Independent harness written under task evidence.
- [x] Executor call counting, refusal, digest, determinism, leakage, evidence,
  event, and boundary checks run.
- [x] Authority distinction recorded.
- [x] Reports and evidence materialized.
- [ ] Acceptance completed.

## Exit

Result is `PASS_WITH_WARNINGS` with zero material findings. Recommend exactly
`AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
