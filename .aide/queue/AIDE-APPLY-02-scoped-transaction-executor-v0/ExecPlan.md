# AIDE-APPLY-02 ExecPlan

## Purpose

Implement `AIDE-APPLY-02 - Scoped Transaction Executor v0` as the first narrowly bounded transaction executor for AIDE. The executor must operate only on explicit transaction plans, explicit operator-provided target paths, explicit allowed roots, and explicit operation allowlists. Managed-section update operations are the default allowed mutation class.

This plan began as the authorization scaffold. `AIDE-APPLY-02-IMPLEMENT` now uses it as the living control document for the scoped transaction executor v0 implementation and review-gated handoff.

## Scope

Allowed future implementation paths are the exact paths recorded in `task.yaml` and `allowed-paths.md`. The intended implementation may add a focused executor module, policy, schemas, examples, fixture tests, AIDE Lite command support, evidence reports, capability reality records, reference documentation, export-pack support, and generated manifest updates only inside the allowlist.

The future executor must support dry-run/report mode and may support explicit apply mode only for the scoped operation classes authorized in this task. Any future apply behavior must be path-bounded, operation-allowlisted, hash-aware, rollback-compatible, evidence-backed, and review-gated.

## Non-Goals

- No scoped transaction executor implementation in `AIDE-APPLY-02-AUTHORIZE`.
- No production-ready broad active-repo apply.
- No install apply.
- No upgrade apply.
- No repair apply.
- No rollback/uninstall apply.
- No target repo mutation.
- No branch/worktree mutation.
- No merge, push, promotion, tag, release, or publication.
- No GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad deletes or moves.
- No mutation outside explicit allowed paths.
- No self-promotion from review-gated to accepted or production-ready.

## Current Facts To Verify

- Repo root: `C:/Projects/AIDE/aide`.
- HEAD before authorization: `5c714e645b8ac4a6a1f22db1df2ae3ff8b4f39d3`.
- Branch before authorization: `main...origin/main`.
- `.aide/queue/current.toml`: absent.
- No `.aide/queue/AIDE-APPLY-02*` task existed before this authorization task.
- Latest task packet names `AIDE-APPLY-02 - Scoped Transaction Executor v0`.
- `AIDE-CHECK-APPLY-01-managed-section-patcher-review/status.yaml` names `AIDE-APPLY-02-scoped-transaction-executor-v0` as `next_action`.
- `AIDE-CHECK-APPLY-01` reports `AIDE-APPLY-01` as `ACCEPTED_WITH_NOTES` and `AIDE-APPLY-02` as `READY_FOR_AIDE_APPLY_02_WITH_WARNINGS`.
- `managed-section status` and `transaction status` preserve report-only or fixture-only boundaries; real repository apply is not broadly authorized.

## Future Implementation Requirements

### Inputs And Planning

The future executor must require:

- explicit transaction plan input;
- explicit target paths;
- explicit operation list;
- explicit allowed roots;
- explicit protected roots;
- explicit expected preimage hash;
- explicit expected postimage or postimage hash where feasible;
- explicit dry-run/apply mode;
- explicit report/evidence destination;
- explicit rollback-record destination.

### Path Safety

The future executor must:

- reject paths outside allowed roots;
- reject protected paths;
- reject absolute/relative path traversal ambiguity;
- normalize and compare paths deterministically;
- reject implicit broad scans unless separately authorized;
- reject broad deletes and moves unless separately authorized;
- preserve target repo boundaries.

### Operation Allowlist

The future executor must:

- allow only operations explicitly listed by live task policy;
- default to managed-section replacement/update operations;
- reject unsupported operations;
- reject missing operation type;
- reject ambiguous operation type.

### Managed-Section Boundary

The future executor must:

- operate only inside explicit managed markers by default;
- preserve manual content outside markers;
- block missing markers;
- block duplicate markers;
- block malformed markers;
- block nested markers;
- block ambiguous marker ownership;
- block unsupported files or encodings unless explicitly permitted.

### Hash And Image Checks

The future executor must:

- compute preimage hash before mutation;
- compare actual preimage hash to expected preimage hash;
- block mutation on preimage mismatch;
- verify postimage after planned mutation;
- detect and report postimage mismatch;
- record hashes in evidence.

### Transaction Records

The future executor must write:

- transaction plan record;
- staged-change records;
- rollback-compatible records;
- final report record.

Records must include deterministic identifiers or timestamps according to repo convention, plus file path, operation, preimage hash, postimage hash, validation status, and rollback reference.

### Modes

The future executor must ensure:

