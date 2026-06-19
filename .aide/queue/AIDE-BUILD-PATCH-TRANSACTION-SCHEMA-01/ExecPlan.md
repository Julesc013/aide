# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01 ExecPlan

## Objective

Build the first minimal AIDE `PatchTransaction` vertical slice as a portable,
deterministic, schema-only record for proposed bounded repository mutations.

## Scope

- Add `aide-patch-transaction.schema.json`.
- Add `core/protocol/patch_transaction.py`.
- Register `patch-transaction status/project/validate` in `aide_lite.py`.
- Generate deterministic transaction, index, scope, projection, status,
  validation, explicit-non-capability, future-work, and next-task reports.
- Add a deterministic sample unified-diff artifact under the report directory.
- Add focused tests for identity, digest binding, deterministic projection,
  source immutability, fail-closed path scope, lifecycle/no-apply consistency,
  reference handling, and no-trust boundaries.
- Materialize queue metadata and evidence.

## Dependencies

- `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01` result:
  `ACCEPTED_WITH_WARNINGS`.
- `AIDE-OPERATIONAL-HEALTH-PAUSE-01` result:
  `PASS_WITH_WARNINGS`.
- Operational-health readiness authorizes this schema-only build before
  PatchTransaction check/accept and before any apply engine.

## Milestones

- Baseline authority verified from live queue and current Git state.
- Schema/helper/CLI/tests implemented.
- Deterministic reports generated.
- Task evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run Python compile checks, focused unit tests, `patch-transaction`
status/project/validate, predecessor protocol validators, task inspect/evidence
checks, broad AIDE validation, JSON parsing for generated JSON reports,
deterministic repeated-projection comparison, source-input byte comparison,
secret-like value scan, Git diff checks, and commit-policy validation.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, writes complete
evidence, preserves no-apply/no-approval/no-admission/no-trust semantics, keeps
scope validation fail-closed, generates one deterministic no-apply transaction
record, emits the next check prompt, and commits the bounded slice.

## Non-Capabilities

This task does not implement patch application, active or target repository
mutation, general diff generation or parsing, three-way merge, conflict
resolution, rollback execution, approval engine, policy engine, conformance
runner, automatic observation collection, profile activation, admission, trust,
AdapterManifest, ContextPack v2, Test Broker runtime, worker execution,
scheduler, leases, supervisor, Runtime, Service, Commander, Workbench, MCP/A2A
server behavior, provider/model/Gateway/network calls, GitHub mutation,
branch/worktree automation, release, promotion, production readiness, or broad
autonomous runtime behavior.
