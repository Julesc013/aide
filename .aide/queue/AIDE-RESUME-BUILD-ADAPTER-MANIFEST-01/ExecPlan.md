# AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01 ExecPlan

## Purpose

Build a minimal AdapterManifest protocol slice after repaired PatchTransaction
acceptance. The task resumes the blocked AdapterManifest build lane without
rewriting the original blocked task.

## Scope

Allowed changes are limited to the AdapterManifest schema, helper, AIDE Lite
dispatch, focused tests, deterministic reports, this task packet/evidence,
queue index, and root planning/log updates.

## Non-Goals

No adapter admission, trust, worker execution, test execution, sandbox creation,
credential resolution, provider/model/Gateway/network call, GitHub mutation,
branch/worktree automation, patch apply, target repository mutation, runtime,
Service, Commander, Workbench, Test Broker, ContextPack v2, release, or
promotion behavior is authorized.

## Progress

- Live queue truth confirmed the original `AIDE-BUILD-ADAPTER-MANIFEST-01`
  remains a blocked historical record.
- `AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` accepted the repaired
  PatchTransaction no-apply protocol slice with warnings and recommended this
  resume build task.
- Added a declaration-only AdapterManifest schema and helper.
- Added thin AIDE Lite `adapter-manifest status/project/validate` dispatch.
- Added focused unit tests for identity, references, fail-closed boundaries,
  non-capabilities, deterministic projection, and CLI behavior.
- Generated deterministic AdapterManifest reports.

## Validation Intent

Run Python compilation, focused AdapterManifest tests, AdapterManifest
status/project/validate commands, predecessor protocol validators, task
inspect/evidence checks, broad AIDE validation, JSON parsing, deterministic
projection review, source immutability review, secret-like scan, Git diff
checks, and commit-policy validation.

## Recovery

If validation fails, preserve this task packet and generated evidence, classify
the defect, and route to a bounded AdapterManifest repair task. Do not rewrite
the original blocked AdapterManifest records.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, complete evidence, no
capability acceptance or admission, no forbidden operation, and exactly one next
task: `AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01`.