- dry-run/report mode does not mutate target files;
- apply mode is separately explicit;
- report-only command output is distinguishable from apply evidence;
- failure leaves clear evidence and avoids partial unreported mutation.

### Validation And Review

The future executor must include:

- targeted unit tests;
- fixture tests;
- managed-section validation;
- transaction validation;
- `git diff --check`;
- secret scan over changed files;
- evidence/review packet;
- status ending at review gate.

### Capability Reality

The future executor must label capability honestly:

- planned/specified before implementation;
- implemented/tested/review-gated only after code and tests exist;
- not production-ready;
- not install apply;
- not upgrade apply;
- not repair apply;
- not rollback/uninstall apply;
- not target-repo apply;
- not release-ready.

## Required Test Plan

Future targeted tests must cover:

- dry-run produces no file mutation;
- allowed managed-section replacement succeeds in fixture;
- disallowed path is blocked;
- protected path is blocked;
- path traversal is blocked;
- unsupported operation is blocked;
- missing operation is blocked;
- missing marker is blocked;
- duplicate marker is blocked;
- malformed marker is blocked;
- nested marker is blocked;
- ambiguous marker ownership is blocked;
- preimage hash mismatch is blocked;
- postimage mismatch is detected;
- rollback-compatible record is generated;
- staged-change record is generated;
- manual content outside markers is preserved;
- report/evidence output is generated;
- capability label is not overstated.

## Milestones

1. Re-verify live repo truth, queue state, worktree status, current task packet, and AIDE-APPLY-02 task packet.
2. Confirm exact allowed paths, protected paths, forbidden operations, and review gate from this scaffold.
3. Add the scoped executor policy/schema/report shape, if still required and within the allowlist.
4. Add a focused `core/apply/transaction_executor.py` implementation and import surface without broadening managed-section implementation.
5. Add AIDE Lite command support, fixtures, targeted tests, docs, generated reports, capability reality updates, export-pack support, and manifest updates inside the allowlist.
6. Run validation, write evidence, classify warnings, and set status to `needs_review`.
7. Hand off to `AIDE-CHECK-APPLY-02` for independent checkpoint review.

## Progress

- 2026-06-04: Authorization scaffold created by `AIDE-APPLY-02-AUTHORIZE`; no scoped transaction executor implementation performed.
- 2026-06-04: `AIDE-APPLY-02-IMPLEMENT` added `core/apply/transaction_executor.py`, scoped executor policy and schemas, scoped fixtures and examples, AIDE Lite `scoped-transaction` commands, targeted unit tests, reference docs, deterministic scoped executor reports, and implementation evidence.
- 2026-06-04: Core executor tests and AIDE Lite scoped-transaction command tests passed. `scoped-transaction validate`, `fixture-plan`, `fixture-verify`, and dry-run `run --plan` produced PASS results without target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, network calls, release publication, install/upgrade/repair/rollback/uninstall apply, or broad active-repo apply.

## Recovery

If interrupted before implementation starts, inspect `task.yaml`, `allowed-paths.md`, `protected-paths.md`, `forbidden-operations.md`, `validation-checklist.md`, `review-gate.md`, `status.yaml`, and `evidence/authorization-report.md`. Continue only if `authorization_status` remains `AUTHORIZED_FOR_IMPLEMENTATION`, the worktree is clean or unrelated dirt is classified, and the intended writes are inside the allowlist.

If a future implementation needs paths outside this scaffold, stop at the `permission_widening` review gate and create a narrow repair or authorization update task. Do not silently widen paths.

## Validation Intent

Run and record:

- `git status --short --branch`;
- `git diff --check`;
- `py -3 .aide/scripts/aide_lite.py task status`;
- `py -3 .aide/scripts/aide_lite.py managed-section status`;
- `py -3 .aide/scripts/aide_lite.py managed-section validate`;
- `py -3 .aide/scripts/aide_lite.py transaction status`;
- `py -3 .aide/scripts/aide_lite.py transaction validate`;
- targeted executor unit tests once implementation exists;
- fixture verification once fixtures exist;
- boundary text searches;
- local secret scan over changed files.

Generated report refreshes from status commands must be either inside the task allowlist or restored when they are unrelated churn.

## Retrospective

The implementation stayed inside the AIDE-APPLY-02 allowlist and reused the existing managed-section patcher instead of modifying it. Apply mode exists only as explicit scoped plan execution with preflight checks; validation exercised apply mode in temporary fixtures, while live AIDE command reports used dry-run/report mode. Capability reality remains implemented, tested, fixture-tested, report-backed, and review-gated, not production-ready, release-ready, target-repo capable, install/upgrade/repair/rollback/uninstall capable, or broad active-repo apply capable.
