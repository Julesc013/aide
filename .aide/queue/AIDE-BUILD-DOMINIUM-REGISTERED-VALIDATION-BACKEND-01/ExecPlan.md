# ExecPlan: AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

## Objective

Build a narrow AIDE registered validation backend that proves exactly one
bounded read-only invocation of Dominium's `dominium.validation.run` command
through `apps/workbench/module/validation/cli.py`, `run_validation_command()`,
and `ValidationServiceAdapter`.

## Scope

Allowed changes are limited to the new backend module, AIDE Lite CLI wiring,
focused fake-runner tests, this task packet/evidence, the backend report
directory, the queue index, and focused root plan/execution log entries.

The task may read and execute one local pinned Dominium CLI process through an
exact allowlisted argv. It may not mutate Dominium, create branches or
worktrees, dispatch arbitrary commands, call providers/models/network, run
workers, start Workbench or Service behavior, preview/apply/rollback, or invoke
GitHub/release behavior.

## Plan

1. Confirm accepted fixture-backed predecessor and clean AIDE worktree.
2. Add a separate registered validation backend without changing the accepted
   fixture-backed adapter.
3. Add preflight checks for repository identity, pinned revision, clean status,
   required command files, command id, and command implementation digests.
4. Add a single subprocess seam with `shell=False`, exact argv, sanitized
   environment, timeout, separate stdout/stderr capture, and fake-runner test
   injection.
5. Normalize Dominium stdout JSON into typed AIDE result/refusal records and
   deterministic ContextDescriptor, ContextPack, WorkUnit, EvidencePacket,
   EventRecord, projection, and validation outputs.
6. Run focused fake-runner tests, execute the live Dominium CLI exactly once,
   run validation, record evidence, and stop at `needs_review`.

## Progress

- [x] Predecessor queue state reviewed.
- [x] Local Dominium checkout presence reviewed.
- [x] Backend module implemented.
- [x] CLI wiring added.
- [x] Focused tests added.
- [x] Live command invoked exactly once.
- [x] Reports and task evidence written.
- [x] Validation completed.

## Exit

Result is `PASS_WITH_WARNINGS`. The registered backend proved a single real
Dominium CLI process invocation, source state remained unchanged, evidence is
complete, and the next task is exactly
`AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.
