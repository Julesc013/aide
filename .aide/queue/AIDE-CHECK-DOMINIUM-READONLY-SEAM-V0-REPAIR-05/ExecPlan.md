# ExecPlan: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05

## Objective

Independently check the committed Repair 05 build for the four remaining
Dominium read-only seam blockers and decide whether acceptance may proceed.

## Scope

Allowed edits are limited to this check task directory, the matching check
report directory, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
Production seam code, schemas, fixtures, tests, generated seam outputs, Repair
05 build reports, and Dominium are read-only inputs.

## Plan

1. Reconfirm source-chain baseline, clean worktree, Repair 05 build evidence,
   and absent downstream tasks.
2. Capture production tree hashes before check execution.
3. Run an evidence-local independent harness for the four finding closures:
   schema surface closure, semantic extension refusal, exercised guard dispatch,
   and non-static guard report generation.
4. Sample critical prior invariants: schema discrimination, fixture replay
   strictness, arbitrary unsupported CLI refusal, no-write evidence, raw trace
   auditability, portability output set, and Dominium immutability.
5. Capture production tree hashes after check execution and compare to the
   before snapshot.
6. Write required check reports, validation evidence, queue status, and routing.
7. Run validation and commit this check separately.

## Verification

The check records machine-readable assertions in `check-report.json`, source
finding dispositions in `four-finding-closure.json`, and validation commands in
task-local evidence.

## Review Gate

Stop at `needs_review`. If material findings remain, route to
`AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-06` and do not begin acceptance.
If zero material findings remain, route to
`AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.
