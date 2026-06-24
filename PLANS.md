# AIDE Planning Index

## Purpose

`PLANS.md` is the repository's working plan index for substantial engineering work. It exists to track real execution intent, dependencies, milestones, blockers, and verification plans. It is not a marketing roadmap.

## How Plans Are Structured

- Each substantial work item should have a stable identifier such as `P00`, `P01`, or a later program-specific id.
- A plan entry should describe one coherent objective.
- Plans should be updated as work progresses rather than rewritten after the fact.
- Status values should be explicit, for example `proposed`, `active`, `blocked`, `completed`, or `superseded`.

## Recommended Fields For A Plan Entry

- `Plan ID`
- `Title`
- `Status`
- `Objective`
- `Scope`
- `Allowed Paths`
- `Dependencies`
- `Milestones`
- `Blockers`
- `Verification Intent`
- `Exit Criteria`
- `Notes`

## Dependency Tracking

- Record upstream dependencies that must exist before the plan can finish.
- Record downstream work that depends on the plan when that relationship matters to execution order.
- Reference authoritative docs or prompts rather than relying on memory.

## Milestone Tracking

- Break work into small milestones with observable completion criteria.
- Use milestones to separate governance, scaffolding, implementation, verification, and packaging when those phases differ.
- Mark milestones complete only when the corresponding verification intent has been satisfied.

## Blocker Tracking

- Record blockers explicitly and name whether they are internal or external.
- Distinguish blocked work from intentionally deferred work.
- Remove or downgrade a blocker only when the blocking condition is actually resolved.

## Verification Intent

- State how the plan will be verified before the work is declared complete.
- Verification intent may include file checks, schema checks, tests, evals, or structural review depending on the task.
- If only structural verification is possible, say so up front.

## Entry Template

```md
### Plan ID: PX

- Title:
- Status:
- Objective:
- Scope:
- Allowed Paths:
- Dependencies:
- Milestones:
- Blockers:
- Verification Intent:
- Exit Criteria:
- Notes:
```

## Current Plan Index

### Plan ID: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

- Title: Repair Registered Process Execution Provider v0 Safety Findings
- Status: needs_review
- Objective: repair the five material safety findings from `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01` without accepting or widening the provider.
- Scope: generic provider safety behavior, focused provider regression tests, repair reports, task/evidence, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01` at commit `e1ae28892c34e66ac03e61f89efe635efa0641e0`, result `REQUEST_CHANGES`, with five material findings.
- Milestones: repair task materialized; pre-launch binding coherence checks added; per-invocation launch receipts fixed; decoder and state-probe failure axes made incomplete/fail-closed; process cancellation declared unsupported; focused provider and Dominium parity tests passed; task evidence and reports written.
- Blockers: provider acceptance remains blocked until an independent repair check passes.
- Verification Intent: Python compile, focused provider tests, focused Dominium parity tests, genericity scans, JSON parsing, task inspect/evidence, broad validation, leakage scans, diff checks, staged diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, provider still unaccepted, and next task exactly `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.
- Notes: this task does not implement cancellation, accept the provider, add Omnigent/ExecutionHost behavior, rerun the live Dominium command, mutate Dominium or target repositories, call provider/model/network services, run workers, start runtime/Workbench behavior, preview/apply/rollback, mutate GitHub, release, or promote.

### Plan ID: AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

- Title: Check Registered Process Execution Provider v0
- Status: needs_review
- Objective: independently check the proposed `registered_process_execution_provider_v0` for genericity, process safety, result-axis separation, Dominium parity, and honest non-capability boundaries.
- Scope: check task/evidence, `.aide/reports/registered-process-execution-provider-v0-check/**`, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/task.yaml`.
- Dependencies: `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01` at commit `2137af3a68cc50a06b57fe1fd5ee5bc3af8e0924`, result `PASS_WITH_WARNINGS`, proposed capability `registered_process_execution_provider_v0`.
- Milestones: source build reviewed; independent behavior harness run; genericity and leakage scans completed; Dominium parity reviewed; five material findings recorded; repair prompt generated.
- Blockers: provider acceptance and second-adapter proof are blocked by material provider safety findings.
- Verification Intent: independent harness, focused provider tests, focused Dominium parity tests, backend validation, task inspect/evidence, local-path and secret-like scans, broad validation, Dominium status, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `REQUEST_CHANGES`, `material_finding_count: 5`, and next task exactly `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.
- Notes: this check does not repair implementation, accept the provider, rerun the live Dominium command, mutate Dominium or target repositories, call provider/model/network services, run workers, start runtime/Workbench behavior, preview/apply/rollback, mutate GitHub, release, or promote.

### Plan ID: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

- Title: Build Registered Process Execution Provider v0
- Status: needs_review
- Objective: extract reusable registered-process execution mechanics from the accepted Dominium registered validation command-boundary proof into a domain-neutral provider while preserving Dominium behavior through a thin adapter.
- Scope: neutral execution/protocol modules, Dominium registered-validation adapter refactor, focused provider and Dominium parity tests, `.aide/reports/registered-process-execution-provider-v0/**`, task/evidence, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01` at commit `0754363`, result `ACCEPTED_WITH_WARNINGS`, accepted capability exactly `dominium_registered_validation_command_boundary_invocation_v0`.
- Milestones: generic protocol records added; registered process provider implemented with injected preflight, state probe, output decoder, scrubber, and runner ports; Dominium backend adapted over the provider; focused conformance and parity tests added; task evidence and reports materialized.
- Blockers: none. Warnings: provider is proposed only; full child-process-tree termination, persistent idempotency, resource quotas, streaming artifact storage, and non-Git state providers are not implemented in v0; live Dominium command was not rerun.
- Verification Intent: Python compile, focused generic-provider tests, focused Dominium parity tests, backend report validation, schema/JSON parsing, genericity and leakage scans, task inspect/evidence, broad validation, Dominium clean-state inspection, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, proposed capability `registered_process_execution_provider_v0`, no provider acceptance, and next task exactly `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.
- Notes: this task does not implement a universal execution ontology, arbitrary-command runner, generic command CLI, runtime, worker, provider/model/network behavior, preview/apply/rollback, repository apply behavior, branch/worktree automation, GitHub mutation, release, or promotion.

### Plan ID: AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

- Title: Accept Dominium Registered Validation Backend
- Status: needs_review
- Objective: accept only the checked and relabeled Dominium registered validation command-boundary invocation capability.
- Scope: acceptance task/evidence, `.aide/reports/dominium-registered-validation-backend-accept/**`, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`, `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`, `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01` at commit `78e24e2`, and `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01` at commit `3954459` with `PASS_WITH_WARNINGS`, `missing_evidence: 0`, and `material_finding_count: 0`.
- Milestones: source chain reviewed; accepted capability recorded; warning and non-capability boundaries preserved; task-local accepted capability projection written; next task prompt generated.
- Blockers: none. Warnings: typed refusal is the observed domain outcome; aggregate validation execution and success remain unaccepted; service-adapter entry remains unaccepted; mutation observation is limited to declared probe coverage.
- Verification Intent: JSON parsing, task inspect/evidence, backend validation, broad validation, local-path and secret-like scans, Dominium clean-state inspection, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepted capability exactly `dominium_registered_validation_command_boundary_invocation_v0`, and next task exactly `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.
- Notes: no implementation, refactor, live Dominium rerun, generic provider acceptance, runtime, worker, provider/model/network, preview/apply/rollback, repository mutation, branch/worktree automation, GitHub mutation, release, or promotion is authorized by this acceptance.

### Plan ID: AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01

- Title: Check Dominium Registered Validation Backend Relabel
- Status: needs_review
- Objective: independently verify the bounded relabel task and decide whether precise acceptance may proceed.
- Scope: check task/evidence, `.aide/reports/dominium-registered-validation-backend-relabel-check/**`, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01` at commit `78e24e2`, result `PASS_WITH_WARNINGS`, and `missing_evidence: 0`.
- Milestones: active label scan completed; historical evidence integrity checked; boundary claims reviewed; no-overclaiming review completed; validation completed.
- Blockers: none. Warnings: this check does not accept the capability; historical evidence still contains the superseded label; local Dominium remains behind `origin/main`.
- Verification Intent: evidence-local independent checker, focused tests, backend validation, task inspect/evidence, leakage scans, broad validation, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, `material_finding_count: 0`, and next task exactly `AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.
- Notes: no implementation, report repair, or live Dominium invocation is authorized by this check.

### Plan ID: AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01

- Title: Build Dominium Registered Validation Backend Relabel
- Status: needs_review
- Objective: repair the overbroad active registered-validation capability label and related boundary projections without changing execution behavior.
- Scope: registered-validation backend code, focused CLI/test output, active registered-validation reports, relabel task/evidence, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01/task.yaml`.
- Dependencies: `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01` at `REQUEST_CHANGES`, `missing_evidence: 0`, and material finding `capability_label.overclaims_observed_boundary`.
- Milestones: predecessor evidence inspected; active label changed to `dominium_registered_validation_command_boundary_invocation_v0`; boundary facts separated; active reports regenerated from saved invocation artifacts; task evidence written.
- Blockers: none. Warnings: historical predecessor evidence still contains the superseded label; local Dominium remains behind `origin/main`; service-adapter entry is not accepted.
- Verification Intent: focused compile/tests, backend report validation, task inspect/evidence, active-label scan, local-path/secret scans, broad validation, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, no live Dominium command rerun, preserved historical evidence, and next task exactly `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01`.
- Notes: this task does not accept the capability or build a generic provider.

### Plan ID: AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

- Title: Check Dominium Registered Validation Backend
- Status: needs_review
- Objective: independently verify the registered Dominium validation backend and decide whether the proposed capability label is precise enough for acceptance.
- Scope: check task/evidence, `.aide/reports/dominium-registered-validation-backend-check/**`, queue index, and focused root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01` at commit `1206980e8897ba6031d2d142743d9cac53be1817` with result `PASS_WITH_WARNINGS` and missing evidence zero.
- Milestones: source reports reviewed; Dominium CLI/command/service source inspected; independent harness run; process, typed refusal, state safety, evidence, scrub, and authority-label assertions recorded.
- Blockers: acceptance is blocked by one material authority-label finding.
- Verification Intent: task-local independent harness, task inspect/evidence, Dominium clean-state check, diff checks, broad validation, and commit policy.
- Exit Criteria: stop at `needs_review` with `REQUEST_CHANGES`, `material_finding_count: 1`, proven capability `dominium_registered_validation_command_boundary_readonly_v0`, and next task exactly `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01`.
- Notes: the check does not repair the backend or rerun the live Dominium CLI.

### Plan ID: AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

- Title: Build Dominium Registered Validation Backend
- Status: needs_review
- Objective: prove exactly one bounded local read-only invocation of Dominium's registered `dominium.validation.run` command through the Dominium CLI, command boundary, and `ValidationServiceAdapter`.
- Scope: add a separate AIDE registered validation backend, AIDE Lite command wiring, focused fake-runner tests, task-local evidence, deterministic reports, and queue/root log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` at `ACCEPTED_WITH_WARNINGS`, with accepted capability exactly `fixture_backed_dominium_validation_adapter` and live Dominium command execution still unaccepted.
- Milestones: predecessor state reviewed; backend implemented; tests added; one live Dominium CLI invocation completed; reports and evidence written; validation completed.
- Blockers: none. Warnings: local Dominium checkout is behind `origin/main` and is used as the pinned clean revision rather than refreshed or mutated; Dominium returned a typed refusal for target `all` because aggregate validation suite service is not bound.
- Verification Intent: focused fake-runner unit tests, one live Dominium CLI invocation through the new backend, backend validation, broad AIDE validation, diff checks, and commit policy.
- Exit Criteria: stopped at `needs_review` with completed evidence, proposed capability `live_dominium_validation_command_readonly_v0`, unchanged Dominium state, and next task exactly `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.
- Notes: the proposed capability remains unaccepted until independent check and acceptance.

### Plan ID: AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

- Title: Accept Dominium WorkUnit Validation Slice
- Status: needs_review
- Objective: accept only the checked `fixture_backed_dominium_validation_adapter` capability and route to the next build that can prove live Dominium-owned validation command execution.
- Scope: acceptance task/evidence, `.aide/reports/dominium-workunit-validation-slice-accept/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` and `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` at `PASS_WITH_WARNINGS`, source check commit `630e28f15db4041727f0fba1468e5b98e7c9d147`, source missing evidence zero, source material findings zero, and accepted capability label `fixture_backed_dominium_validation_adapter`.
- Milestones: source chain reviewed; warnings preserved; capability boundary recorded; acceptance reports and evidence materialized; queue index and root logs updated.
- Blockers: none. Warnings: this does not accept live Dominium-owned command execution, general dispatch, Workbench, Service/runtime, workers, providers/models/network, preview/apply/rollback, mutation, GitHub, release, or promotion.
- Verification Intent: task inspect/evidence for build, check, and acceptance; secret/path scan; diff checks; broad AIDE validation; commit policy.
- Exit Criteria: stop at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepted capability exactly `fixture_backed_dominium_validation_adapter`, and next task exactly `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.
- Notes: next serialized task is `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

### Plan ID: AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

- Title: Check Dominium WorkUnit Validation Slice
- Status: needs_review
- Objective: independently verify the WorkUnit validation slice and decide whether it proves fixture-backed adapter execution or live Dominium-owned command execution.
- Scope: check task/evidence, `.aide/reports/dominium-workunit-validation-slice-check/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` at `PASS_WITH_WARNINGS`, source commit `8d8f511c77388b96118eb530f5361090b66911c1`, and source task `missing_evidence: 0`.
- Milestones: baseline checked; independent harness written; executor call counting, unsupported and malformed refusal probes, digest recomputation, determinism, leakage scan, evidence/event reference checks, and authority classification completed.
- Blockers: none. Warning: the achieved capability is `fixture_backed_dominium_validation_adapter`; live Dominium-owned command execution is not proven.
- Verification Intent: independent task-local harness, task inspect/evidence, diff checks, broad AIDE validation, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, zero material findings, preserved warning, and next task exactly `AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
- Notes: acceptance must preserve the fixture-backed capability label.

### Plan ID: AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

- Title: Build Dominium WorkUnit Validation Slice
- Status: needs_review
- Objective: prove the first real post-seam operation shape by routing a Dominium fixture context through ContextDescriptor, ContextPack, WorkUnit, a registered `dominium.validation.run` capability, typed result, EvidencePacket, EventRecord, and read-only projection.
- Scope: bounded Dominium WorkUnit validation adapter, thin CLI commands, temporary fixture workspace, generated validation slice reports, focused tests, queue task evidence, queue index, and execution log.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01` at `ACCEPTED_WITH_WARNINGS` with `missing_evidence: 0` and recommended next task `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
- Milestones: predecessor gate checked; fixture workspace generated; one registered read-only capability invocation implemented; ContextDescriptor, ContextPack, WorkUnit, EvidencePacket, EventRecord, projection, report, validation, and tests materialized; task evidence written.
- Blockers: none. Warnings: the target is a temporary fixture workspace, not a live Dominium checkout; this is not a Workbench, Service, trust/grant, preview/apply, rollback, worker, provider, network, or general Dominium command runner.
- Verification Intent: focused compile and unit tests, live `dominium-workunit-validation status/run/validate`, task inspect/evidence, diff checks, and broad AIDE validation.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, exactly one `dominium.validation.run` invocation, no forbidden boundary crossing, no mutation, complete evidence, and next task exactly `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
- Notes: next serialized task is `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.

### Plan ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01

- Title: Independent Check Of The Dominium Read-Only Seam v0 Repair
- Status: needs_review
- Objective: independently verify the bounded repair for the offline read-only AIDE-Dominium seam v0 without repairing implementation or advancing to acceptance.
- Scope: repair-check task/evidence, `.aide/reports/dominium-readonly-seam-v0-repair-check/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` at `PASS_WITH_WARNINGS`, local repair commit `30931ba1f17b1bc4d9d2b9b12ef18133831ad8fd`, source check `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01` at `REQUEST_CHANGES`, and source-task evidence `missing_evidence: 0`.
- Milestones: baseline verified; independent harness materialized; repaired identity, revision, digest, schema, registry projection, fixture replay, conformance evidence, operation ledger, determinism, immutability, report consistency, warning, and non-capability surfaces checked; reports and evidence materialized.
- Blockers: seam acceptance remains blocked by 10 material repair-check gaps.
- Verification Intent: evidence-local independent repair harness, JSON parsing, task inspect/evidence, focused seam tests where non-mutating, production seam CLI validation as target-under-test where deterministic, Dominium immutability, diff checks, broad validation, secret scan, and commit policy.
- Exit Criteria: stop at `needs_review` with `REQUEST_CHANGES`, do not repair defects, do not modify Dominium or production seam artifacts, and recommend exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.
- Notes: next serialized task is `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.

### Plan ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01

- Title: Repair Offline Read-Only AIDE-Dominium Seam v0
- Status: needs_review
- Objective: repair the 18 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01` while preserving the offline, deterministic, read-only seam boundary.
- Scope: Dominium seam schema, `core/interop/dominium/**`, focused tests, fixtures, `.aide/interop/dominium/**`, `.aide/reports/dominium-readonly-seam-v0/**`, repair reports, repair task/evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01` at `REQUEST_CHANGES`, check commit `692b4b3469e80a67f3f2f98612ec66c86b7394e9`, 18 material findings, missing evidence zero, and recommended next task `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.
- Milestones: exact repository identity implemented; digest finalization repaired; registry truncation disclosure added; public schema tightened; negative fixtures made replayable; conformance checks made expectation-specific; demo timing made truthful with operation ledger; semantic validator hardened for revisions, cardinality, references, owners, capabilities, diagnostics, refusals, events, and required fields; tests and live demo passed; reports/evidence materialized.
- Blockers: none. Warnings: seam remains offline/read-only; SeamBundle remains projection evidence only; local Dominium remains behind `origin/main` by 24 commits; runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, workers, preview/apply/rollback, and mutation remain absent.
- Verification Intent: Python compile, original seam tests, repair regression tests, live seam demo, live seam validation, JSON parsing, diff checks, broad validation, task inspect/evidence, Dominium immutability, secret scan, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, no forbidden operation, no Dominium modification, complete repair reports/evidence, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.

### Plan ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01

- Title: Full Independent Adversarial Check Of The Offline AIDE-Dominium Seam
- Status: needs_review
- Objective: independently check the offline read-only AIDE-Dominium seam v0 build without repairing it or modifying production seam artifacts.
- Scope: check task/evidence, `.aide/reports/dominium-readonly-seam-v0-check/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01` at `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01` at `PASS_WITH_WARNINGS`, build commit `a75635478be155ef7bc2b62de4ead3837212bbb8`, and source-task evidence `missing_evidence: 0`.
- Milestones: baseline verified; independent harness materialized; selected inputs, digests, records, references, capabilities, registries, fixtures, conformance, demo evidence, CLI boundaries, and Dominium immutability checked; reports and evidence materialized.
- Blockers: none for the check. Material findings block seam acceptance and require bounded repair.
- Verification Intent: independent harness, existing focused seam tests, task inspect/evidence, JSON parsing, diff checks, broad validation, Dominium immutability check, secret scan, and commit policy.
- Exit Criteria: stop at `needs_review` with `REQUEST_CHANGES`, do not repair defects, do not modify Dominium or production seam artifacts, and recommend exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.
- Notes: next serialized task is `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.

### Plan ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01

- Title: Full Offline Read-Only AIDE-Dominium Seam v0
- Status: needs_review
- Objective: build the complete offline, deterministic, read-only AIDE-Dominium seam v0 authorized by the accepted planning charter.
- Scope: public seam schema, cohesive `core/interop/dominium/` implementation, thin `dominium-seam` CLI dispatch, positive and adversarial fixtures, `.aide/interop/dominium/**`, `.aide/reports/dominium-readonly-seam-v0/**`, task evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01` at `ACCEPTED_WITH_WARNINGS`, missing evidence zero, commit `c2298b743e275f14a987da29db1ca78927c154fb`, and read-only local Dominium input at pinned revision `c92b386027890c1bbf14aef6eaafe0357b7b03dd`.
- Milestones: schema and models implemented; read-only snapshot reader implemented; mappings and SeamBundle projection implemented; CLI status/snapshot/project/validate/diff/demo implemented; positive and adversarial fixtures generated; 108 focused tests passed; offline demo passed with source mutation count zero; reports and evidence materialized.
- Blockers: none. Warnings: seam is offline/read-only; SeamBundle is projection evidence only; local Dominium remains behind `origin/main`; runtime, Workbench, bridge runtime, service, provider/model/network calls, workers, preview/apply/rollback, and mutation remain absent.
- Verification Intent: Python compile, focused seam tests, CLI status/snapshot/project/validate/diff/demo, unsupported-operation refusal probe, deterministic projection comparison, source digest recomputation, Dominium immutability check, JSON parsing, secret scan, diff checks, broad validation, task inspect/evidence, and commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, complete offline vertical slice, no forbidden operation, no Dominium modification, complete reports/evidence, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`.

### Plan ID: AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01

- Title: Accept Planning-Only AIDE-Dominium Integration Charter
- Status: needs_review
- Objective: accept the planning-only AIDE-Dominium integration charter after consolidating the charter build, independent remote freshness and semantic check, source-chain evidence, and warning disposition.
- Scope: acceptance task/evidence, `.aide/reports/dominium-integration-charter-accept/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01/task.yaml`.
- Dependencies: A2A AgentCard acceptance, `AIDE-DOMINIUM-INTEGRATION-CHARTER-01` at `PASS_WITH_WARNINGS`, `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01` at `PASS_WITH_WARNINGS`, missing evidence zero, zero material findings, charter commit `5b80e4c4c3c400e2a3ccf8d2c42cfb44c3d6aa28`, check commit `2af8bb2108eb5fdf281105c98429ac4491372ed1`, and remote Dominium `main` freshness.
- Milestones: source chain verified; remote Dominium freshness confirmed; accepted scope, warnings, and non-capabilities recorded; source hierarchy, ownership, namespace, mapping, transaction, Workbench, compatibility, security, recovery, seam, validation-slice, DAG, and turn-size policy accepted; evidence and reports materialized; validation run.
- Blockers: none. Warnings: charter is planning-only; local Dominium remains behind remote by 24 commits; read-only seam, Host Contract, Bridge, Workbench, runtime, service, preview/apply/rollback, workers, providers, and network behavior remain absent.
- Verification Intent: parse acceptance JSON, inspect source tasks/evidence, confirm remote Dominium HEAD read-only, run source-chain consistency, ownership, namespace, object-mapping, DAG, dependency, mutation-prerequisite, downstream-task absence, Dominium immutability, secret, broad validation, diff, and commit-policy checks.
- Exit Criteria: stop at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepted planning artifact `aide_dominium_integration_charter_v0`, no implementation, no Dominium writes, no downstream task materialization, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`.

### Plan ID: AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01

- Title: Independent Cross-Repository Check Of The AIDE-Dominium Integration Charter
- Status: needs_review
- Objective: independently check the planning-only AIDE-Dominium integration charter, with adversarial focus on the stale pinned Dominium snapshot versus current remote `main`.
- Scope: check task/evidence, `.aide/reports/dominium-integration-charter-check/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01/task.yaml`.
- Dependencies: `AIDE-DOMINIUM-INTEGRATION-CHARTER-01` at `PASS_WITH_WARNINGS`, missing evidence zero, commit `5b80e4c4c3c400e2a3ccf8d2c42cfb44c3d6aa28`, and current read-only Dominium remote inspection.
- Milestones: source chain verified; remote Dominium `main` checked; canonical inputs hashed; stale snapshot classified; ownership, namespace, mappings, Workbench authority, transaction layering, compatibility, security, recovery, seam, validation slice, DAG, parallel lane, turn policy, and reports reviewed; evidence and next acceptance prompt materialized; validation run.
- Blockers: none. Warnings: local Dominium checkout remains behind remote by 24 commits, remote public docs changed, and the charter remains planning-only.
- Verification Intent: parse check JSON, inspect source and check tasks/evidence, compare Dominium remote HEAD and immutable object content, run graph/mapping scans, verify no forbidden changes, run broad AIDE validation, run diff checks, and run commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, no repair, no Dominium writes, no downstream implementation materialization, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`.

### Plan ID: AIDE-DOMINIUM-INTEGRATION-CHARTER-01

- Title: Planning-Only AIDE-Dominium Integration Ownership Charter
- Status: needs_review
- Objective: freeze semantic ownership, source-of-truth hierarchy, namespace ownership, object mappings, command/refusal/diagnostic/evidence/event mappings, transaction composition, host/bridge/provider/experience boundaries, Workbench non-authority law, compatibility, security, recovery, first read-only seam, first validation slice, critical-path DAG, and read-only RepoGraph lane.
- Scope: charter task/evidence, `.aide/reports/dominium-integration-charter/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-DOMINIUM-INTEGRATION-CHARTER-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01` at `ACCEPTED_WITH_WARNINGS`, missing evidence zero, commit `7e80ea2f18b404af68a752502a7491fceaa7abea`, and recommended next task `AIDE-DOMINIUM-INTEGRATION-CHARTER-01`; live local Dominium checkout at `C:/Projects/Dominium/dominium`.
- Milestones: AIDE and Dominium baselines pinned; input hashes recorded; ownership matrix written; source hierarchy and namespace policy written; object, command, refusal, diagnostic, evidence, event, transaction, security, compatibility, and recovery mappings written; read-only seam and validation slice specified; task graph and parallel lane written; evidence and next check prompt materialized; validation run.
- Blockers: none. Warning: local Dominium `main` is clean but behind `origin/main` by 24 commits; no fetch was performed because remote-ref mutation is out of scope.
- Verification Intent: parse JSON reports, parse Dominium TOML input, run graph uniqueness/dependency/cycle checks, run ownership and non-authority checks, run secret-like scan, verify no cross-repo changes, inspect task evidence, run broad AIDE validation, run diff checks, and run commit policy.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, no downstream queue materialization, no Dominium writes, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`.

### Plan ID: AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01

- Title: Accept Repaired Contract-Only A2A Agent Card Projection
- Status: needs_review
- Objective: accept only the repaired `minimal_a2a_agent_card_contract` projection after reviewing the MCP acceptance, A2A build, failed independent check, bounded repair, and independent repair-check chain.
- Scope: acceptance task/evidence, `.aide/reports/a2a-agent-card-contract-accept/**`, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01/task.yaml`.
- Dependencies: MCP acceptance at `ACCEPTED_WITH_WARNINGS`; A2A build at `PASS_WITH_WARNINGS`; failed A2A check preserved with eight material findings; A2A repair at `PASS_WITH_WARNINGS`; independent repair check at `PASS_WITH_WARNINGS` with zero remaining material findings.
- Milestones: source chain reviewed; historical failure preserved; repaired official AgentCard accepted; candidate skill and runtime boundaries accepted; reports and evidence materialized; validation run.
- Blockers: none. Remaining warnings are no full vendored official A2A schema validation, no live A2A runtime, and advisory future `aide://interop` ReferenceID debt.
- Verification Intent: parse acceptance JSON, inspect task/evidence, run focused A2A tests and validators, run predecessor validators, run broad AIDE validation, run independent JSON/field checks, unsupported-operation probes, secret scan, diff checks, and commit policy.
- Exit Criteria: stop at `needs_review` with `ACCEPTED_WITH_WARNINGS`, no material remaining findings, explicit non-capabilities, complete evidence, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-DOMINIUM-INTEGRATION-CHARTER-01`.

### Plan ID: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01

- Title: Independent Check of A2A Agent Card Standards Repair
- Status: needs_review
- Objective: independently verify that `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` closes the eight material A2A AgentCard standards-alignment findings without expanding A2A capability.
- Scope: repair-check task/evidence, repair-check reports, queue index, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01/task.yaml`.
- Dependencies: A2A build, failed A2A check, and bounded A2A repair at `PASS_WITH_WARNINGS`.
- Milestones: source-chain review complete; independent AgentCard scan complete; validator and CLI boundary review complete; evidence and reports complete.
- Blockers: none.
- Verification Intent: focused A2A tests, A2A status/project/validate, predecessor validators, broad AIDE validate, independent JSON scan, immutability review, unsupported-command probes, and secret scan.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS`, no material remaining findings, and exactly one next task recommendation.
- Notes: next serialized task is `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.

### Plan ID: AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01

- Title: Repair A2A 1.0 AgentCard Standards Alignment and Metadata Separation
- Status: needs_review
- Objective: repair the eight material A2A standards-alignment defects found by `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01` without adding live A2A behavior.
- Scope: A2A helper/schema/tests, regenerated `.aide/interop/a2a/**`, regenerated `.aide/reports/a2a-agent-card-contract/**`, repair task/evidence, repair reports, queue index, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01/task.yaml`.
- Dependencies: accepted MCP server contract, A2A build at `PASS_WITH_WARNINGS`, failed A2A check at `FAILED_VALIDATION` with eight material findings, and no later repair.
- Milestones: source chain verified; official AgentCard cleaned; supported interface fixture added; provider/legacy/capability/skill defects repaired; validator and tests hardened; reports and evidence materialized.
- Blockers: none for this bounded repair. Acceptance remains blocked until independent repair check passes.
- Verification Intent: run diff checks, Python compile, focused A2A tests, A2A status/project/validate, predecessor validators, task inspect/evidence, broad AIDE validation, independent JSON/probe checks, unsupported command probes, secret scan, and commit-policy validation.
- Exit Criteria: stop at `needs_review` with `PASS_WITH_WARNINGS` and recommend `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01` only.
- Notes: This repair preserves failed-check evidence and does not implement endpoint, publication, registration, authentication, authorization, task delegation, worker execution, provider/model/network calls, runtime, host integration, PatchTransaction apply, or target mutation.

### Plan ID: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01

- Title: Independent Standards and Boundary Check of A2A Agent Card Contract
- Status: needs_review
- Objective: independently check `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01` against A2A 1.0 AgentCard standards alignment and no-runtime boundaries.
- Scope: check task/evidence, `.aide/reports/a2a-agent-card-contract-check/**`, queue index, and plan/execution log updates only.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01` accepted with warnings and `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01` complete at `needs_review` with `missing_evidence: 0`.
- Milestones: source-chain review complete; independent AgentCard standards review complete; reports and evidence materialized.
- Blockers: eight material standards-alignment findings block acceptance.
- Verification Intent: focused tests, A2A CLI status/project/validate, predecessor validators, task evidence checks, broad AIDE validate, JSON parsing, unsupported-operation probes, secret scan, and commit policy.
- Exit Criteria: stop at `needs_review` and recommend `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01`.
- Notes: check-only; no A2A implementation, artifact, schema, helper, or test repair was performed.

### Plan ID: AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01

- Title: Build Minimal Contract-Only A2A Agent Card Projection
- Status: needs_review
- Objective: build `minimal_a2a_agent_card_contract` as a deterministic contract-only A2A agent-card projection after MCP contract acceptance.
- Scope: A2A schema, helper, thin AIDE Lite dispatch, focused tests, `.aide/interop/a2a/**`, `.aide/reports/a2a-agent-card-contract/**`, queue task/evidence, queue index, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01` at `ACCEPTED_WITH_WARNINGS` with `missing_evidence: 0` and recommended next task `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`.
- Milestones: source chain verified; A2A schema/helper/CLI/tests added; static inactive agent-card projection generated; skill, capability, refusal, security, conformance, artifact, validation, future-work, and non-capability reports written; evidence complete.
- Blockers: none. Remaining warnings are no-live-endpoint, no-registration, no-authentication, no-delegation, no-runtime, no-full-external-A2A-schema-validation, and advisory future `aide://interop` ReferenceID debt.
- Verification Intent: run Git diff checks, Python compile, focused A2A tests, A2A status/project/validate, predecessor validators, task inspect/evidence checks, broad validation, JSON parsing, deterministic projection, source immutability, unsupported-command probes, secret scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, accepts no capability by itself, preserves no-runtime and no-authority boundaries, performs no forbidden operation, and recommends `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`.
- Notes: This build does not implement or authorize a live A2A endpoint, authentication, delegation, worker execution, Host Contract, Dominium Bridge, Workbench, Runtime, Service, provider/model/network calls, PatchTransaction apply, GitHub mutation, release, promotion, or target mutation.

### Plan ID: AIDE-ACCEPT-MCP-SERVER-CONTRACT-01

- Title: Accept Minimal Contract-Only MCP Projection
- Status: needs_review
- Objective: accept the repaired `minimal_mcp_server_contract` capability as a deterministic contract-only MCP projection after the build, failed-check, repair, and repair-check chain.
- Scope: acceptance task packet, task-local evidence, `.aide/reports/mcp-server-contract-accept/**`, queue index entry, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-MCP-SERVER-CONTRACT-01/task.yaml`.
- Dependencies: `AIDE-BUILD-MCP-SERVER-CONTRACT-01` at `PASS_WITH_WARNINGS`, `AIDE-CHECK-MCP-SERVER-CONTRACT-01` preserved at `FAILED_VALIDATION`, `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01` at `PASS_WITH_WARNINGS`, `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01` at `PASS_WITH_WARNINGS` with zero material findings, and complete evidence for all four source tasks.
- Milestones: source chain verified; historical failure preserved; schema/helper and JSON-RPC fixture readiness consolidated; pagination and resource-not-found repairs accepted; catalogues, refusals, transport expectations, authorization expectations, conformance expectations, runtime facts, determinism, immutability, warnings, and non-capabilities reviewed; reports and evidence written.
- Blockers: none. Remaining warnings are no-runtime, no-full-official-schema-validation, and advisory future `aide://interop` ReferenceID debt.
- Verification Intent: run Git diff checks, Python compile, focused MCP tests, MCP status/validate, predecessor validators, task inspect/evidence checks, broad validation, JSON parsing, independent fixture scans, validator regression evidence review, unsupported-operation probes, secret scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepts only the contract-only projection capability, preserves failed-check evidence, performs no forbidden operation, and recommends `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`.
- Notes: This acceptance does not implement or authorize live MCP server behavior.

### Plan ID: AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01

- Title: Check MCP Pagination and Resource-Error Repair
- Status: needs_review
- Objective: independently recheck `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01` and determine whether the MCP contract slice is ready for acceptance review.
- Scope: repair-check task packet, task-local evidence, `.aide/reports/mcp-server-contract-repair-check/**`, queue index entry, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01/task.yaml`.
- Dependencies: original MCP build at `PASS_WITH_WARNINGS`, original MCP check at `FAILED_VALIDATION`, MCP repair at `PASS_WITH_WARNINGS`, complete evidence for all source tasks, and repair commit `4907fab451400ed745a84493ae6894cc00f177ad`.
- Milestones: source chain verified; failed check preserved; pagination and cursor-type repairs independently rechecked; resource-not-found and custom refusals rechecked; temporary regression injection performed; JSON-RPC regression reviewed; focused tests and validators run; warnings classified; reports and evidence written.
- Blockers: none. Remaining warnings are no-runtime/no-full-schema boundaries.
- Verification Intent: run Git diff checks, Python compile, focused MCP tests, MCP status/project/validate, predecessor validators, task inspect/evidence checks, broad validation, independent JSON fixture scans, temporary invalid-fixture validator probes, unsupported-operation probes, fixture/report hash checks, immutability checks, secret scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, zero material findings, complete evidence, no forbidden operation, and recommended next task `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.
- Notes: This check does not accept MCP and does not alter MCP helper/schema/tests/fixtures/build or repair reports.

### Plan ID: AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01

- Title: Repair MCP Pagination Fixtures and Resource-Not-Found Mapping
- Status: needs_review
- Objective: repair only the two material standards-alignment defects found by `AIDE-CHECK-MCP-SERVER-CONTRACT-01`.
- Scope: MCP contract fixture generation and validation, focused MCP tests, affected MCP generated fixtures/reports, repair queue packet/evidence, queue index, and focused execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-BUILD-MCP-SERVER-CONTRACT-01` at `PASS_WITH_WARNINGS`, `AIDE-CHECK-MCP-SERVER-CONTRACT-01` at `FAILED_VALIDATION`, complete evidence for both source tasks, build commit `c8a143f76af585ae3a0cc3004fb5278c57f264e0`, and failed-check commit `18839ccf9b1ec2b129064b09bfb2c90988e31e63`.
- Milestones: source chain verified; pagination fixtures repaired; resource-not-found code repaired; fixture validator hardened; focused regressions added; affected projection regenerated; evidence and reports written.
- Blockers: none for this bounded repair. Acceptance remains blocked until an independent repair check passes.
- Verification Intent: run diff checks, Python compile, focused MCP tests, MCP status/project/validate, predecessor validators, JSON parsing, independent fixture probes, repeated projection comparison, source immutability checks, task inspect/evidence, broad validation, unsupported-command probes, secret scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, both material defects are repaired, no failed-check evidence is rewritten, no runtime or forbidden operation occurs, and recommended next task is `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`.
- Notes: This repair does not accept the MCP contract and does not broaden MCP beyond the existing contract-only projection slice.

### Plan ID: AIDE-CHECK-MCP-SERVER-CONTRACT-01

- Title: Check Minimal Contract-Only MCP Projection
- Status: needs_review
- Objective: independently check `AIDE-BUILD-MCP-SERVER-CONTRACT-01` against the pinned MCP `2025-11-25` and JSON-RPC `2.0` subset while preserving no-runtime and no-authority boundaries.
- Scope: check task packet, task-local evidence, `.aide/reports/mcp-server-contract-check/**`, queue index entry, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-MCP-SERVER-CONTRACT-01/task.yaml`.
- Dependencies: `AIDE-BUILD-MCP-SERVER-CONTRACT-01` at `needs_review` with `PASS_WITH_WARNINGS`, build commit `c8a143f76af585ae3a0cc3004fb5278c57f264e0`, complete evidence, and accepted static interop exports.
- Milestones: source chain verified; MCP JSON parsed; JSON-RPC, lifecycle, version, capability, resource, tool, prompt, refusal, transport, authorization, security, authority, conformance, determinism, and CLI boundaries reviewed; findings classified; reports and evidence written.
- Blockers: two material fixture defects block acceptance: null `cursor` or `nextCursor` fields in list fixtures, and resource-not-found error code `-32043` instead of pinned `-32002`.
- Verification Intent: run diff checks, Python compile, focused MCP tests, MCP status/project/validate, predecessor validators, JSON parsing, direct fixture probes, unsupported-command probes, repeated projection comparison, source immutability check, task inspect/evidence, broad validation, secret scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `FAILED_VALIDATION`, preserves build evidence, performs no repair or forbidden operation, and recommends `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`.
- Notes: Acceptance is not recommended until a bounded repair and independent repair check pass.

### Plan ID: AIDE-ACCEPT-INTEROP-EXPORTS-01

- Title: Accept Static Interop Export Previews
- Status: needs_review
- Objective: accept `static_interop_export_previews` after successful build and independent check, while preserving preview-only and no-live-runtime boundaries.
- Scope: acceptance task packet, task-local evidence, `.aide/reports/interop-exports-accept/**`, queue index entry, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-INTEROP-EXPORTS-01/task.yaml`.
- Dependencies: `AIDE-BUILD-INTEROP-EXPORTS-01` and `AIDE-CHECK-INTEROP-EXPORTS-01` at `needs_review` with `PASS_WITH_WARNINGS`, complete evidence, and zero material findings.
- Milestones: source chain verified; artifact inventory and hashes accepted; format checks reviewed; queue/projection authority boundaries confirmed; agent/MCP/A2A preview boundaries confirmed; no-install/no-runtime warnings classified; reports and evidence written; validation run; next MCP contract prompt generated.
- Blockers: none for static-preview acceptance. Live instruction installation, MCP/A2A servers, Host Contract, Dominium Bridge, Workbench, runtime, worker execution, provider/model/network calls, PatchTransaction apply, branch/worktree automation, release, promotion, and target mutation remain deferred.
- Verification Intent: run Git status and diff checks, JSON parsing, hash verification, manifest containment and duplicate checks, bounded Aider YAML review, wording scans, immutability checks, task inspect/evidence for build/check/acceptance, broad AIDE validation, secret-like scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepted scope is limited to static previews, evidence is complete, no forbidden operation occurred, and recommended next task is `AIDE-BUILD-MCP-SERVER-CONTRACT-01`.
- Notes: Acceptance does not install or activate any preview artifact.

### Plan ID: AIDE-CHECK-INTEROP-EXPORTS-01

- Title: Check Static Interop Export Previews
- Status: needs_review
- Objective: independently check `AIDE-BUILD-INTEROP-EXPORTS-01` for complete evidence, static artifact integrity, JSON/report consistency, queue authority preservation, and explicit non-capability boundaries.
- Scope: check task packet, task-local evidence, `.aide/reports/interop-exports-check/**`, queue index entry, and focused plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-INTEROP-EXPORTS-01/task.yaml`.
- Dependencies: `AIDE-BUILD-INTEROP-EXPORTS-01` at `needs_review` with `PASS_WITH_WARNINGS` and `missing_evidence: 0`.
- Milestones: source chain reviewed; artifact hashes independently recomputed; JSON artifacts parsed; boundary scan completed; build artifacts confirmed unchanged; reports and evidence written; validation run; next acceptance prompt generated.
- Blockers: none for this check. Live MCP/A2A, Host Contract, Dominium Bridge conformance, Workbench, Commander, Service, runtime, worker execution, provider/model/network calls, PatchTransaction apply, branch/worktree automation, release, promotion, and target mutation remain deferred.
- Verification Intent: run Git status and diff checks, task inspect/evidence for build and check tasks, JSON parsing, hash verification, manifest/report consistency checks, boundary scans, broad AIDE validation, secret-like scan, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, no material findings, complete evidence, no forbidden operation, and recommended next task `AIDE-ACCEPT-INTEROP-EXPORTS-01`.
- Notes: The check does not accept the interop exports and does not alter the build artifacts.

### Plan ID: AIDE-BUILD-INTEROP-EXPORTS-01

- Title: Build Static Interop Export Previews
- Status: needs_review
- Objective: create static, deterministic, report-only interop preview exports after accepted ContextPack v2 without implementing live service, runtime, worker, provider, host, or mutation behavior.
- Scope: task packet, task-local evidence, `.aide/interop/exports/**`, `.aide/reports/interop-exports/**`, queue index entry, and focused root planning/documentation updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-INTEROP-EXPORTS-01/task.yaml`.
- Dependencies: `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01` and `AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01` at `needs_review` with non-blocking warning results.
- Milestones: live queue reviewed; static preview artifacts written; artifact hashes recorded; non-capabilities preserved; reports and evidence written; validation run; next independent-check prompt generated.
- Blockers: none for the static build. Live MCP/A2A, Host Contract, Dominium Bridge conformance, Workbench, Commander, Service, runtime, worker execution, provider/model/network calls, PatchTransaction apply, branch/worktree automation, release, promotion, and target mutation remain deferred.
- Verification Intent: run Git status and diff checks, JSON parsing for preview/report JSON, preview hash verification, task inspect/evidence, broad AIDE validation, secret-like scan over changed files, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, static previews and reports exist, evidence is complete, no implementation or forbidden operation occurred, and the recommended next task is `AIDE-CHECK-INTEROP-EXPORTS-01`.
- Notes: The previews are not installed into external tool locations and do not become accepted interop capability until independent check and acceptance.

### Plan ID: AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01

- Title: Intent-To-Transaction Roadmap Incorporation
- Status: needs_review
- Objective: incorporate the 2026-06-19 through 2026-06-20 architecture synthesis into AIDE's planning surfaces without interrupting live queue routing or starting Host Contract, Dominium Bridge, Workbench, runtime, provider, worker, or mutation implementation.
- Scope: planning task packet, task-local evidence, `.aide/reports/intent-to-transaction-roadmap/**`, queue index entry, and focused updates to root roadmap/documentation/planning logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01/task.yaml`.
- Dependencies: live queue state at `24e6caeeca0802baf4582166ab298f61871e0b60`; `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01` at `needs_review` with `ACCEPTED_WITH_WARNINGS`.
- Milestones: live queue reviewed; source synthesis classified; `AIDE-BUILD-INTEROP-EXPORTS-01` preserved as current serialized next task; future Host/Capability/Transaction/Artifact-Event-Evidence contract families recorded; Dominium seam and Workbench ramp recorded; reports and evidence written; validation run.
- Blockers: none for the planning update. Host Contract, CapabilityInvocation, DevelopmentTransaction, PreviewSession, Dominium Bridge conformance, Workbench, Commander, Service, runtime, worker execution, provider/model/network calls, branch/worktree automation, PatchTransaction apply, target mutation, release, and promotion remain deferred.
- Verification Intent: run Git status and diff checks, task inspect/evidence for this planning task, JSON parsing for the roadmap report, broad AIDE validation, secret-like scan over changed files, and commit-policy validation.
- Exit Criteria: task stops at `needs_review` with `PASS_WITH_WARNINGS`, planning reports exist, explicit non-capabilities are preserved, no implementation or forbidden operation occurred, and the recommended next task remains `AIDE-BUILD-INTEROP-EXPORTS-01`.
- Notes: Future candidate tasks are route records only until materialized and processed through their own queue evidence gates.

### Plan ID: AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01

- Title: Resume Acceptance of Minimal ContextPack v2 Schema
- Status: needs_review
- Objective: accept the minimal `context_pack_v2` projection capability after resume build and independent check while preserving original blocked ContextPack records.
- Scope: acceptance task packet, task-local evidence, `.aide/reports/context-pack-v2-resume-accept/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01/task.yaml`.
- Dependencies: `AIDE-RESUME-BUILD-CONTEXTPACK-V2-01` and `AIDE-RESUME-CHECK-CONTEXTPACK-V2-01` at `needs_review` with `PASS_WITH_WARNINGS`.
- Milestones: source chain reviewed; accepted scope narrowed; no-execution/no-admission/no-trust boundary preserved; reports and evidence written; validation run; next Interop Exports prompt generated.
- Blockers: none for this acceptance. Full JSON Schema Draft validation, resolver/event-store behavior, model/provider/network calls, embeddings, runtime consumption, adapter admission, trust, patch apply, and target mutation remain deferred.
- Verification Intent: run task inspect/evidence for build/check/acceptance, ContextPack status, focused test review, acceptance JSON parsing, broad AIDE validation, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `ACCEPTED_WITH_WARNINGS`, complete evidence, no implementation or forbidden operation, accepted scope stated narrowly, original blocked records preserved, and exactly one next task: `AIDE-BUILD-INTEROP-EXPORTS-01`.
- Notes: Acceptance does not edit CapabilityManifest records and does not create a runtime context service.

### Plan ID: AIDE-RESUME-CHECK-CONTEXTPACK-V2-01

- Title: Resume Check of Minimal ContextPack v2 Schema
- Status: needs_review
- Objective: independently check the resume ContextPack v2 build while preserving the original blocked ContextPack check record.
- Scope: check task packet, task-local evidence, `.aide/reports/context-pack-v2-resume-check/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-CHECK-CONTEXTPACK-V2-01/task.yaml`.
- Dependencies: `AIDE-RESUME-BUILD-CONTEXTPACK-V2-01` at `needs_review` with result `PASS_WITH_WARNINGS`; original `AIDE-CHECK-CONTEXTPACK-V2-01` preserved as `BLOCKED`.
- Milestones: source chain reviewed; source hashes independently recomputed; deterministic projection checked in a temp workspace; unsupported CLI operations probed; reports and evidence written; validation run.
- Blockers: none for this check. ContextPack acceptance, full JSON Schema Draft validation, model/provider/network calls, embeddings, resolver/event-store behavior, runtime consumption, adapter admission, trust, patch apply, and target mutation remain deferred.
- Verification Intent: run Python compilation, focused ContextPack v2 tests, live ContextPack status, unsupported-command probes, task inspect/evidence, broad AIDE validation, JSON parsing, source hash recomputation, deterministic projection and source immutability checks, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, complete evidence, no implementation or forbidden operation, no material findings, original blocked check preserved, and exactly one next task: `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01`.
- Notes: This check does not accept ContextPack v2 and does not regenerate build reports to hide drift.

### Plan ID: AIDE-RESUME-BUILD-CONTEXTPACK-V2-01

- Title: Resume Build of Minimal ContextPack v2 Schema
- Status: needs_review
- Objective: build the minimal deterministic `context_pack_v2` slice after repaired PatchTransaction and AdapterManifest resume acceptance while preserving the original blocked ContextPack records.
- Scope: ContextPack v2 schema, helper, AIDE Lite dispatch, focused tests, deterministic reports, resume task packet/evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-BUILD-CONTEXTPACK-V2-01/task.yaml`.
- Dependencies: `AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01` at `needs_review` with result `ACCEPTED_WITH_WARNINGS`; original ContextPack build/check records preserved as blocked historical evidence.
- Milestones: source chain reviewed; schema/helper added; CLI dispatch added; focused tests added; reports projected; evidence written; validation run; next resume-check prompt generated.
- Blockers: none for this narrow build. Model/provider/Gateway/network calls, embeddings, agent/worker/command execution, adapter admission, trust, patch apply, target mutation, runtime, Service, Commander, Workbench, Test Broker, full JSON Schema Draft compliance, and acceptance remain deferred.
- Verification Intent: run Python compilation, focused ContextPack v2 tests, ContextPack v2 status/project/validate, predecessor protocol validators, task inspect/evidence, broad AIDE validation, JSON parsing, deterministic projection review, source immutability review, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, projection-only ContextPack v2 slice built, complete evidence, no execution/model/network/admission/trust/apply/mutation behavior, original blocked records preserved, and exactly one next task: `AIDE-RESUME-CHECK-CONTEXTPACK-V2-01`.
- Notes: This build task does not accept ContextPack v2. Acceptance requires independent check and later resume acceptance.

### Plan ID: AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01

- Title: Resume Acceptance of Minimal AdapterManifest Schema
- Status: needs_review
- Objective: accept `minimal_adapter_manifest_schema` after resume build and independent check while preserving the original blocked acceptance record.
- Scope: acceptance task packet, task-local evidence, `.aide/reports/adapter-manifest-resume-accept/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01` and `AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01` at `needs_review` with `PASS_WITH_WARNINGS`; original `AIDE-ACCEPT-ADAPTER-MANIFEST-01` preserved as `BLOCKED`.
- Milestones: source chain reviewed; accepted scope narrowed; no-admission/no-trust/no-execution boundary preserved; reports and evidence written; validation run; next ContextPack v2 resume build prompt generated.
- Blockers: none for this acceptance. Adapter admission, trust, execution, credentials, network/provider calls, runtime, target mutation, ContextPack v2, and full JSON Schema Draft validation remain deferred.
- Verification Intent: run focused AdapterManifest tests, AdapterManifest status/validate, build/check/accept task inspect/evidence, broad AIDE validation, JSON parsing, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `ACCEPTED_WITH_WARNINGS`, complete evidence, no implementation or forbidden operation, original blocked acceptance preserved, and exactly one next task: `AIDE-RESUME-BUILD-CONTEXTPACK-V2-01`.
- Notes: This acceptance does not edit CapabilityManifest records and does not admit or trust any adapter.

### Plan ID: AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01

- Title: Resume Check of Minimal AdapterManifest Schema
- Status: needs_review
- Objective: independently check the resume AdapterManifest build while preserving the original blocked AdapterManifest check record.
- Scope: check task packet, task-local evidence, `.aide/reports/adapter-manifest-resume-check/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01` at `needs_review` with result `PASS_WITH_WARNINGS`; original `AIDE-CHECK-ADAPTER-MANIFEST-01` preserved as `BLOCKED`.
- Milestones: source chain reviewed; independent reference and authority-boundary probes run; deterministic projection checked; CLI unsupported operations probed; reports and evidence written; validation run.
- Blockers: none for this check. Adapter acceptance, admission, trust, execution, credentials, network/provider calls, runtime, target mutation, and full JSON Schema Draft validation remain deferred.
- Verification Intent: run Python compilation, focused AdapterManifest tests, AdapterManifest status/project/validate, task inspect/evidence for build and check, broad AIDE validation, JSON parsing, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, complete evidence, no implementation or forbidden operation, no material findings, and exactly one next task: `AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01`.
- Notes: This check does not accept AdapterManifest and does not rewrite the original blocked check.

### Plan ID: AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01

- Title: Resume Build of Minimal AdapterManifest Schema
- Status: needs_review
- Objective: build the minimal declaration-only `minimal_adapter_manifest_schema` slice after repaired PatchTransaction acceptance while preserving the original blocked AdapterManifest records.
- Scope: AdapterManifest schema, helper, AIDE Lite dispatch, focused tests, deterministic reports, resume task packet/evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `ACCEPTED_WITH_WARNINGS`; original AdapterManifest build/check/accept records preserved as blocked historical evidence.
- Milestones: source chain reviewed; schema/helper added; CLI dispatch added; focused tests added; reports projected; evidence written; validation run; next resume-check prompt generated.
- Blockers: none for this narrow build. Adapter admission, trust, execution, sandbox creation, credentials, network/provider calls, GitHub mutation, patch apply, target mutation, runtime, Service, Commander, Workbench, Test Broker, ContextPack v2, full JSON Schema Draft compliance, and acceptance remain deferred.
- Verification Intent: run Python compilation, focused AdapterManifest tests, AdapterManifest status/project/validate, predecessor protocol validators, task inspect/evidence, broad AIDE validation, JSON parsing, deterministic projection review, source immutability review, secret-like scan, Git diff checks, and commit-policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, declaration-only AdapterManifest slice built, complete evidence, no admission/trust/execution/mutation behavior, original blocked records preserved, and exactly one next task: `AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01`.
- Notes: This build task does not accept AdapterManifest. Acceptance requires independent check and later resume acceptance.

### Plan ID: AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01

- Title: Resume Acceptance of Repaired Minimal PatchTransaction Schema
- Status: needs_review
- Objective: accept the repaired `minimal_patch_transaction_schema` capability after the failed check, bounded repair, and independent repair check while preserving the original blocked acceptance record.
- Scope: resume acceptance task packet, task-local evidence, `.aide/reports/patch-transaction-resume-accept/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01` at `needs_review` with result `PASS_WITH_WARNINGS` and complete evidence; original `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` preserved as `BLOCKED`.
- Milestones: source chain reviewed; original blocked acceptance preserved; repaired path-scope behavior accepted; no-apply authority boundary accepted; warning debt classified; downstream resume route generated; validation run.
- Blockers: none for this narrow acceptance. Full JSON Schema, general diff parsing, artifact resolution, VCS reachability, policy, approval, apply, rollback, conformance runner, admission, trust, runtime, adapter execution, and case-folding policy remain deferred.
- Verification Intent: run Git status and diff checks, focused PatchTransaction tests, PatchTransaction status/validate, predecessor validators, repair-check and resume-task inspect/evidence checks, broad AIDE validation, JSON parsing, unsupported operation probes, secret-like scan, and commit-policy validation.
- Exit Criteria: `ACCEPTED_WITH_WARNINGS`, original blocked acceptance preserved, no implementation or forbidden operation, complete evidence, and exactly one next task: `AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01`.
- Notes: This task does not update CapabilityManifest records. Any aggregate capability projection requires separate authorization.

### Plan ID: AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01

- Title: Independent Recheck of PatchTransaction Portable Path-Scope Repair
- Status: needs_review
- Objective: independently recheck the PatchTransaction path-scope repair without modifying the implementation, schema, tests, failed-check evidence, repair reports, or blocked downstream records.
- Scope: repair-check task packet, task-local evidence, `.aide/reports/patch-transaction-repair-check/**`, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `FAILED_VALIDATION`; `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01` at `needs_review` with result `PASS_WITH_WARNINGS`; hardening commit `fca99236c2f933660de29b657dc181f1174dd719` at live `HEAD`.
- Milestones: source chain reviewed; independent drive-prefix and duplicate-normalization probes run; diagnostics reviewed; scope regressions checked; deterministic projection and source immutability verified; downstream blocked tasks preserved; reports and evidence written; validation run.
- Blockers: none for repair-check completion. Case-folding policy, full JSON Schema, general diff parsing, artifact resolution, VCS reachability, policy, approval, apply, rollback, runtime, adapter execution, admission, trust, and inherited warning debt remain deferred.
- Verification Intent: run Git status and diff checks, Python compilation, focused PatchTransaction tests, PatchTransaction status/project/validate, predecessor validators, repair/check task inspect and evidence checks, broad AIDE validation, JSON parsing, direct path probes, duplicate diagnostic assertions, repeated projection comparison, source immutability check, original failed-check preservation review, blocked downstream-record review, unsupported subcommand probes, secret-like scan, and commit-policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, no implementation or forbidden operation, both material defects independently rechecked as fixed, warning debt classified, complete evidence, and exactly one next task: `AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`.
- Notes: The original blocked acceptance, AdapterManifest, and ContextPack records remain historical; recovery proceeds through explicit resume tasks.

### Plan ID: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

- Title: Repair PatchTransaction Path-Scope Fail-Closed Validation
- Status: needs_review
- Objective: repair the material PatchTransaction path-scope defects found by `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` without widening the schema-only no-apply boundary.
- Scope: path normalization and scope validation repair in `core/protocol/patch_transaction.py`, focused regression tests, repair task packet, repair reports, queue index entry, and plan/execution log updates. No schema, CLI dispatch, accepted predecessor, failed-check evidence, runtime, adapter, provider, host, VCS, GitHub, OKF, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `PASS_WITH_WARNINGS`; `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `FAILED_VALIDATION`; live failed-check prompt recommends this repair.
- Milestones: live source chain inspected; repair task materialized; validator repaired; focused regression tests added; duplicate diagnostics hardened; full stricter repair report set added; repair reports and evidence written; validation run; task stopped at `needs_review`.
- Blockers: none for this bounded repair. PatchTransaction acceptance remains blocked until the repair is independently checked.
- Verification Intent: run compile checks, focused unit tests, direct path-scope probes, PatchTransaction status/project/validate, predecessor validators, repair task inspect/evidence checks, broad AIDE validation, JSON parsing, deterministic projection review, source mutation review, secret-like scan, Git diff checks, and commit policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, repaired path-scope fail-closed behavior, complete evidence, no apply/approval/policy/rollback/admission/trust/runtime behavior, and exactly one next task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: The repair preserves the failed independent check as historical evidence and does not accept `minimal_patch_transaction_schema`. Follow-up prompt alignment expanded tests and reports without changing the no-apply capability boundary.

### Plan ID: AIDE-CHECK-CONTEXTPACK-V2-01

- Title: Check ContextPack v2
- Status: needs_review
- Objective: process the ContextPack v2 independent-check prompt against live queue truth and stop before check execution if the source build or predecessor acceptance gates are not satisfied.
- Scope: blocked check task packet, task-local evidence, `.aide/reports/context-pack-v2-check/**`, queue index entry, and plan/execution log updates. No ContextPack v2 schema, helper, CLI, tests, projections, build reports, existing Context Compiler v0 outputs, accepted records, OKF pages, runtime, adapter, provider, VCS, GitHub, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-CONTEXTPACK-V2-01/task.yaml`.
- Dependencies: `AIDE-BUILD-CONTEXTPACK-V2-01` at `needs_review` with result `BLOCKED`; `AIDE-ACCEPT-ADAPTER-MANIFEST-01` at `needs_review` with result `BLOCKED`; `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `BLOCKED`.
- Milestones: live source chain inspected; check blocked; task packet and blocked check reports written; task-local evidence written; validation run; task stopped at `needs_review`.
- Blockers: ContextPack v2 build is `BLOCKED`, not `PASS` or `PASS_WITH_WARNINGS`; AdapterManifest and PatchTransaction acceptance are `BLOCKED`; the live queue recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: task inspect/evidence for ContextPack v2 build and this check, JSON parsing for the blocked check report, diff checks, secret-like scan, broad validation, and commit-policy check.
- Exit Criteria: `BLOCKED`, no ContextPack v2 check execution, no implementation or repair, no forbidden operation, complete evidence, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not check ContextPack v2 implementation because the build task did not pass and did not create the implementation slice.

### Plan ID: AIDE-BUILD-CONTEXTPACK-V2-01

- Title: Build ContextPack v2
- Status: needs_review
- Objective: process the ContextPack v2 build prompt against live queue truth and stop before implementation if AdapterManifest acceptance or PatchTransaction acceptance prerequisites are not satisfied.
- Scope: blocked build task packet, task-local evidence, `.aide/reports/context-pack-v2/**`, queue index entry, and plan/execution log updates. No ContextPack v2 schema, helper, CLI, tests, projections, context-pack outputs, accepted records, OKF pages, runtime, adapter, provider, VCS, GitHub, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONTEXTPACK-V2-01/task.yaml`.
- Dependencies: `AIDE-BUILD-ADAPTER-MANIFEST-01`, `AIDE-CHECK-ADAPTER-MANIFEST-01`, and `AIDE-ACCEPT-ADAPTER-MANIFEST-01` at `needs_review` with result `BLOCKED`; `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `BLOCKED`.
- Milestones: live source chain inspected; build blocked; task packet and blocked reports written; task-local evidence written; validation run; task stopped at `needs_review`.
- Blockers: AdapterManifest acceptance is `BLOCKED`, not `ACCEPTED` or `ACCEPTED_WITH_WARNINGS`; PatchTransaction acceptance is `BLOCKED`; the live queue recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: task inspect/evidence for AdapterManifest build/check/acceptance and this task, JSON parsing for the blocked report, diff checks, secret-like scan, broad validation, and commit-policy check.
- Exit Criteria: `BLOCKED`, no ContextPack v2 implementation or capability, no forbidden operation, complete evidence, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not build `context_pack_v2` because the prompt's execution-order gate is not satisfied.

### Plan ID: AIDE-ACCEPT-ADAPTER-MANIFEST-01

- Title: Accept Minimal AdapterManifest Schema
- Status: needs_review
- Objective: process the AdapterManifest acceptance prompt against live queue truth and stop before acceptance if the AdapterManifest build/check source chain or PatchTransaction acceptance prerequisite is not satisfied.
- Scope: blocked acceptance task packet, task-local evidence, `.aide/reports/adapter-manifest-accept/**`, queue index entry, and plan/execution log updates. No AdapterManifest schema, helper, CLI, focused tests, build/check reports, accepted predecessor, runtime, adapter, provider, host, VCS, OKF, GitHub, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-BUILD-ADAPTER-MANIFEST-01` at `needs_review` with result `BLOCKED`; `AIDE-CHECK-ADAPTER-MANIFEST-01` at `needs_review` with result `BLOCKED`; `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `BLOCKED`.
- Milestones: live source chain inspected; acceptance blocked; task packet and blocked acceptance reports written; task-local evidence written; validation run; task stopped at `needs_review`.
- Blockers: AdapterManifest build/check are `BLOCKED`, not `PASS` or `PASS_WITH_WARNINGS`; PatchTransaction acceptance is `BLOCKED`; the live queue recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: task inspect/evidence for AdapterManifest build, check, and this acceptance task; JSON parsing for the blocked acceptance report; diff checks; secret-like scan; broad validation; and commit-policy check.
- Exit Criteria: `BLOCKED`, no AdapterManifest acceptance, no implementation or repair, no forbidden operation, complete evidence, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not accept `minimal_adapter_manifest_schema` because the source chain is blocked.

### Plan ID: AIDE-CHECK-ADAPTER-MANIFEST-01

- Title: Check Minimal AdapterManifest Schema
- Status: needs_review
- Objective: process the AdapterManifest independent-check prompt against live queue truth and stop before check execution if the source build or PatchTransaction acceptance prerequisite is not satisfied.
- Scope: blocked check task packet, task-local evidence, `.aide/reports/adapter-manifest-check/**`, queue index entry, and plan/execution log updates. No AdapterManifest schema, helper, CLI, focused tests, build reports, accepted predecessor, runtime, adapter, provider, host, VCS, OKF, GitHub, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-BUILD-ADAPTER-MANIFEST-01` at `needs_review` with result `BLOCKED`; `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `BLOCKED`.
- Milestones: live source chain inspected; check blocked; task packet and blocked check reports written; task-local evidence written; validation run; task stopped at `needs_review`.
- Blockers: AdapterManifest build is `BLOCKED`, not `PASS` or `PASS_WITH_WARNINGS`; PatchTransaction acceptance is `BLOCKED`; the live queue recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: task inspect/evidence for AdapterManifest build and this check, JSON parsing for the blocked check report, diff checks, secret-like scan, broad validation, and commit-policy check.
- Exit Criteria: `BLOCKED`, no AdapterManifest check execution, no implementation or repair, no forbidden operation, complete evidence, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not check AdapterManifest implementation because the build task did not pass and did not create the implementation slice.

### Plan ID: AIDE-BUILD-ADAPTER-MANIFEST-01

- Title: Build Minimal AdapterManifest Schema
- Status: needs_review
- Objective: process the AdapterManifest build prompt against live queue truth and stop before implementation if the PatchTransaction acceptance prerequisite is not satisfied.
- Scope: blocked task packet, task-local evidence, `.aide/reports/adapter-manifest/**`, queue index entry, and plan/execution log updates. No AdapterManifest schema, helper, CLI, focused tests, projection, accepted predecessor, runtime, adapter, provider, host, VCS, OKF, GitHub, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-ADAPTER-MANIFEST-01/task.yaml`.
- Dependencies: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `PASS_WITH_WARNINGS`; `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `FAILED_VALIDATION`; `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `BLOCKED`.
- Milestones: live source chain inspected; implementation blocked; task packet and blocked reports written; task-local evidence written; validation run; task stopped at `needs_review`.
- Blockers: PatchTransaction acceptance is `BLOCKED`, not `ACCEPTED` or `ACCEPTED_WITH_WARNINGS`; the live queue recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: task inspect/evidence for PatchTransaction acceptance and this task, JSON parsing for the blocked report, diff checks, secret-like scan, broad validation, and commit-policy check.
- Exit Criteria: `BLOCKED`, no AdapterManifest implementation or capability, no forbidden operation, complete evidence, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not build AdapterManifest because the prompt's own execution-order gate is not satisfied.

### Plan ID: AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01

- Title: Accept Minimal PatchTransaction Schema
- Status: needs_review
- Objective: consolidate the live PatchTransaction build/check chain and either accept the minimal schema-only capability or block acceptance on live material findings.
- Scope: acceptance task packet, task-local evidence, `.aide/reports/patch-transaction-accept/**`, queue index entry, and plan/execution log updates. No PatchTransaction implementation, schema, tests, build/check reports, predecessor protocols, runtime, adapter, provider, host, VCS, OKF, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `PASS_WITH_WARNINGS`; `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` at `needs_review` with result `FAILED_VALIDATION`.
- Milestones: live queue reviewed; build and check evidence inspected; failed check preserved; acceptance reports written as blocked records; task evidence written; validation run; next repair task prompt generated.
- Blockers: independent check result is `FAILED_VALIDATION` and recommends `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Verification Intent: run Git diff checks, compile checks, focused tests, PatchTransaction status/validate, predecessor validators, build/check/accept task inspect and evidence checks, broad AIDE validation, JSON parsing, unsupported subcommand probes, secret-like scan, generated churn restoration, and commit policy validation.
- Exit Criteria: `BLOCKED`, no accepted PatchTransaction capability, no implementation or forbidden operation, complete evidence, failed check preserved, and exactly one next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: This task intentionally does not accept `minimal_patch_transaction_schema`. It preserves the failed check and routes to repair.

### Plan ID: AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01

- Title: Check Minimal PatchTransaction Schema
- Status: needs_review
- Objective: independently check the minimal PatchTransaction schema-only slice and determine whether it is ready for acceptance review.
- Scope: check task packet, task-local evidence, `.aide/reports/patch-transaction-check/**`, queue index entry, and plan/execution log updates. No implementation, schema, helper, test, build-report, predecessor, runtime, adapter, provider, host, VCS, OKF, or target-repository files are changed.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` exists at `needs_review` with result `PASS_WITH_WARNINGS`, complete evidence, and build commit `2559b1dbc528992451193d942bff741e8cb0a0a7` at live `HEAD`.
- Milestones: build source chain verified; schema/helper/report boundary reviewed; artifact digest independently recomputed; path-scope probes run; lifecycle, authority, CLI, report, determinism, and immutability checks completed; material findings classified; repair next-task prompt generated.
- Blockers: PatchTransaction acceptance is blocked by material path-scope defects: drive-prefixed relative paths and duplicate-normalized declared paths are accepted by the production scope validator.
- Verification Intent: run Git diff checks, compile checks, focused unit tests, PatchTransaction status/project/validate, predecessor validators, task inspect/evidence checks, broad AIDE validation, JSON parsing, independent digest recomputation, path-scope probes, unsupported subcommand probes, deterministic projection comparison, source immutability review, secret-like scan, and commit policy validation.
- Exit Criteria: `FAILED_VALIDATION`, complete evidence, no implementation or forbidden operation, warning debt classified, and exactly one recommended next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
- Notes: Deferred apply, policy, approval, admission, trust, rollback, artifact resolution, VCS reachability, and runtime behavior remain warnings. They are not the material blocker found by this check.

### Plan ID: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01

- Title: Build Minimal PatchTransaction Schema
- Status: needs_review
- Objective: build the first schema-only PatchTransaction protocol slice for proposed, bounded, inspectable repository mutations.
- Scope: schema, helper/model/projection/validation module, thin AIDE Lite CLI dispatch, deterministic reports, focused tests, task packet, task-local evidence, queue index entry, and root plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-OPERATIONAL-HEALTH-PAUSE-01` with result `PASS_WITH_WARNINGS` and readiness for this task; `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01` with result `ACCEPTED_WITH_WARNINGS`; accepted ReferenceID, EventRecord, EvidencePacket, WorkUnit, WorkerRun, TestJob, CapabilityManifest, ConformanceProfile, and ConformanceResult surfaces.
- Milestones: baseline verified; schema/helper/CLI/tests implemented; deterministic no-apply projection generated; reports and evidence written; validation matrix run; task stopped at `needs_review`.
- Blockers: none for the schema-only slice.
- Verification Intent: run compile checks, focused unit tests, `patch-transaction` status/project/validate, predecessor validators, JSON parsing, deterministic repeated projection comparison, source immutability review, task inspect/evidence checks, broad AIDE validation, secret-like scan, Git diff checks, and commit policy validation.
- Exit Criteria: `PASS_WITH_WARNINGS`, no accepted capability or trust grant from this build, no apply or target mutation, complete task evidence, and exactly one recommended next task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`.
- Notes: inherited operational-health warning debt is retained and classified as non-blocking for this schema-only build; any apply engine, approval engine, policy engine, AdapterManifest, ContextPack v2, runtime, worker execution, Workbench, provider/network behavior, branch/worktree automation, target mutation, release, or promotion remains deferred.

### Plan ID: AIDE-OPERATIONAL-HEALTH-PAUSE-01

- Title: Report-Only Operational Health Pause Before Mutation Work
- Status: needs_review
- Objective: assess operational health after ConformanceResult acceptance and before PatchTransaction or later operational-loop work.
- Scope: queue task packet, task-local evidence, operational-health-pause reports, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-OPERATIONAL-HEALTH-PAUSE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01` with result `ACCEPTED_WITH_WARNINGS`, accepted predecessor protocol/evidence reports, Reconciler, OKF, ReportIndex, GeneratedOutputLedger, and Track B B1 barrier evidence.
- Milestones: live queue truth verified; acceptance chain reviewed; ConformanceResult digest and historical failed check preserved; accepted protocol baseline reviewed; OKF/Reconciler/ReportIndex/GeneratedOutputLedger/Track B warning debt classified; PatchTransaction readiness assessed; reports and evidence written; validation run; task stopped at review.
- Blockers: none for beginning a schema-only PatchTransaction build. Report volume, ambiguity, stale context, Reconciler findings, historical review-gate debt, and runnerless/non-admitting ConformanceResult state remain warnings.
- Verification Intent: git state and diff checks, predecessor validators, OKF validate/lint, Reconciler status/validate, ReportIndex/GeneratedOutputLedger/Track B JSON parse checks, task inspect/evidence checks, broad AIDE validation, JSON parsing for the health report, secret-like scan, and commit policy validation.
- Exit Criteria: result is `PASS_WITH_WARNINGS`, health reports exist and parse, task evidence is complete, live queue truth is unambiguous, accepted predecessor integrity is confirmed, no forbidden operation occurred, PatchTransaction readiness is explicit, and next task is exactly `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`.
- Notes: This pause does not implement PatchTransaction. It authorizes no apply behavior, runtime behavior, adapter execution, provider/model/network calls, branch/worktree automation, target mutation, release, or promotion.

### Plan ID: AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01

- Title: Accept Minimal ConformanceResult Schema
- Status: needs_review
- Objective: accept the completed ConformanceResult build/check/repair/recheck chain as a bounded evidence-projected protocol capability without implementation repair.
- Scope: acceptance task packet, `conformance-result-accept` reports, evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01/task.yaml`.
- Dependencies: accepted predecessor `AIDE-ACCEPT-CONFORMANCE-PROFILE-01`, original build `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`, failed check `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`, repair `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`, and repair check `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.
- Milestones: live queue truth verified; acceptance task missing and authorized by repair-check next-task prompt; source chain reviewed; historical failed digest check preserved; repaired digest and repair-check evidence reviewed; warning debt classified; acceptance reports and evidence written; validation matrix run; task stopped at review.
- Blockers: none for accepting the bounded ConformanceResult record. Runtime, runner, execution, admission, trust, PatchTransaction, AdapterManifest, ContextPack v2, Service, Commander, provider/model calls, branch mutation, release, and target apply remain intentionally deferred.
- Verification Intent: JSON parsing for acceptance and predecessor reports, Python compile checks, focused ConformanceResult tests, ConformanceResult/Profile/CapabilityManifest validators, task inspect/evidence checks, broad AIDE validation, diff checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: result is `ACCEPTED_WITH_WARNINGS`, all required evidence and reports exist, failed-check and repair-chain evidence remain preserved, no implementation or predecessor artifacts are repaired, no forbidden operations are performed, and next task is `AIDE-OPERATIONAL-HEALTH-PAUSE-01`.
- Notes: This acceptance does not authorize PatchTransaction. It recommends a report-only operational-health pause before mutation or operational-loop work.

### Plan ID: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

- Title: Check Canonical ConformanceProfile Digest Repair
- Status: needs_review
- Objective: independently recheck `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01` without implementation repair and determine whether the corrected `ConformanceResult` digest binding is ready for acceptance review.
- Scope: repair-check task packet, `conformance-result-repair-check` reports, evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01` result `FAILED_VALIDATION`, repair task `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`, checked commit `00407e4d63d6ad72ce5184bee5b22e07fc56856e`, accepted candidate profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0`, and accepted CapabilityManifest evidence.
- Milestones: live queue truth verified; missing repair-check task confirmed; repair authorization and predecessor evidence inspected; independent canonical profile digest recomputed; bad-digest, copy-mutation, immutability, determinism, boundary, report, and evidence checks run; check reports and evidence written; validation matrix run; task stopped at review.
- Blockers: none. The digest repair check passes with retained non-capability warning debt.
- Verification Intent: Python compile checks, focused ConformanceResult tests, independent digest recomputation without production digest helper authority, bad-digest validation, lifecycle-warning copy mutation checks, repeated projection determinism, ConformanceResult status/project/validate, JSON report parsing, predecessor validators, task inspect/evidence checks, broad AIDE validation, diff checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: check result is `PASS_WITH_WARNINGS`, all required evidence and reports exist, the historical failed check remains preserved, no implementation artifacts are repaired, no forbidden operations are performed, and next task is `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`.
- Notes: This check does not accept ConformanceResult. It preserves that the result is evidence-projected, runnerless, not activated, not admitted, and not trusted.

### Plan ID: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

- Title: Repair Canonical ConformanceProfile Digest Binding
- Status: needs_review
- Objective: repair the ConformanceResult profile digest binding so projection and validation bind to the pristine accepted ConformanceProfile payload instead of a validation-warning-mutated profile copy.
- Scope: ConformanceResult digest helper/loading/validation repair, focused regression tests, regenerated ConformanceResult reports, repair reports, queue task packet, evidence, queue index, and execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01/task.yaml`.
- Dependencies: `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01` result `FAILED_VALIDATION`, accepted profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0`, and original `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` reports/evidence.
- Milestones: live failure reproduced; root cause located; `sha256-canonical-json-v1` implemented over pristine profile payload; regression tests added; ConformanceResult reports regenerated; repair reports and evidence written; validation matrix run; task stopped at review.
- Blockers: none for this repair. Independent repair recheck remains required before acceptance.
- Verification Intent: Python compile checks, focused ConformanceResult tests, independent digest recomputation without production helper import, repeated projection determinism check, ConformanceResult status/project/validate, JSON report parsing, predecessor validators, task inspect/evidence checks, broad AIDE validation, source-mutation review, diff checks, secret-like scan, and commit policy validation.
- Exit Criteria: corrected result digest equals independent pristine-profile digest, source profile remains unchanged, case and aggregate semantics remain unchanged, no execution/admission/trust behavior is added, all repair evidence exists, result is `PASS_WITH_WARNINGS`, and next task is `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.
- Notes: This repair does not supersede the failed check by itself. The historical failed check remains evidence and must be independently rechecked.

### Plan ID: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01

- Title: Check Minimal ConformanceResult Schema
- Status: needs_review
- Objective: independently check `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` without implementation repair and determine whether the evidence-projected `ConformanceResult` is ready for acceptance review.
- Scope: check task packet, `conformance-result-check` reports, evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` result `PASS_WITH_WARNINGS`, accepted candidate profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0`, accepted CapabilityManifest evidence, predecessor validators, and classified Track B B1 warning debt.
- Milestones: live queue truth verified; source chain reviewed; schema/helper/result/case/aggregation/evidence/admission/projection/CLI/report/test boundaries checked; profile digest independently recomputed from the raw profile payload; check reports and evidence written; validation matrix run; task stopped at review.
- Blockers: acceptance is blocked by `profile_digest_mismatch`. The recorded ConformanceResult profile digest does not match the raw accepted ConformanceProfile report payload.
- Verification Intent: JSON parsing for check reports, task inspect/evidence checks, `conformance-result status/validate`, predecessor validators, broad AIDE validation, independent raw profile digest recomputation, diff whitespace checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: check result is `FAILED_VALIDATION`, all required evidence and reports exist, no implementation artifacts are repaired, no forbidden operations are performed, and next task is `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.
- Notes: Most non-digest boundaries pass. The check does not accept ConformanceResult and does not recommend moving to PatchTransaction or any later Track A task.

### Plan ID: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01

- Title: Minimal ConformanceResult For CapabilityManifest Profile Observations
- Status: needs_review
- Objective: build the first evidence-projected `ConformanceResult` for the accepted `minimal_capability_manifest` ConformanceProfile candidate while preserving the result/admission/trust separation.
- Scope: ConformanceResult schema, helper/projection/validation module, `conformance-result status/project/validate` CLI dispatch, deterministic result and case-result reports, focused tests, queue task packet, evidence, and execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-CONFORMANCE-PROFILE-01` result `ACCEPTED_WITH_WARNINGS`, accepted candidate profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0`, accepted CapabilityManifest evidence, ReferenceID/EventRecord validation surfaces, and Track B B1 warning debt remaining classified rather than repaired.
- Milestones: live queue truth verified; prompt and governing docs reviewed; schema/helper/CLI/tests implemented; ConformanceResult reports generated; queue task and evidence written; validation matrix run; task stopped at review.
- Blockers: none. Conformance runner, case execution, command execution, automatic result collection, profile activation, conformance admission, subject admission, trust grants, adapter admission/execution, PatchTransaction, AdapterManifest, ContextPack v2, runtime, worker execution, provider/model/network/Gateway calls, target apply, branch/worktree automation, release, promotion, production readiness, and broad autonomous runtime behavior remain intentionally deferred.
- Verification Intent: Python compile checks, focused ConformanceResult unit tests, `conformance-result status/project/validate`, JSON parsing for generated reports, predecessor validators, task inspect/evidence checks, broad AIDE validation, diff whitespace checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: evidence-projected result `aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01` exists with profile digest binding, case-result records, fail-closed aggregation, explicit non-capabilities, deterministic reports, complete evidence, `PASS_WITH_WARNINGS`, and next task `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.
- Notes: This slice records observed outcomes from existing evidence only. It does not execute cases, admit the subject, activate the profile, grant trust, or authorize mutation.

### Plan ID: AIDE-ACCEPT-CONFORMANCE-PROFILE-01

- Title: Accept Minimal ConformanceProfile
- Status: needs_review
- Objective: accept the build/check ConformanceProfile chain as the narrow `minimal_conformance_profile` protocol capability while preserving candidate-only, no-result, no-execution, no-admission, and no-trust boundaries.
- Scope: acceptance task packet, `conformance-profile-accept` reports, evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-CAPABILITY-MANIFEST-01` result `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-CONFORMANCE-PROFILE-01` result `PASS_WITH_WARNINGS`, `AIDE-CHECK-CONFORMANCE-PROFILE-01` result `PASS_WITH_WARNINGS`, and Track B B1 read-only governance evidence.
- Milestones: live queue truth verified; source chain reviewed; schema/profile/case/aggregation/versioning/evidence/admission/governance boundaries accepted; warnings dispositioned; acceptance reports and evidence written; validation matrix run; task stopped at review.
- Blockers: none. ConformanceResult, conformance runner/execution/admission, profile activation, subject admission by conformance, trust grants, adapter admission/execution, PatchTransaction, AdapterManifest, ContextPack v2, runtime, Service, Commander, provider/model/network/Gateway calls, branch/worktree automation, target apply, release, promotion, production readiness, and broad autonomous runtime behavior remain intentionally deferred.
- Verification Intent: Python compile checks, focused ConformanceProfile tests, `conformance-profile status/validate`, report JSON parsing, task inspect/evidence checks, predecessor validators, broad AIDE validation, source-mutation review, diff whitespace checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: acceptance result is `ACCEPTED_WITH_WARNINGS`, all required evidence and reports exist, no implementation/predecessor artifacts are repaired, the candidate profile remains inactive, and next task is `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.
- Notes: This accepts the ability to define and validate candidate profiles, not the candidate profile as active policy and not the subject by conformance.

### Plan ID: AIDE-CHECK-CONFORMANCE-PROFILE-01

- Title: Check Minimal ConformanceProfile
- Status: needs_review
- Objective: independently check `AIDE-BUILD-CONFORMANCE-PROFILE-01` without implementation repair and determine whether the candidate profile is ready for acceptance review.
- Scope: check task packet, `conformance-profile-check` reports, evidence, queue index entry, and plan/execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-CONFORMANCE-PROFILE-01/task.yaml`.
- Dependencies: `AIDE-BUILD-CONFORMANCE-PROFILE-01` result `PASS_WITH_WARNINGS`, accepted `minimal_capability_manifest`, predecessor validators, and classified Track B B1 warning debt.
- Milestones: live queue truth verified; source chain reviewed; schema/helper/model/case/CLI/report/test boundaries checked; warnings dispositioned; check reports and evidence written; validation matrix run; task stopped at review.
- Blockers: none. `ConformanceResult`, conformance runner/execution/admission, adapter admission/execution, PatchTransaction, AdapterManifest, ContextPack v2, Test Broker runtime, runtime, Service, Commander, provider/model/network/Gateway calls, target apply, branch/worktree automation, release, promotion, production readiness, and broad autonomous runtime behavior remain intentionally deferred.
- Verification Intent: Python compile checks, focused ConformanceProfile tests, `conformance-profile status/project/validate`, report JSON parsing, task inspect/evidence checks, predecessor validators, broad AIDE validation, determinism/source-mutation sentinel, diff whitespace checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: check result is `PASS_WITH_WARNINGS`, no blockers exist, all required evidence and reports exist, no implementation artifacts are repaired, no forbidden operations are performed, and next task is `AIDE-ACCEPT-CONFORMANCE-PROFILE-01`.
- Notes: The check is not an acceptance decision and does not create observed conformance outcomes.

### Plan ID: AIDE-BUILD-CONFORMANCE-PROFILE-01

- Title: Minimal ConformanceProfile For CapabilityManifest Admission Requirements
- Status: needs_review
- Objective: build the first candidate `ConformanceProfile` for the accepted `minimal_capability_manifest` capability while preserving the declaration/profile/result/admission separation.
- Scope: ConformanceProfile schema, helper/projection/validation module, `conformance-profile status/project/validate` CLI dispatch, deterministic profile and case reports, focused tests, queue task packet, evidence, and execution log updates.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONFORMANCE-PROFILE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-CAPABILITY-MANIFEST-01` result `ACCEPTED_WITH_WARNINGS`, existing ReferenceID and EventRecord validation surfaces, and Track B B1 warning debt remaining classified rather than repaired.
- Milestones: live queue truth verified; prompt and governing docs reviewed; schema/helper/CLI/tests implemented; ConformanceProfile reports generated; queue task and evidence written; validation matrix run; task stopped at review.
- Blockers: none. `ConformanceResult`, conformance execution, admission policy, adapter admission/execution, PatchTransaction, AdapterManifest, ContextPack v2, runtime, worker execution, provider/model/network/Gateway calls, target apply, branch/worktree automation, release, promotion, production readiness, and broad autonomous runtime behavior remain intentionally deferred.
- Verification Intent: Python compile checks, focused ConformanceProfile unit tests, `conformance-profile status/project/validate`, JSON parsing for generated reports, predecessor validators, task inspect/evidence checks, broad AIDE validation, diff whitespace checks, generated churn containment, secret-like scan, and commit policy validation.
- Exit Criteria: candidate profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0` exists with profile-scoped cases, fail-closed aggregation, evidence requirements, explicit non-capabilities, deterministic reports, complete evidence, `PASS_WITH_WARNINGS`, and next task `AIDE-CHECK-CONFORMANCE-PROFILE-01`.
- Notes: This slice defines admission requirements only. It does not create observed conformance outcomes or trust/admit any capability.

### Plan ID: AIDE-ADOPT-APACHE-2-LICENSE-01

- Title: Adopt Apache-2.0 Permissive Licensing Docs
- Status: needs_review
- Objective: replace the no-public-license posture with a standard Apache-2.0 legal-doc packet for AIDE.
- Scope: queue packet, Apache-2.0 license text, NOTICE, licensing policy, generated-output policy, trademark policy, license summary, README license blurb, contribution license guidance, documentation index, planning log, execution log, task evidence, and scoped commit.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ADOPT-APACHE-2-LICENSE-01/task.yaml`.
- Dependencies: user-supplied permissive licensing drafts under `C:/Downloads/`, official Apache-2.0 and SPDX license references, current bypass/queue policy, and live clean worktree preflight.
- Milestones: repo state inspected; docs and queue skills loaded; intent and git plan preflight run; queue packet materialized; legal docs written; root docs updated; evidence recorded; validation run; generated helper churn contained; scoped commit created.
- Blockers: none for repository documentation. Counsel review remains an external review requirement before public release, commercial launch, foundation transfer, dual licensing, or trademark registration.
- Verification Intent: official Apache-2.0/SPDX reference check, AIDE doctor, AIDE validation, intent validation, task inspect/evidence checks, diff whitespace checks, changed-file review, generated helper drift containment, and commit policy validation.
- Exit Criteria: root legal docs exist and describe Apache-2.0 default licensing, generated-output ownership boundary, inbound=outbound contribution licensing, and trademark/project identity boundary; README no longer says there is no public license; task evidence is complete; status stops at `needs_review`; scoped commit passes commit policy.
- Notes: This task changes licensing documentation and contribution/trademark/generated-output policy only. It does not publish a release, create tags, mutate GitHub, create or promote branches, require a CLA, register trademarks, change runtime behavior, change protocol schemas, promote generated outputs as source truth, call providers/models/network services, or mutate target repositories.

### Plan ID: AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01

- Title: Acceptance Review For Deterministic OKF-Compatible AIDE Knowledge Bundle
- Status: needs_review
- Objective: accept only the checked `minimal_okf_knowledge_bundle` capability after reviewing OKF build and independent check evidence.
- Scope: acceptance queue packet, `okf-accept` reports, source-chain review, OKF structure/frontmatter/projection/CLI/lint/index review, ReferenceID and EventRecord integration review, warning disposition, explicit non-capability boundary, next Reconciler Reports prompt, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01` result `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` result `PASS_WITH_WARNINGS`, and `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01` result `PASS_WITH_WARNINGS`.
- Milestones: live queue truth verified; stale latest task packet classified; build and check evidence reviewed; warnings dispositioned; acceptance reports written; Reconciler Reports next-task prompt generated; task stopped at review.
- Blockers: none. Full YAML parser integration, Reconciler implementation, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime knowledge service, event sourcing runtime, append-only event store, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: acceptance report JSON parsing, task inspect/evidence checks, OKF status/validate/lint, predecessor protocol validators, broad repository validation, diff whitespace checks, generated-report churn containment, and commit policy validation.
- Exit Criteria: acceptance result is `ACCEPTED_WITH_WARNINGS`, evidence and reports exist, no implementation code changes are made, explicit non-capabilities are preserved, and next task is `AIDE-BUILD-RECONCILER-REPORTS-01`.
- Notes: `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority. This acceptance does not implement Reconciler.

### Plan ID: AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01

- Title: Independent Check For Deterministic OKF-Compatible AIDE Knowledge Bundle
- Status: needs_review
- Objective: independently check the `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` build without repairing implementation files or advancing to Reconciler.
- Scope: check queue packet, `okf-check` reports, build evidence review, OKF structure/frontmatter/projection/CLI/lint/index review, ReferenceID and EventRecord integration review, predecessor compatibility review, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01/task.yaml`.
- Dependencies: `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` result `PASS_WITH_WARNINGS`; reported build commit `c51859006e8cf4ac429bbaf9663917d0fdbe904b`, which is an ancestor of the live HEAD reviewed for this check; accepted EventRecord and ReferenceID predecessor surfaces.
- Milestones: live queue truth verified; stale prompt-reported dirty state reconciled; generated pre-check report churn contained; build evidence and OKF reports reviewed; check evidence and reports written; deterministic projection and validation commands run; task stopped at review.
- Blockers: none. Full YAML parser integration, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime knowledge service, event sourcing runtime, append-only event store, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: diff whitespace checks, Python compile checks, focused OKF tests, `okf status/project/validate/lint`, OKF and okf-check JSON parsing, EventRecord and ReferenceID validators, task inspect/evidence checks for build and check tasks, broad repository validation, generated-report churn containment, and commit policy validation.
- Exit Criteria: result is `PASS_WITH_WARNINGS`, all required evidence and `okf-check` reports exist, no implementation repair is made, no generated churn outside scope remains, and next task is `AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01`.
- Notes: `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority. The prompt-reported dirty intake state was stale relative to live repo truth.

### Plan ID: DOCS-PUBLIC-README-POSITIONING-01

- Title: Public README Positioning Refresh
- Status: completed
- Objective: make the root README public-facing and future-proof by positioning AIDE as a portable agentic development control plane for real repositories while preserving current implementation boundaries.
- Scope: public README rewrite, contributor claim-discipline guidance, roadmap status alignment, documentation-index alignment, execution-log entry, and intake preflight evidence.
- Allowed Paths: `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `DOCUMENTATION.md`, `PLANS.md`, `IMPLEMENT.md`, and `.aide/intake/preflight-or-blocker-report.md`.
- Dependencies: explicit user authorization after the initial intake blocker, live queue/status inspection, current OKF validation output, and external reference verification for OKF, LLM Wiki, and Codex `AGENTS.md` context.
- Milestones: repo state inspected; docs/roadmap skills loaded; live protocol and OKF status reconciled; external references checked; README rewritten with diagram, status warning, differentiation table, OKF section, roadmap, and implementation-status table; supporting root docs updated; validation run; generated latest-intake and task-status report churn contained.
- Blockers: the first intent compile classified the broad public README request as blocked release/public-positioning work. The user then explicitly authorized the bounded docs-only refresh. No release publication, tag, branch mutation, queue status mutation, code change, runtime work, provider/model call, target mutation, or GitHub mutation is authorized by this plan.
- Verification Intent: `okf status`, `okf validate`, `intent validate`, broad repository validation if practical, `git diff --check`, Markdown/link sanity review, and final diff review.
- Exit Criteria: README advertises AIDE as a portable agentic development control plane; public claims distinguish implemented-for-review, metadata-only, projection-only, report-only, planned, and not-started surfaces; supporting root docs agree with the README; validation passes or gaps are recorded; no generated report churn remains unintentionally in scope.
- Notes: This is a docs-only positioning pass. It does not change repository law, support tiers, capability levels, protocol schemas, queue statuses, release posture, branch state, or runtime behavior.

### Plan ID: AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01

- Title: Deterministic OKF-Compatible AIDE Knowledge Bundle
- Status: needs_review
- Objective: build the first deterministic OKF-compatible AIDE knowledge bundle projection after accepted EventRecord, while preserving protocol/evidence/reference/event authority.
- Scope: OKF helper, stdlib structural frontmatter writer/parser/validator, `okf status/project/validate/lint` CLI dispatch, `.aide/knowledge/okf/**`, `.aide/reports/okf/**`, focused tests, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01` result `ACCEPTED_WITH_WARNINGS`, accepted ReferenceID scheme, and predecessor ContractEnvelope, EvidencePacket, WorkUnit, WorkerRun, and TestJob protocol validation surfaces.
- Milestones: live queue truth verified; stale latest task packet classified; OKF helper and frontmatter subset added; CLI dispatch added; 24 concept pages plus reserved `index.md` and `log.md` generated; OKF reports written; focused tests passed; evidence written; task stopped at review.
- Blockers: none. Full YAML parser integration, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime knowledge service, event sourcing runtime, append-only event store, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: Python compile checks, focused OKF tests, `okf status/project/validate/lint`, report JSON parsing, predecessor protocol validators, task inspect/evidence checks, broad repository validation, generated-report churn containment, and diff whitespace checks.
- Exit Criteria: `okf validate` and `okf lint` report `PASS_WITH_WARNINGS`, generated bundle and reports exist, no predecessor artifacts are mutated, no forbidden operations are performed, and next task is `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.
- Notes: `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority. OKF pages explain current truth but do not replace queue, protocol, evidence, ReferenceID, or EventRecord authority.

### Plan ID: AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01

- Title: Acceptance Review For Projection-Only AIDE EventRecord Schema
- Status: needs_review
- Objective: accept only the checked `minimal_event_record_schema` capability after reviewing EventRecord build and independent check evidence.
- Scope: acceptance queue packet, `event-record-accept` reports, source-chain review, schema/helper/projection/CLI/test review, warning disposition, explicit non-capability boundary, next OKF prompt, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` result `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` result `PASS_WITH_WARNINGS`, and `AIDE-CHECK-EVENT-RECORD-SCHEMA-01` result `PASS_WITH_WARNINGS`.
- Milestones: live queue state verified; stale latest task packet classified; build and check evidence reviewed; warnings dispositioned; acceptance reports written; OKF next-task prompt generated; task stopped at review.
- Blockers: none. Event sourcing runtime, append-only event store, runtime event log, replay, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF implementation, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: acceptance report JSON parsing, task inspect/evidence checks, EventRecord status/validate, predecessor protocol validators, broad repository validation, diff whitespace checks, generated-report churn containment, and commit policy validation.
- Exit Criteria: acceptance result is `ACCEPTED_WITH_WARNINGS`, evidence and reports exist, no implementation code changes are made, explicit non-capabilities are preserved, and next task is `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`.
- Notes: `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority. This acceptance does not implement OKF.

### Plan ID: AIDE-CHECK-EVENT-RECORD-SCHEMA-01

- Title: Independent Check For Projection-Only AIDE EventRecord Schema
- Status: needs_review
- Objective: independently check the minimal projection-only EventRecord protocol slice from `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` without changing implementation files.
- Scope: check queue packet, `event-record-check` reports, build evidence review, EventRecord schema/helper/projection/CLI/test review, predecessor compatibility review, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-EVENT-RECORD-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` result `PASS_WITH_WARNINGS`, `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` result `ACCEPTED_WITH_WARNINGS`, and the accepted/minimal ContractEnvelope, EvidencePacket, WorkUnit queue, WorkerRun, TestJob, and ReferenceID predecessor protocol slices.
- Milestones: live queue state verified; stale latest task packet classified; build evidence reviewed; schema/helper/projection/CLI/test/report evidence checked; predecessor validators rerun; generated report churn restored; check reports written; task stopped at review.
- Blockers: none. Event sourcing runtime, append-only event store, runtime event log, replay, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: focused EventRecord tests, Python compile checks, schema/report JSON parsing, `event-record status/project/validate`, `reference-id validate`, predecessor protocol validations, task inspect/evidence checks, overclaim review, forbidden-operation review, broad repo validation, and diff whitespace checks.
- Exit Criteria: check result is `PASS_WITH_WARNINGS`, evidence and reports exist, no implementation files are changed, no forbidden operations are performed, and next task is `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`.
- Notes: `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority. This check does not recommend moving directly to OKF.

### Plan ID: AIDE-BUILD-EVENT-RECORD-SCHEMA-01

- Title: Minimal EventRecord Schema
- Status: needs_review
- Objective: build the minimal projection-only EventRecord protocol slice after accepted ReferenceID, using stable `aide://...` refs for event identity, subject, causation, correlation, evidence, and report references.
- Scope: EventRecord schema, helper, thin `event-record` CLI dispatch, event family index, projection-only example events, validation reports, focused tests, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-EVENT-RECORD-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` result `ACCEPTED_WITH_WARNINGS`, plus the accepted/minimal ContractEnvelope, EvidencePacket, WorkUnit queue, WorkerRun, TestJob, and ReferenceID predecessor protocol slices.
- Milestones: live queue state verified; stale latest task packet classified; EventRecord schema/helper added; CLI dispatch added; event family index, projection examples, and validation reports written; focused tests passed; evidence written; task stopped at review.
- Blockers: none for this bounded slice. Event sourcing runtime, append-only event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime remain out of scope.
- Verification Intent: focused EventRecord tests, Python compile checks, schema/report JSON parsing, `event-record status/project/validate`, `reference-id validate`, predecessor protocol validations, task inspect/evidence checks, overclaim scans, broad repo validation, and diff whitespace checks.
- Exit Criteria: `event-record validate` reports `PASS_WITH_WARNINGS`, evidence and reports exist, no predecessor artifacts are mutated, no forbidden operations are performed, and next task is `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.
- Notes: `.aide/context/latest-task-packet.md` is stale lifecycle-runner text and is not authority for this build. This task lists OKF only as future work after EventRecord check and acceptance; it does not recommend OKF directly.

### Plan ID: AIDE-ACCEPT-REFERENCE-ID-SCHEME-01

- Title: Acceptance Review For Stable AIDE Reference ID Scheme
- Status: needs_review
- Objective: accept only the `minimal_reference_id_scheme` capability after reviewing the ReferenceID build and independent check chain.
- Scope: acceptance queue packet, `reference-id-accept` reports, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-TESTJOB-SCHEMA-01` result `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-REFERENCE-ID-SCHEME-01` result `PASS_WITH_WARNINGS`, and `AIDE-CHECK-REFERENCE-ID-SCHEME-01` result `PASS_WITH_WARNINGS`.
- Milestones: live queue state verified; stale latest task packet classified; build and check evidence reviewed; schema/helper/projection/reference-map/CLI/test evidence checked; warnings dispositioned; acceptance reports written; EventRecord next-task prompt generated; task stopped at review.
- Blockers: none. Full JSON Schema Draft 2020-12 validation, runtime registry, resolver service, EventRecord implementation, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime coordination, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, and model/provider calls remain out of scope.
- Verification Intent: acceptance-report JSON parsing, task inspect/evidence checks, `reference-id status/validate`, predecessor protocol validations, broad repository validation, overclaim scans, diff whitespace checks, generated-report churn containment, and commit policy validation.
- Exit Criteria: acceptance result is `ACCEPTED_WITH_WARNINGS`, evidence and reports exist, no implementation code changes are made, and next task is `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`.
- Notes: `.aide/context/latest-task-packet.md` is stale lifecycle-runner text and is not authority. This acceptance records EventRecord only as the next bounded queue task; it does not implement EventRecord.

### Plan ID: AIDE-CHECK-REFERENCE-ID-SCHEME-01

- Title: Independent Check For Stable AIDE Reference ID Scheme
- Status: needs_review
- Objective: independently check the minimal metadata-only ReferenceID scheme from `AIDE-BUILD-REFERENCE-ID-SCHEME-01` without changing implementation code.
- Scope: check queue packet, `reference-id-check` reports, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-REFERENCE-ID-SCHEME-01/task.yaml`.
- Dependencies: `AIDE-BUILD-REFERENCE-ID-SCHEME-01` result `PASS_WITH_WARNINGS`, accepted TestJob predecessor, and accepted/minimal predecessor protocol validation surfaces.
- Milestones: live queue state verified; build evidence reviewed; schema/helper/projection/CLI/reference-map/tests checked; predecessor validators rerun; reports and evidence written; task stopped at review.
- Blockers: none. Full JSON Schema Draft 2020-12 validation, runtime registry, resolver service, EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime coordination, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, and model/provider calls remain out of scope.
- Verification Intent: focused ReferenceID tests, Python compile checks, schema/report JSON parsing, `reference-id status/project/validate`, predecessor protocol validations, task inspect/evidence checks, overclaim scans, broad repo validation, and diff whitespace checks.
- Exit Criteria: check result is `PASS_WITH_WARNINGS`, evidence and reports exist, no implementation files are changed, no forbidden operations are performed, and next task is `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`.
- Notes: `.aide/context/latest-task-packet.md` is stale lifecycle-runner text and is not authority. This check does not recommend moving directly to EventRecord.

### Plan ID: AIDE-BUILD-REFERENCE-ID-SCHEME-01

- Title: Minimal Reference ID Scheme
- Status: needs_review
- Objective: build the minimal metadata-only ReferenceID scheme after accepted TestJob, using stable `aide://<kind>/<id>` identities with file paths as locators.
- Scope: ReferenceID schema, helper, thin `reference-id` CLI dispatch, additive reference map reports, focused tests, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-TESTJOB-SCHEMA-01` result `ACCEPTED_WITH_WARNINGS`, plus the accepted ContractEnvelope, EvidencePacket, WorkUnit queue, WorkerRun, and TestJob predecessor protocol slices.
- Milestones: live queue state verified; ReferenceID schema/helper added; CLI dispatch added; reference map projection and validation reports written; focused tests passed; evidence written; task stopped at review.
- Blockers: none for this bounded slice. Full JSON Schema Draft 2020-12 validation, runtime registry, resolver service, EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime coordination, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, and model/provider calls remain out of scope.
- Verification Intent: focused ReferenceID tests, Python compile checks, schema/report JSON parsing, `reference-id status/project/validate`, predecessor protocol validations, task inspect/evidence checks, overclaim scans, and diff whitespace checks.
- Exit Criteria: `reference-id validate` reports `PASS_WITH_WARNINGS`, evidence and reports exist, no predecessor artifacts are mutated, no forbidden operations are performed, and next task is `AIDE-CHECK-REFERENCE-ID-SCHEME-01`.
- Notes: `.aide/context/latest-task-packet.md` is stale relative to queue truth and is not authority for this build. This task does not recommend moving directly to EventRecord.

### Plan ID: AIDE-ACCEPT-TESTJOB-SCHEMA-01

- Title: Acceptance Review For Minimal Metadata-Only TestJob Schema
- Status: needs_review
- Objective: accept the minimal metadata-only TestJob schema/helper/projection/validation slice after build and independent check evidence review.
- Scope: acceptance queue packet, `test-job-accept` reports, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-WORKER-RUN-SCHEMA-01` result `ACCEPTED_WITH_WARNINGS`, `AIDE-BUILD-TESTJOB-SCHEMA-01` result `PASS`, and `AIDE-CHECK-TESTJOB-SCHEMA-01` result `PASS_WITH_WARNINGS`.
- Milestones: live queue state verified; build and check evidence reviewed; warnings dispositioned; acceptance reports written; next-task prompt for ReferenceID generated; task stopped at review.
- Blockers: none. Full JSON Schema Draft 2020-12 validation, Test Broker runtime, async execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, Service, Commander, providers, Gateway, network, GitHub mutation, branch automation, target apply, release, promotion, and PatchTransaction remain out of scope.
- Verification Intent: JSON validation for the acceptance report, task inspect/evidence checks, TestJob status/validate, predecessor protocol validations, repository validation, diff whitespace checks, and generated-report churn containment.
- Exit Criteria: acceptance result is `ACCEPTED_WITH_WARNINGS`, evidence and reports exist, no implementation code changes are made, and next task is `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.
- Notes: `.aide/context/latest-task-packet.md` is stale relative to queue truth and is not authority for this acceptance review.

### Plan ID: AIDE-CHECK-TESTJOB-SCHEMA-01

- Title: Independent Check For Minimal TestJob Schema
- Status: needs_review
- Objective: independently check the minimal metadata-only TestJob schema/helper/projection/validation slice from `AIDE-BUILD-TESTJOB-SCHEMA-01`.
- Scope: check queue packet, `test-job-check` report, task-local evidence, queue index, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-BUILD-TESTJOB-SCHEMA-01` result `PASS` and accepted metadata-only WorkerRun predecessor.
- Milestones: queue packet created; build evidence reviewed; focused structural checks and TestJob tests run; CLI and predecessor validation run; unsupported execution subcommands checked; evidence written; task stopped at review.
- Blockers: none. Full JSON Schema Draft 2020-12 validation, Test Broker runtime, async execution, scheduler, leases, worker execution, Service, Commander, providers, Gateway, network, GitHub mutation, branch automation, target apply, release, and promotion remain out of scope.
- Verification Intent: focused TestJob tests, schema/report JSON parsing, `test-job status/project/validate`, predecessor protocol validations, unsupported subcommand fail-closed checks, secret and overclaim scans, task inspect/evidence checks, and diff whitespace checks.
- Exit Criteria: check result is `PASS_WITH_WARNINGS`, evidence and report files exist, no implementation code changes are made, and next task is `AIDE-ACCEPT-TESTJOB-SCHEMA-01`.
- Notes: The attached frozen sequence places `AIDE-BUILD-REFERENCE-ID-SCHEME-01` after TestJob acceptance, superseding the older build evidence's PatchTransaction-after-acceptance note unless live queue truth changes.

### Plan ID: AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01

- Title: Minimal EvidencePacket Schema
- Status: needs_review
- Objective: extract a minimal EvidencePacket schema, helper, projection, validation, and CLI slice from accepted lifecycle fixture runner and contract-envelope artifacts.
- Scope: queue packet, `core/protocol/evidence_packet.py`, EvidencePacket schema, thin `evidence-packet` CLI dispatch, focused tests, additive EvidencePacket reports, and planning/execution evidence.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-CONTRACT-ENVELOPE-01` result `ACCEPTED_WITH_WARNINGS`.
- Milestones: queue packet created; helper and schema added; CLI dispatch added; accepted-slice projections generated; focused tests added; evidence written; task stopped at review.
- Blockers: none for this bounded slice. Full evidence engine, EvidenceStore, WorkUnit schema/CLI, TestJob schema, Test Broker, Checkpoint, PromotionPolicy, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, Gateway, network, GitHub, and model/provider calls remain out of scope.
- Verification Intent: py_compile, focused EvidencePacket tests, existing contract-envelope and lifecycle fixture tests, EvidencePacket status/project/validate, contract-envelope status/project/validate, lifecycle-fixture status/run/verify, AIDE Lite validate/test, task inspect/evidence, JSON/YAML structural checks, overclaiming/secret scans, and diff whitespace checks.
- Exit Criteria: `evidence-packet validate` reports schema loaded, parsed, subset validation executed, helper/schema alignment checked, projections valid, explicit non-capabilities preserved, compatibility preserved, and the task ends at `needs_review` with no forbidden operations.
- Notes: This is the evidence packet contract slice only; WorkUnit objects and an evidence engine are intentionally deferred.

### Plan ID: AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01

- Title: Contract Envelope Schema Runtime Alignment Hardening
- Status: needs_review
- Objective: close or materially reduce the CHECK-01 warning by wiring the minimal contract envelope schema into runtime validation.
- Scope: queue packet, `core/protocol/envelope.py`, thin `contract-envelope validate` CLI output, focused contract-envelope tests, generated contract-envelope reports, hardening reports, and planning/execution evidence.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01/task.yaml`.
- Dependencies: `AIDE-BUILD-CONTRACT-ENVELOPE-01` and `AIDE-CHECK-CONTRACT-ENVELOPE-01` result `PASS_WITH_WARNINGS`.
- Milestones: queue packet created; schema loader and subset validator added; schema/helper alignment checks added; validation reports updated; tests expanded; evidence written; task stopped at review.
- Blockers: none for this bounded hardening slice. Full JSON Schema engine, EvidencePacket schema, WorkUnit schema/CLI, TestJob schema, Test Broker, Service, Commander, providers, branch/worktree automation, target apply, rollback execution, release, Gateway, network, GitHub, and model/provider calls remain out of scope.
- Verification Intent: py_compile, focused contract-envelope tests, lifecycle fixture tests, apply tests, contract-envelope status/project/validate, lifecycle-fixture status/run/verify, AIDE Lite validate/test, task inspect/evidence, JSON/YAML structural checks, overclaiming/secret scans, and diff whitespace checks.
- Exit Criteria: `contract-envelope validate` reports schema loaded, parsed, subset validation executed, helper/schema alignment checked, compatibility preserved, and the task ends at `needs_review` with no forbidden operations.
- Notes: This keeps the schema executable enough for the current envelope while explicitly deferring full JSON Schema Draft 2020-12 support.

### Plan ID: AIDE-BUILD-CONTRACT-ENVELOPE-01

- Title: Minimal Contract Envelope Slice
- Status: needs_review
- Objective: introduce the minimal public protocol envelope shape earned by the accepted lifecycle fixture runner slice.
- Scope: queue packet, minimal protocol helper, envelope schema, thin AIDE Lite dispatch, focused tests, contract-envelope projections/reports, and planning/execution log entries.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-01/task.yaml`.
- Dependencies: `AIDE-ACCEPT-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01` result `ACCEPTED_WITH_WARNINGS`.
- Milestones: queue packet created; envelope helper/schema added; lifecycle fixture reports projected; validation and tests pass; evidence written; task stopped at review.
- Blockers: none for this bounded slice. Full kernel schemas, WorkUnit CLI, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, rollback execution, release, Gateway, network, GitHub, and model/provider calls remain out of scope.
- Verification Intent: focused contract-envelope tests, existing lifecycle fixture tests, transaction/managed-section tests, contract-envelope status/project/validate commands, lifecycle-fixture status/run/verify commands, AIDE Lite validate/test, task inspect/evidence, JSON parse checks, overclaiming/secret scans, and diff whitespace checks.
- Exit Criteria: task status is `needs_review`, generated projections validate, legacy lifecycle reports remain readable and unmigrated, explicit non-capabilities are preserved, and no forbidden operations are performed.
- Notes: This is a protocol-shaped vertical slice, not a kernel scaffold. The helper is intentionally `v1alpha1` and limited to lifecycle fixture runner reports.

### Plan ID: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01

- Title: Lifecycle Fixture Temp Runner
- Status: needs_review
- Objective: implement one protocol-shaped lifecycle fixture slice that copies a canonical fixture into a temp workspace, applies the managed-section transaction there, verifies the postimage, and emits evidence without active-repo or target-repo mutation.
- Scope: queue packet, latest task packet, lifecycle fixture runner module, thin AIDE Lite dispatch, focused tests, generated temp-run reports, and planning/execution/documentation log entries.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/task.yaml`.
- Dependencies: latest intent packet, existing lifecycle fixture plan/expected/rollback files, existing managed-section parser helpers, and the AIDE-APPLY-00 transaction model boundary.
- Milestones: authorized WorkUnit materialized; runner seams implemented; path-jail tests added; status/run/verify commands pass; evidence and generated reports written; root logs updated.
- Blockers: none for this bounded slice. Kernel schemas, service, Commander, provider adapters, branch/worktree automation, target repo mutation, rollback execution, and general lifecycle apply remain out of scope.
- Verification Intent: targeted lifecycle runner tests, existing transaction/managed-section tests, lifecycle-fixture status/run/verify commands, canonical fixture no-diff check, AIDE Lite intent validation, AIDE Lite validate/test, task inspect/evidence, and diff whitespace checks.
- Exit Criteria: task status is `needs_review`, reports truthfully label capability as `fixture_temp_apply_only`, canonical fixtures are unchanged, temp workspace verification passes, and no forbidden operations are performed.
- Notes: The runner uses a marker-bounded full block replacement in the temp workspace because the canonical expected postimage changes marker metadata as well as generated content. This is deliberately not promoted to the general transaction executor in this slice. The attached-prompt alignment pass adds `verify.json` / `verify.md`, future/unfinished-work reports, explicit no-forbidden-ops evidence, and expanded tests without widening execution authority.

### Plan ID: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01

- Title: Lifecycle Fixture Temp Runner Hardening
- Status: needs_review
- Objective: harden the reviewed lifecycle fixture temp runner after CHECK-01 without widening authority.
- Scope: runner verification code, focused lifecycle fixture tests, HARDEN-01 queue evidence, lifecycle fixture runner reports, and root planning/execution logs.
- Allowed Paths: paths listed in `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01/task.yaml`.
- Dependencies: `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01` result `PASS_WITH_WARNINGS`.
- Milestones: queue packet created; verifier hardening added; focused tests expanded; validation run; evidence written; task stopped at review.
- Blockers: none. Broader lifecycle apply, rollback execution, target mutation, service, Commander, providers, branch/worktree, network, Gateway, release, and WorkUnit/TestBroker/Codex-adapter work remain out of scope.
- Verification Intent: focused lifecycle runner tests, existing apply tests, lifecycle-fixture status/run/verify, AIDE Lite validate/test, JSON parse, canonical fixture diff, overclaiming scan, secret scan, and diff whitespace check.
- Exit Criteria: status is `needs_review`, focused tests pass, verifier catches overclaiming and malformed rollback/report evidence, canonical fixtures remain unchanged, and no forbidden operations are introduced.
- Notes: This is hardening of the first vertical slice, not a move to broader primitives.

### Plan ID: AI-LONG-TURN-OPERATING-PROTOCOL-00

- Title: Long-Turn Operating Protocol
- Status: needs_review
- Objective: create docs-only operating protocol material for long-running AIDE and Codex queued turns.
- Scope: queue packet, intake evidence, `docs/planning/ai_long_turn_protocol/**`, and root documentation/planning logs.
- Allowed Paths: paths listed in `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/task.yaml`.
- Dependencies: Q36 intent compiler and Q27 WorkUnit recovery/commit discipline.
- Milestones: compile raw request through intake; split to docs-only WorkUnit; add queue packet; add protocol templates; update indexes; validate; commit if checks pass.
- Blockers: no runtime, branch, publication, target-repo, provider/model, Gateway, network, or external discovery work is authorized by this task.
- Verification Intent: `git diff --check`, AIDE Lite intent validation, task inspect/evidence checks, doctor, validate, and commit check when committed.
- Exit Criteria: status is `needs_review`, protocol docs exist, evidence records validation, and broader blocked operations remain out of scope.
- Notes: The pasted report contained stale `dev`/product state. Live AIDE repo state is authoritative for this plan.

### Plan ID: AIDE-REVIEW-APPLY-00

- Title: Review and Accept Transaction Model Boundary Checkpoint
- Status: needs_review
- Objective: review AIDE-APPLY-00 and AIDE-CHECK-APPLY-00, accept or block the transaction-model boundary checkpoint, classify warnings, and decide readiness for AIDE-APPLY-01.
- Scope: review queue packet, apply-review reports, latest task/review packet refreshes, generated validation reports, and planning/execution log entries.
- Allowed Paths: paths listed in `.aide/queue/AIDE-REVIEW-APPLY-00-transaction-model-review-acceptance/task.yaml`.
- Dependencies: AIDE-APPLY-00 transaction model and AIDE-CHECK-APPLY-00 review checkpoint.
- Milestones: repo identity confirmed; prior evidence inspected; review packet created; warnings classified; validation run; review packet regenerated; structured commit created.
- Blockers: none. AIDE-APPLY-01 implementation, real apply, target mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model/network calls, Gateway forwarding, and install/repair/upgrade/rollback/uninstall apply are out of scope.
- Verification Intent: required AIDE Lite validation, transaction, golden task, pack/release/install/repair/upgrade/rollback/uninstall validator, verify, review-pack, diff, commit, and secret-scan commands.
- Exit Criteria: review task status is `needs_review`, result is `PASS_WITH_WARNINGS`, AIDE-APPLY-01 remains the next task, no apply behavior is introduced, and validation evidence is complete.
- Notes: Stale pre-repair `.aide/reports/aide-apply-00-readiness.md`, generated manifest warning, and dirty pack provenance are classified warnings rather than blockers.

### Plan ID: AIDE-CHECK-APPLY-00

- Title: Transaction Model Review and No-Real-Apply Boundary Audit
- Status: needs_review
- Objective: review AIDE-APPLY-00 transaction model evidence, command surface, docs, reports, export-pack inclusion, and no-real-apply boundary before AIDE-APPLY-01 managed-section patcher planning.
- Scope: queue packet, local apply-check reports, evidence, report-only intake/git/task status refreshes, and planning/execution log entries.
- Allowed Paths: paths listed in `.aide/queue/AIDE-CHECK-APPLY-00-transaction-model-review/task.yaml`.
- Dependencies: AIDE-APPLY-00 transaction model.
- Milestones: queue packet created; AIDE-APPLY-00 evidence reviewed; no-real-apply boundary checked; export-pack inclusion checked; evidence written; validation run; structured commit created.
- Blockers: none. Real apply, managed-section patcher implementation, target mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model/network calls, Gateway forwarding, and install/repair/upgrade/rollback/uninstall apply are out of scope.
- Verification Intent: transaction status/validate, transaction no-real-apply and export-pack goldens, AIDE Lite validate/test/selftest/verify/review-pack, Harness validate, diff check, and targeted secret scan.
- Exit Criteria: checkpoint status is `needs_review`, outcome is `PASS_WITH_NOTES`, no apply behavior is introduced, and AIDE-APPLY-01 remains the next bounded work item.
- Notes: This checkpoint records the existing Harness generated-manifest warning and pack provenance note without treating either as a blocker for managed-section patcher planning.

### Plan ID: X-OS-01

- Title: AIDE Task OS Report-Only Commands
- Status: needs_review
- Objective: implement local report-only `task`, `blocker`, `wave`, and `checkpoint` inspection/planning commands for AIDE Task OS records without apply behavior.
- Scope: X-OS-01 queue packet, AIDE Lite command handlers and validation hooks, `.aide/reports/task-os-*` generated reports, golden tasks, unit tests, reference docs, export-pack sync, evidence, and the latest X-OS-02 task packet.
- Allowed Paths: paths listed in `.aide/queue/X-OS-01-aide-task-os-report-only-commands/task.yaml`.
- Dependencies: X-OS-00 Task OS schemas and policies, Q27/Q28/Q30 task and branch governance, Q31 export pack governance, Q47/Q48 release boundaries, and X-TEST-00 validation tier policy.
- Milestones: queue packet created; report-only commands implemented; reports generated; tests and golden tasks added; docs updated; export pack refreshed; evidence written; structured commit created.
- Blockers: none known at plan creation; target-repo work, branch mutation, GitHub mutation, provider/model calls, network calls, task execution, and repair/checkpoint apply are explicitly out of scope.
- Verification Intent: run AIDE Lite command smoke checks, targeted X-OS-01 unit tests, X-OS-01 golden tasks, `validate`, `test`, `selftest`, export-pack/pack-status checks, diff check, and secret scan.
- Exit Criteria: X-OS-01 status is `needs_review`, command reports exist, validation evidence is written, no apply-capable behavior is introduced, and a structured X-OS-01 commit exists.
- Notes: X-OS-02 should add Capability Reality Ledger v0 records and status surfaces before AIDE-CHECK-OS-01.

### Plan ID: X-OS-00

- Title: AIDE Task OS Schemas and Policies
- Status: needs_review
- Objective: define the Task OS v0 schema and policy layer for WorkUnit lifecycle states, blockers, repair loops, waves, checkpoints, branch provenance, and capability reality before any apply-capable automation exists.
- Scope: X-OS-00 queue packet, Task OS policies, `.aide/tasks` schemas, `.aide/ledgers` schemas, examples, reference docs, reports, golden tasks, AIDE Lite validation registration, tests, latest X-OS-01 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/X-OS-00-aide-task-os-schemas-policies/task.yaml`.
- Dependencies: Q27-Q31 commit/task/Git governance, Q34-Q48 release and no-apply planning surfaces, X-TEST-00 test policy, and AIDE-CONTINUE-00 continuation posture.
- Milestones: queue packet created; schema and policy layer added; examples and docs added; golden tasks and tests added; AIDE Lite validation registered; export pack regenerated; evidence written.
- Blockers: none internal to X-OS-00. X-OS-00 intentionally does not implement a `task-os` command group, worker execution, repair execution, branch mutation, target mutation, provider/model/network calls, merge, promotion, release publication, or apply behavior.
- Verification Intent: AIDE Lite doctor/validate/test/selftest/eval, Task OS targeted unit tests and golden tasks, export-pack, pack-status, release/install/repair/upgrade/rollback/uninstall validators, diff check, and targeted secret scan.
- Exit Criteria: X-OS-00 status reaches `needs_review`, schema/policy/docs/examples/golden tasks exist, validation passes or warnings are classified, evidence is complete, latest task packet points to X-OS-01, and no apply behavior is introduced.
- Notes: X-OS-00 is contract and validation infrastructure only. X-OS-01 is expected to add report-only Task OS commands.

### Plan ID: Q48

- Title: GitHub Release Draft v0
- Status: needs_review
- Objective: generate local, reviewable GitHub Release draft artifacts from the Q47 release bundle without publishing, tagging, uploading, calling GitHub APIs, mutating branches, or claiming target readiness.
- Scope: Q48 queue packet, release draft policies, `.aide/release/github-release-*.schema.json`, AIDE Lite `release draft` commands, release draft golden tasks and tests, docs, Q49 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q48-github-release-draft-v0/task.yaml`.
- Dependencies: Q47 local release bundle artifacts and validation evidence.
- Blockers: none internal to Q48. Q48 intentionally does not implement tag creation, GitHub Release creation, asset upload, package publication, branch mutation, target repo mutation, install/repair/upgrade/rollback/uninstall apply, active CI, GitHub API calls, or provider/model/network calls.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, release validate/status/draft/draft-validate/draft-status/upload-plan/checklist/publication-boundary, export-pack, pack-status, Q48 targeted tests and golden tasks, pack/estimate for Q49, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q48 status reaches `needs_review`, release draft policies/schemas and generated draft outputs exist, assets have checksums, draft validation passes, evidence is complete, and no tag, GitHub Release, upload, branch mutation, GitHub API/network call, active CI, provider/model call, target mutation, or apply behavior occurs.
- Notes: Q48 is local draft generation only. Q49 is still needed before any Dominium target install preflight or release readiness claim.

### Plan ID: Q47

- Title: AIDE Lite Release Bundle v0
- Status: Implemented for review
- Objective: generate a local, downloadable, checksummed AIDE Lite Pack bundle from the validated export pack without publishing, tagging, uploading, or installing into target repositories.
- Scope: Q47 queue packet, release bundle policies, `.aide/release` schemas and local bundle outputs, AIDE Lite `release` commands, release golden tasks and tests, docs, Q48 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q47-aide-lite-release-bundle-v0/task.yaml`.
- Dependencies: Q43 install planning, Q44 repair planning, Q45 upgrade planning, Q46 rollback/uninstall planning, current export pack, changelog preview outputs, and existing pack-status validation.
- Milestones: governance packet created; policies and schemas added; release commands implemented; tests and golden tasks added; docs updated; export pack regenerated; local archives, checksums, manifest, install notes, provenance, and validation reports generated; evidence written.
- Blockers: none internal to Q47. Q47 intentionally does not implement GitHub Release draft, tag creation, upload, package publication, branch mutation, target repo mutation, install/repair/upgrade/rollback/uninstall apply, active CI, or provider/model/network calls.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, install/repair/upgrade/rollback/uninstall validation, export-pack, pack-status, release bundle/validate/status/assets/manifest/checksums/provenance/clean dry-run, Q47 targeted tests and golden tasks, pack/estimate for Q48, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q47 status reaches `needs_review`, release policies/schemas and local bundle artifacts exist, archive extraction and checksum validation pass, evidence is complete, and no tag, GitHub Release, upload, branch mutation, provider/model/network call, target install, or apply behavior occurs.
- Notes: Q47 is local release-bundle generation only. It makes the portable pack downloadable and inspectable, but Q48 is still needed before any GitHub Release draft surface is reviewed.

### Plan ID: QFIX-05

- Title: Release Readiness Warning Reconciliation
- Status: Implemented for review
- Objective: inventory current queue and validation warning state after Q46 and QFIX-04, fix deterministic generated-manifest drift where safe, and record remaining release blockers without claiming production readiness.
- Scope: QFIX-05 queue packet and evidence, generated artifact metadata refresh, branch/readiness evidence, and compact implementation/planning records.
- Allowed Paths: paths listed in `.aide/queue/QFIX-05-release-readiness-warning-reconciliation/task.yaml`.
- Dependencies: current queue index, generated artifact compiler, Harness validation, AIDE Lite validation, and QFIX-04 performance hotfix commit.
- Milestones: baseline warning inventory completed; QFIX-05 packet created; generated artifact state refreshed; validation rerun; evidence written; structured commit created.
- Blockers: review-gated Q36-Q47 and QFIX-04 block public-release claims until reviewed; Q48 release draft remains future work.
- Verification Intent: `git diff --check`, `scripts/aide compile --dry-run`, `scripts/aide validate`, AIDE Lite validate/task status/pack-status, and commit check.
- Exit Criteria: deterministic generated-manifest warning is removed or documented, QFIX-05 status ends at `needs_review`, evidence is complete, and no release publication, tag, branch push, target mutation, provider/model/network call, or review-gate bypass occurs.
- Notes: This is a readiness cleanup pass, not a release certification.

### Plan ID: Q46

- Title: Rollback / Uninstall Model v0
- Status: Implemented for review
- Objective: define deterministic rollback and uninstall observation, preservation-first planning, dry-run summaries, ownership-evidence gates, and verification plans before any future rollback apply, uninstall apply, or release bundle phase.
- Scope: Q46 queue packet, rollback and uninstall policies, `.aide/rollback` and `.aide/uninstall` schemas and generated no-apply artifacts, AIDE Lite `rollback` and `uninstall` commands, golden tasks, tests, docs, Q47 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q46-rollback-uninstall-model-v0/task.yaml`.
- Dependencies: Q43 install ownership and preservation rules, Q44 repair plans, Q45 upgrade plans, current export pack, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; rollback/uninstall commands implemented; tests and golden tasks added; docs updated; no-apply rollback/uninstall artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q46. Q46 intentionally does not implement rollback apply, uninstall apply, install/repair/upgrade apply, release bundles, target mutation, deletion, overwrites, managed-section removal, file moves, or reference rewrites.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, install/repair/upgrade validation, rollback observe/plan/dry-run/validate/status/classes/explain, uninstall observe/plan/dry-run/validate/status/classes/explain, Q46 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q47, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q46 status reaches `needs_review`, rollback/uninstall policies/schemas and no-apply artifacts exist, pack-status passes, evidence is complete, and no rollback apply, uninstall apply, delete, overwrite, managed-section removal, source-state replacement, target-repo mutation, branch mutation, provider/model/network call, or source-generated rollback/uninstall plan export occurs.
- Notes: Q46 is rollback/uninstall planning infrastructure only. It makes future target removal and recovery reviewable and reversible, but Q47 is still a release-bundle planning phase, not apply authorization.

### Plan ID: Q45

- Title: Upgrade Model v0
- Status: Implemented for review
- Objective: define deterministic current-install observation, source-pack observation, compatibility comparison, no-apply upgrade plans, dry-run summaries, conflict reports, migration reports, and verification plans before any future upgrade apply, rollback, or uninstall phase.
- Scope: Q45 queue packet, upgrade policies, `.aide/upgrade` schemas and generated no-apply artifacts, AIDE Lite `upgrade` commands, golden tasks, tests, docs, Q46 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q45-upgrade-model-v0/task.yaml`.
- Dependencies: Q43 install observation and preservation rules, Q44 repair diagnosis and safety gates, current export pack, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; upgrade commands implemented; tests and golden tasks added; docs updated; no-apply upgrade artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q45. Q45 intentionally does not implement upgrade apply, install apply, repair apply, rollback/uninstall apply, release bundles, target mutation, overwrites, deletions, automatic migrations, file moves, or reference rewrites.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, install and repair validation, upgrade observe-current/observe-source/compare/plan/dry-run/validate/status/compatibility/conflicts/migrations/explain, Q45 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q46, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q45 status reaches `needs_review`, upgrade policies/schemas and no-apply artifacts exist, pack-status passes, evidence is complete, and no upgrade apply, overwrite, delete, migration apply, source-state replacement, target-repo mutation, branch mutation, provider/model/network call, or source-generated upgrade plan export occurs.
- Notes: Q45 is upgrade planning infrastructure only. It makes future target updates reviewable and reversible, but Q46 and later apply-capable phases must authorize rollback/uninstall and any concrete target action separately.

### Plan ID: Q44

- Title: Repair / Doctor Model v0
- Status: Implemented for review
- Objective: define deterministic repair observation, diagnosis, repair classes, no-apply repair plans, dry-run summaries, doctor repair reports, and verification plans before any future repair apply, upgrade, rollback, or uninstall phase.
- Scope: Q44 queue packet, repair/doctor policies, `.aide/repair` schemas and generated no-apply artifacts, AIDE Lite `repair` commands, golden tasks, tests, docs, Q45 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q44-repair-doctor-model-v0/task.yaml`.
- Dependencies: Q43 install observation, preservation, ownership, conflict, and verification plans; current export pack; and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; repair commands implemented; tests and golden tasks added; docs updated; no-apply repair artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q44. Q44 intentionally does not implement repair apply, install apply, upgrade apply, rollback/uninstall apply, release bundles, target mutation, overwrites, deletions, automatic migrations, file moves, or reference rewrites.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, install validation, repair observe/diagnose/plan/dry-run/validate/status/classes/doctor/explain, Q44 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q45, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q44 status reaches `needs_review`, repair policies/schemas and no-apply artifacts exist, pack-status passes, evidence is complete, and no repair apply, overwrite, delete, migration apply, source-state replacement, target-repo mutation, branch mutation, provider/model/network call, or source-generated repair plan export occurs.
- Notes: Q44 is repair planning infrastructure only. It makes future target repair and upgrade work reviewable and reversible, but Q45 and later apply-capable phases must authorize any concrete target action separately.

### Plan ID: Q43

- Title: Install Plan Model v0
- Status: Implemented for review
- Objective: define deterministic install observation, preservation-first install plans, dry-run summaries, ownership ledgers, conflict reports, and verification plans before any future install apply, repair, upgrade, rollback, or uninstall phase.
- Scope: Q43 queue packet, install policies, `.aide/install` schemas and generated no-apply artifacts, AIDE Lite `install` commands, golden tasks, tests, docs, Q44 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q43-install-plan-model-v0/task.yaml`.
- Dependencies: Q37 repo intelligence, Q38 quality, Q39 refactor control, Q40 root recycling, Q41 tool absorption, Q42 map/alias planning, current export pack, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; install commands implemented; tests and golden tasks added; docs updated; no-apply install artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q43. Q43 intentionally does not implement install apply, repair apply, upgrade apply, rollback/uninstall apply, release bundles, target mutation, overwrites, automatic migrations, file moves/deletes, or reference rewrites.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo/quality/refactor/roots/tools/map validation, install observe/plan/dry-run/validate/status/ownership/conflicts/explain, Q43 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q44, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q43 status reaches `needs_review`, install policies/schemas and no-apply artifacts exist, pack-status passes, evidence is complete, and no install apply, overwrite, migration apply, source-state leak, target-repo mutation, branch mutation, provider/model/network call, or source-generated install plan export occurs.
- Notes: Q43 is install planning infrastructure only. It makes future target install, repair, upgrade, rollback, and uninstall work reviewable and reversible, but Q44 and later apply-capable phases must authorize any concrete target action separately.

### Plan ID: Q42

- Title: Move Map / Salvage Map / Path Alias v0
- Status: Implemented for review
- Objective: define deterministic candidate move maps, salvage maps, path alias plans, reference rewrite plans, and draft migration ledger events before any future structural apply phase.
- Scope: Q42 queue packet, map/alias/rewrite/ledger policies, `.aide/refactors` schemas and generated candidate artifacts, AIDE Lite `refactor map` commands, golden tasks, tests, docs, Q43 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/task.yaml`.
- Dependencies: Q37 repo intelligence, Q38 file quality, Q39 refactor control, Q40 root recycling, Q41 tool absorption, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; map commands implemented; tests and golden tasks added; docs updated; candidate maps generated; export pack regenerated; evidence written.
- Blockers: none internal to Q42. Q42 intentionally does not implement file moves, salvage extraction, alias/shim creation, reference rewriting, concrete Dominium/Eureka migration, tool migration, install/upgrade/rollback, or apply behavior.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/validate, quality ledger/validate, refactor validate/map/move-map/salvage-map/aliases/rewrite-plan/validate-map/map-status, roots inventory/validate, tools inventory/validate, Q42 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q43, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q42 status reaches `needs_review`, map/alias policies and schemas exist, current candidate map artifacts exist, pack-status passes, evidence is complete, and no file move/delete/reference rewrite, alias/shim application, target-repo mutation, branch mutation, provider/model/network call, or source-generated current map export occurs.
- Notes: Q42 is candidate planning infrastructure only. It makes future install, root recycling, tool absorption, and migration work reviewable and reversible, but Q43 and later apply-capable phases must authorize any concrete structural action separately.

### Plan ID: Q41

- Title: Existing Tool Absorption v0
- Status: Implemented for review
- Objective: define deterministic no-execution existing-tool inventory, capability classification, preservation fates, risk summaries, adapter maps, and future wrap plans before any tool deletion, rename, migration, wrapper execution, or target-repo absorption.
- Scope: Q41 queue packet, tool absorption policies, `.aide/tools` schemas and generated advisory artifacts, AIDE Lite `tools` commands, golden tasks, tests, docs, Q42 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q41-existing-tool-absorption-v0/task.yaml`.
- Dependencies: Q37 repo intelligence outputs, Q38 file quality ledger outputs, Q39 no-apply refactor controls, Q40 root recycling outputs, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; tools commands implemented; tests and golden tasks added; docs updated; no-execution tool artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q41. Q41 intentionally does not implement concrete Dominium XStack absorption, Eureka validator absorption, active wrappers, tool deletion, tool rename, tool migration, current move maps, salvage maps, path aliases, or install/upgrade/rollback behavior.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/validate, quality ledger/validate, refactor validate, roots inventory/validate, tools inventory/classify/wrap-plan/validate/status/capabilities/explain-tool, Q41 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q42, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q41 status reaches `needs_review`, tool policies/schemas and no-execution artifacts exist, pack-status passes, evidence is complete, and no unknown tool execution, deletion, rename, migration, wrapper apply, target-repo mutation, branch mutation, provider/model/network call, or source-generated tool output export occurs.
- Notes: Q41 is planning infrastructure only. It makes future tool absorption reviewable and reversible, but Q42 and later apply-capable phases must authorize any concrete structural mapping, wrapper execution, migration, or retirement separately.

### Plan ID: Q40

- Title: Root Recycling Framework v0
- Status: Implemented for review
- Objective: define deterministic no-apply root inventory, root classification, file fate, root risk, exception, and root recycling planning before any future root move, file delete, reference rewrite, tool absorption, migration, install, upgrade, or rollback phase.
- Scope: Q40 queue packet, root recycling policies, root schemas under `.aide/refactors`, generated `.aide/roots` inventory/classification/plan artifacts, AIDE Lite `roots` commands, golden tasks, tests, docs, Q41 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q40-root-recycling-framework-v0/task.yaml`.
- Dependencies: Q37 repo intelligence outputs, Q38 file quality ledger outputs, Q39 no-apply refactor controls, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; roots commands implemented; tests and golden tasks added; docs updated; no-apply root artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q40. Q40 intentionally does not implement Q41 Existing Tool Absorption, concrete target-root recycling, current move maps, salvage maps, path alias application, or refactor apply.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/validate, quality ledger/validate, refactor validate, roots inventory/classify/plan/validate/status/explain-root/explain-file, Q40 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q41, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q40 status reaches `needs_review`, root policies/schemas and no-apply artifacts exist, pack-status passes, evidence is complete, and no root move/delete, file move/delete, reference rewrite, apply behavior, tool absorption, target-repo mutation, branch mutation, provider/model/network call, or source-generated root output export occurs.
- Notes: Q40 is planning infrastructure only. It makes future root cleanup reviewable and reversible, but Q41/Q42 and later apply-capable phases must authorize any concrete structural action separately.

### Plan ID: Q39

- Title: Refactor Control Plane v0
- Status: Implemented for review
- Objective: define deterministic no-apply refactor and migration planning before any future structural move, delete, rewrite, migration, install, upgrade, rollback, or root recycling phase.
- Scope: Q39 queue packet, refactor and migration policies, safety/evidence/application policies, `.aide/refactors` schemas and generated readiness/example artifacts, AIDE Lite `refactor` commands, golden tasks, tests, docs, Q40 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q39-refactor-control-plane-v0/task.yaml`.
- Dependencies: Q37 repo intelligence outputs, Q38 file quality ledger outputs, and existing no-call AIDE Lite governance surfaces.
- Milestones: governance packet created; policies and schemas added; refactor commands implemented; tests and golden tasks added; docs updated; no-apply readiness/example artifacts generated; export pack regenerated; evidence written.
- Blockers: none internal to Q39. Q39 intentionally does not implement Q40 Root Recycling Framework, tool absorption, concrete current move maps, path alias application, or refactor apply.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/validate, quality ledger/validate, refactor status/plan/validate/dry-run/schemas/ledger, Q39 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q40, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q39 status reaches `needs_review`, refactor policies/schemas and readiness artifacts exist, pack-status passes, evidence is complete, and no file move/delete/reference rewrite, apply behavior, target-repo mutation, branch mutation, provider/model/network call, or source-generated refactor plan export occurs.
- Notes: Q39 is planning infrastructure only. It makes future refactors reviewable and reversible, but Q40/Q41/Q42 and later apply-capable phases must authorize any concrete structural action separately.

### Plan ID: Q38

- Title: File Quality Ledger v0
- Status: Implemented for review
- Objective: generate deterministic advisory file quality records from Q37 repo intelligence for ownership, docs, tests, validators, stale docs, generated/evidence boundaries, orphan candidates, module hints, and reuse candidates.
- Scope: Q38 queue packet, quality policies, schemas, AIDE Lite `quality` commands, generated `.aide/reports/file-quality-*` reports, golden tasks, tests, docs, Q39 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q38-file-quality-ledger-v0/task.yaml`.
- Dependencies: Q37 repo intelligence outputs and existing no-call AIDE Lite validation surfaces.
- Milestones: governance packet created; policies and schemas added; quality commands implemented; tests and golden tasks added; docs updated; quality reports generated; export pack regenerated; evidence written.
- Blockers: none internal to Q38. Baseline pack checksums were invalid at task start and are repaired by Q38 export-pack sync.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/validate/status, quality ledger/validate/status/explain/docs/tests/modules/reuse, Q38 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q39, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q38 status reaches `needs_review`, quality outputs exist, pack-status passes, evidence is complete, and no file move/delete/refactor, automatic source/doc/test fix, target-repo mutation, branch mutation, provider/model/network call, or source-generated quality report export occurs.
- Notes: Q38 is advisory measurement only. It does not implement Q39 Refactor Control Plane, root recycling, tool absorption, install/upgrade/rollback, or target sync.

### Plan ID: Q37

- Title: Repo Intelligence Index v0
- Status: Implemented for review
- Objective: generate deterministic repo-local indexes for file inventory, ownership, dependencies, tests, documentation links, generated outputs, and conservative orphan candidates.
- Scope: Q37 queue packet, repo-intelligence policies, schemas, AIDE Lite `repo` commands, generated `.aide/repo` indexes, golden tasks, tests, docs, evidence, Q38 task packet, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q37-repo-intelligence-index-v0/task.yaml`.
- Dependencies: Q36 intent compiler and existing no-call AIDE Lite validation surfaces.
- Milestones: governance packet created; policies and schemas added; repo commands implemented; classification/map tests and golden tasks added; docs updated; repo indexes generated; export pack regenerated; evidence written.
- Blockers: none internal to Q37. Unknown files and orphan candidates remain conservative inputs for Q38/Q39, not deletion decisions.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, repo inventory/classify/validate/status/explain-file/docs/tests/deps, Q37 targeted tests and golden tasks, intent validation, export-pack, pack-status, pack/estimate for Q38, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q37 status reaches `needs_review`, repo intelligence outputs exist, pack-status passes, evidence is complete, and no file move/delete/refactor, target-repo mutation, branch mutation, provider/model/network call, or source-generated repo index export occurs.
- Notes: Q37 is index-only. It does not implement Q38 File Quality Ledger, refactor control, root recycling, tool absorption, install/upgrade/rollback, or target sync.

### Plan ID: Q35

- Title: GitHub Protection and CI Advisory v0
- Status: Implemented as report-only advisory
- Objective: define GitHub branch-protection and CI gate posture from repo-local evidence without applying settings or creating workflow files.
- Scope: Q35 queue packet, GitHub/CI policies, `.aide/github` advisory reports, AIDE Lite `github` commands, tests, golden tasks, docs, export-pack sync, and Q36 packet preparation.
- Allowed Paths: paths listed in `.aide/queue/Q35-github-protection-ci-advisory-v0/task.yaml`.
- Dependencies: Q27 commit discipline, Q28-Q30 Git workflow policy/helper state, Q31 export pack, and Q34 changelog preview.
- Milestones: policies added; command family implemented; generated advisory reports written; tests/golden tasks added; docs and pack refreshed; validation run.
- Blockers: none internal to Q35 after validation.
- Verification Intent: AIDE Lite validate/test/selftest/eval, GitHub advisory commands, export-pack, pack-status, commit check, changelog validate, Git policy, Harness validate/doctor/self-check, core unittest suites, and secret scan.
- Exit Criteria: GitHub command family passes, advisory reports are present, pack-status passes, and no GitHub API, workflow, branch, tag, release, provider, model, or network mutation occurs.
- Notes: Active GitHub protection and CI workflow installation remain deferred to a future reviewed apply-capable phase.

### Plan ID: Q36

- Title: Intent Compiler and Prompt Normalization v0
- Status: Implemented for review
- Objective: compile vague, broad, repeated, unsafe, target-repo, Git, release, install, and repair prompts into bounded repo-grounded intent packets and WorkUnit drafts without executing the resulting task.
- Scope: Q36 queue packet, intent and prompt-normalization policies, WorkUnit sizing policy, task/risk class policy, intake schemas/examples, AIDE Lite `intent` commands, latest generated intent artifacts, golden tasks, tests, docs, evidence, and export-pack sync.
- Allowed Paths: paths listed in `.aide/queue/Q36-intent-compiler-prompt-normalization-v0/task.yaml`.
- Dependencies: Q35.
- Milestones: governance packet created; policies and schemas added; deterministic classifier implemented; golden tasks and tests added; docs updated; Q37 task packet generated; export pack regenerated; evidence written.
- Blockers: none internal to Q36. Classification remains heuristic until Q37 adds a Repo Intelligence Index.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/eval, intent compile/validate/examples/status, Q36 targeted tests and golden tasks, export-pack, pack-status, pack/estimate for Q37, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q36 status reaches `needs_review`, latest intent packet and WorkUnit draft exist, pack-status passes, evidence is complete, and no raw prompt execution, provider/model/network calls, target-repo mutation, branch mutation, or compiled WorkUnit execution occurs.
- Notes: Q36 is compile-only. It does not implement Q37 Repo Intelligence Index, File Quality Ledger, refactor control, install/upgrade/rollback, release publishing, Gateway forwarding, or target sync.

### Plan ID: QFIX-03

- Title: Warning And Review Reconciliation
- Status: Implemented and accepted with notes
- Objective: resolve fixable post-Q34 validation warnings and review blockers without rewriting history, publishing releases, mutating remotes, calling providers/models, or changing target repos.
- Scope: generated manifest refresh, queue review-state reconciliation, changelog warning classification, validation evidence, and root documentation status cleanup.
- Allowed Paths: paths listed in `.aide/queue/QFIX-03-warning-review-reconciliation/task.yaml`.
- Dependencies: Q34 final state and existing task-local evidence for the review-gated queue items.
- Milestones: warning inventory completed; generated-manifest drift fixed; eligible review gates reconciled; validation rerun; evidence written.
- Blockers: none remaining in AIDE-local queue state after reconciliation.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite validate/test/selftest/eval, commit checks, changelog preview/validate/status, pack export/status, core unittest suites, and secret scan.
- Exit Criteria: all fixable AIDE-local warnings are removed or converted to explicit findings, queue status no longer contains stale review blockers, and no forbidden product/release/network/target-repo actions occur.
- Notes: Q32/Q33 remain target-repository sync prompts and were not run from the AIDE repository.

### Plan ID: Q34

- Title: Changelog and Release Notes Generator v0
- Status: Accepted with notes by QFIX-03
- Objective: compile structured AIDE commits into deterministic preview-only changelog and release-note Markdown/JSON drafts.
- Scope: Q34 queue packet, changelog policy/config/templates, AIDE Lite `changelog preview/validate/status`, generated preview outputs, malformed commit report, Q34 golden tasks, tests, docs, export-pack sync, and Q35 task packet.
- Allowed Paths: Q34 paths listed in `.aide/queue/Q34-changelog-release-notes-generator-v0/task.yaml`.
- Dependencies: Q27 structured commit discipline, Q31 portable governance export, and existing no-call AIDE Lite validation.
- Milestones: governance packet created; parser/generator implemented; tests and golden tasks added; docs updated; pack regenerated; Q35 packet generated; evidence written.
- Blockers: none internal to Q34; older history remains reported as malformed/legacy findings instead of rewritten.
- Verification Intent: AIDE Lite validate/test/selftest/eval, commit latest/range checks, changelog preview/validate/status, Git detect/plan, export-pack, pack-status, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q34 status is accepted with notes, preview Markdown/JSON files exist, malformed history is reported, pack-status passes, and no tags, GitHub Releases, publishing, branch mutation, provider/model calls, or network calls occur.
- Notes: Q34 creates release drafts only. It does not promote official release notes, infer SemVer bumps, create tags, publish packages, activate CI, or call GitHub APIs.

### Plan ID: Q31

- Title: Export Pack Sync for Git / Commit Workflow
- Status: Accepted with notes by QFIX-03
- Objective: make the portable `aide-lite-pack-v0` carry Q27-Q30 commit discipline, WorkUnit recovery, changelog, Git workflow, and dry-run helper governance without exporting AIDE source-repo state.
- Scope: Q31 queue packet, export/import policy metadata, AIDE Lite export/import validation, Q31 golden tasks, fixture import tests, portable docs, regenerated pack metadata, and Q32 task packet.
- Allowed Paths: Q31 paths listed in `.aide/queue/Q31-export-pack-sync-git-commit-workflow/task.yaml`.
- Dependencies: Q27 commit discipline and recovery, Q28 Git workflow policy, Q29 dry-run helper behavior, and Q30 AIDE branch posture.
- Milestones: governance packet created; export/import include and exclude classes updated; Q31 golden tasks added; fixture import governance tests added; docs/evidence updated; pack regenerated and validated.
- Blockers: none internal to Q31; Eureka and Dominium still need explicit target sync phases.
- Verification Intent: AIDE Lite validate/test/selftest/eval, Q31 fixture import tests, commit check, changelog preview, Git detect/policy/plan, export-pack, pack-status, core unittest suites, diff check, and secret scan.
- Exit Criteria: Q31 status is accepted with notes, pack-status passes, fixture import can run commit/task/Git governance commands, hook installation remains opt-in, and Q32 task packet is regenerated.
- Notes: Q31 exports portable governance capabilities only. It does not sync target repos, mutate branches, install hooks, activate CI, call GitHub, or export AIDE-specific generated Git reports.

### Plan ID: Q30

- Title: AIDE Dev/Main Policy Sync
- Status: Accepted with notes by QFIX-03
- Objective: make AIDE's own branch posture explicit by recording `main` as canonical truth, `dev` as integration truth, and future dev setup or promotion as helper-planned operator actions only.
- Scope: Q30 queue packet, AIDE-specific branch policy, dev/main plan artifacts, AIDE Lite Git policy/plan integration, Q30 golden tasks and tests, docs, generated branch plans, and export-pack sync.
- Allowed Paths: Q30 paths listed in `.aide/queue/Q30-aide-dev-main-policy-sync/task.yaml`.
- Dependencies: Q27 commit discipline, Q28 Git workflow policy, and Q29 dry-run Git helper behavior.
- Milestones: governance packet created; AIDE branch policy added; dev/main plan generated from current branch state; AIDE Lite Git plan/policy commands hardened; Q30 golden tasks and tests added; docs/evidence/export pack updated.
- Blockers: no internal blocker; local and remote `dev` are absent, so creation remains a future explicit operator action and was not run in Q30.
- Verification Intent: AIDE Lite validate/test/selftest/eval, Git policy/plan/dry-runs, Q30 targeted tests, export-pack, pack-status, core unittest suites, commit checks, changelog preview, diff check, and secret scan.
- Exit Criteria: Q30 status is accepted with notes with evidence complete, live branch no-mutation recorded, pack-status passing, and Q31 task packet regenerated.
- Notes: Q30 does not create, push, merge, delete, prune, or promote live branches. `dev` is integration truth only and never canonical release truth.

### Plan ID: Q29

- Title: Merge / Land / Promote Helper v0
- Status: Accepted with notes by QFIX-03
- Objective: add dry-run-first Git helper commands for sync planning, task-to-dev landing, dev-to-main promotion planning, and prune guards without mutating live AIDE branches.
- Scope: Q29 queue packet, helper policy/docs, AIDE Lite `git plan/sync/land/promote/prune`, fixture-only mutation tests, Q29 golden tasks, docs, current helper plans, and export-pack sync.
- Allowed Paths: Q29 paths listed in `.aide/queue/Q29-merge-land-promote-helper-v0/task.yaml`.
- Dependencies: Q27 commit discipline and Q28 Git workflow policy.
- Milestones: governance packet reopened; helper policy and commands added; fixture land/promote/prune tests added; golden tasks added; docs and evidence updated; export pack regenerated.
- Blockers: none internal to Q29; live AIDE `dev` creation/sync and GitHub protection remain future phases.
- Verification Intent: AIDE Lite validate/test/selftest/eval, Git helper dry-runs, Q29 fixture tests, export-pack, pack-status, core unittest suites, commit checks, changelog preview, and secret scan.
- Exit Criteria: Q29 status is accepted with notes with live repo no-mutation evidence, fixture mutation evidence, and Q30 task packet regenerated.
- Notes: Q29 implements local helper plans and explicit `--apply` paths, but Q29 validation does not run `--apply` on the live AIDE repository and never runs `--push`.

### Plan ID: Q28

- Title: Git Workflow Policy v0
- Status: Accepted with notes by QFIX-03
- Objective: define AIDE branch roles, workflow detection, sync, promotion, and prune policy without mutating branches or remotes.
- Scope: Q28 queue packet, Git workflow policy files, branch role docs, report-only AIDE Lite `git` commands, workflow detection artifacts, golden tasks, tests, docs, and export-pack sync.
- Allowed Paths: Q28 paths listed in `.aide/queue/Q28-git-workflow-policy-v0/task.yaml`.
- Dependencies: Q27 commit discipline and WorkUnit recovery.
- Milestones: governance packet reopened; branch/promotion/sync/prune policies added; report-only detection commands added; golden tasks and tests added; docs and evidence updated; export pack regenerated.
- Blockers: none internal to Q28; live branch mutation, GitHub protection, and merge/land/promote helpers remain deferred.
- Verification Intent: AIDE Lite validate/test/selftest/eval, `git detect/doctor/status/roles/policy`, Q28 targeted tests, export-pack, pack-status, core unittest suites, and secret scan.
- Exit Criteria: Q28 status is accepted with notes with evidence complete and Q29 task packet regenerated.
- Notes: Q28 explicitly does not create, delete, merge, push, prune, fetch, or modify branch protection.

### Plan ID: Q27

- Title: Commit Discipline And WorkUnit Recovery v0
- Status: Accepted with notes by QFIX-03
- Objective: make future AIDE work changelog-ready, replay-safe, resumable, and recoverable from repo-local evidence.
- Scope: Q27 queue packet, commit/task/recovery policies, AIDE Lite command surface, golden tasks, tests, docs, generated changelog previews, and export-pack sync.
- Allowed Paths: Q27 paths listed in `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/task.yaml`.
- Dependencies: Q25 repaired pack/import state and Q26 handover checkpoint.
- Milestones: policy layer added; commit/changelog/task commands added; golden tasks and tests added; docs and evidence updated; export pack regenerated.
- Blockers: none internal to Q27; old pre-Q27 commit history remains reported rather than rewritten.
- Verification Intent: AIDE Lite validate/test/selftest/eval, commit latest/range checks, changelog preview, task inspect/noop/status, export-pack, pack-status, core unittest suites, and secret scan.
- Exit Criteria: Q27 status is accepted with notes with evidence complete and Q28 task packet regenerated.
- Notes: Q27 does not implement branch workflow helpers, CI, release publishing, provider/model calls, or product runtime work.

### Plan ID: P00

- Title: AIDE repository constitution and operating law
- Status: Completed
- Objective: establish the root operating law, governance policies, and root planning and documentation templates
- Scope: `README.md`, root control-plane files, and `governance/` policy documents only
- Allowed Paths: `README.md`, `AGENTS.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `governance/vision.md`, `governance/support-policy.md`, `governance/naming-policy.md`, `governance/capability-levels.md`, `governance/release-policy.md`
- Dependencies: existing bootstrap control-plane commit `f2b4e72`
- Milestones: inspect current root docs; draft consistent governance set; verify conceptual anchors and required files; checkpoint a commit
- Blockers: none
- Verification Intent: file existence checks plus `rg` checks for required policy anchors and terminology
- Exit Criteria: all required files exist, the policy set is internally consistent, and verification passes
- Notes: governance only; no product implementation, inventory system, adapter code, packaging, CI, or environments in this prompt; conceptual-anchor verification passed

### Plan ID: P06

- Title: Shared-core architecture and host-adapter contract system
- Status: Completed
- Objective: define the canonical shared-core architecture, host-adapter contract, execution-mode model, and conservative shared schemas for later implementation prompts
- Scope: `specs/**`, `shared/**`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `specs/**`, `shared/**`
- Dependencies: P00 governance law, P01 inventory and matrices, P03 through P05 host-atlas research, and the existing host-lane scaffold under `hosts/**`
- Milestones: architecture narratives created under `specs/architecture/`; shared subtree scaffold created under `shared/`; machine-readable shared schemas created under `shared/schemas/`; root planning and documentation indexes updated to record the milestone
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for core contract terms and execution modes, and an allowed-path audit over the git diff
- Exit Criteria: architecture docs exist and are internally consistent, shared subtree directories and schema placeholders exist, planning or documentation indexes are updated, and verification passes
- Notes: architectural only; executable shared-core logic, host-adapter implementation, packaging, CI, environments, and eval wiring remain deferred

### Plan ID: P07

- Title: Environment, lab, and acquisition framework
- Status: Completed
- Objective: define the environment and lab control plane for acquisition, media provenance, bring-up status, snapshots, blockers, and archival tracking
- Scope: `environments/**`, `labs/**`, `inventory/legal-acquisition.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `inventory/legal-acquisition.yaml`, `environments/**`, `labs/**`
- Dependencies: P00 governance law, P01 inventory and matrices, P06 architecture contracts, and the existing placeholder `environments/` and `labs/` directories
- Milestones: environment model and acquisition policy docs created; environment subtree scaffold and machine-readable catalogs created; lab workflow and registers created; root planning and documentation indexes updated to record the phase
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for environment and acquisition vocabulary, and an allowed-path audit over the git diff
- Exit Criteria: environment and lab frameworks exist and are internally consistent, acquisition/legal posture is machine-readable, catalogs and registers are structurally coherent, and verification passes
- Notes: framework only; no actual media acquisition, environment bring-up, snapshots, proprietary assets, or runnable environment claims are introduced in this prompt

### Plan ID: P08

- Title: Evaluation, verification, packaging, and release framework
- Status: Completed
- Objective: define the control plane for evaluation models, verification routines, graders, packaging posture, artifact classes, release channels, and release-shape tracking
- Scope: `evals/**`, `packaging/**`, `matrices/test-matrix.yaml`, `matrices/packaging-matrix.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `evals/**`, `packaging/**`, `matrices/test-matrix.yaml`, `matrices/packaging-matrix.yaml`
- Dependencies: P00 governance law, P01 inventory and seed matrices, P06 shared-core architecture, P07 environment and lab framework, and existing host-lane and research records
- Milestones: evaluation model and strategy docs created; eval subtree scaffold and catalogs created; packaging model and policy docs created; packaging subtree scaffold and catalogs created; test and packaging matrices refined from placeholders into planning frameworks; root planning and documentation indexes updated to record the phase
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for evaluation and packaging vocabulary, and an allowed-path audit over the git diff
- Exit Criteria: eval and packaging frameworks exist and are internally consistent, machine-readable catalogs and registers are structurally coherent, matrices are meaningfully refined, and verification passes
- Notes: framework only; no executable tests, graders, packaging automation, manifests with real shipping content, release binaries, or CI workflows are introduced in this prompt

### Plan ID: P09

- Title: Cross-host boot-slice specification and oldest-first rollout plan
- Status: Completed
- Objective: define the first implementation slice, lane-by-lane acceptance criteria, degraded or blocked handling, and an oldest-first rollout structure aligned to the research corpus
- Scope: `specs/boot-slice/**`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `specs/boot-slice/**`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`
- Dependencies: P00 through P08, especially host-atlas research, capability matrices, shared-core contract architecture, and evaluation framework documents
- Milestones: boot-slice specification set created; machine-readable boot-slice and rollout manifests created; feature and test matrices refined for the first slice; eval catalog and verification definitions refined for boot-slice planning; root planning and documentation indexes updated
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for boot-slice and rollout vocabulary, lane-id checks against the rollout manifest, and an allowed-path audit over the git diff
- Exit Criteria: the boot-slice specification exists and is internally consistent, the rollout plan covers all committed lanes, degraded or blocked handling is explicit, matrices and eval catalogs are meaningfully refined, and verification passes
- Notes: specification only; no shared-core logic, host-adapter implementation, CI, or runtime eval results are introduced in this prompt

### Plan ID: P10

- Title: Shared-core boot-slice implementation
- Status: Completed
- Objective: implement the shared-core portion of the first boot slice, including deterministic request and response handling, capability reporting, unavailable or deferred reporting, and a host-agnostic CLI bridge
- Scope: `shared/**`, `fixtures/**`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `shared/**`, `fixtures/**`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P06 shared-core architecture, P08 evaluation framework, P09 boot-slice specification, and the existing shared schema set under `shared/schemas/**`
- Milestones: implement the minimal shared-core runtime and CLI bridge; add deterministic boot-slice request or response fixtures; add standard-library tests for dispatch and CLI smoke; record eval definitions and a run record for the shared-core slice; update root planning and documentation indexes
- Blockers: none
- Verification Intent: executable verification, using file existence checks, `py -3 -m unittest discover -s shared/tests -t .`, direct `py -3 -m shared.cli` smoke invocation against fixtures, anchor checks for core contract vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: the shared-core boot slice is implemented, tests pass, the CLI smoke case passes, capability and unavailable or deferred reporting are present, fixtures and eval records exist, and verification passes
- Notes: bootstrap runtime choice is pure Python 3 with the standard library only; host adapters, local-service daemons, packaging flows, and later capabilities remain deferred

### Plan ID: P11

- Title: Microsoft host boot-slice implementations
- Status: Completed
- Objective: implement the Microsoft host-family side of the first boot slice using thin lane-local artifacts that reuse the shared-core CLI bridge where honest and explicit blocked records where native proof is not yet reproducible
- Scope: `hosts/microsoft/**`, Microsoft-related matrix rows, Microsoft eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/microsoft/**`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P03 Microsoft ecosystem atlas, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic runtime fixtures, and the existing Microsoft lane scaffold under `hosts/microsoft/**`
- Milestones: implement runnable degraded cli-bridge proofs for feasible Microsoft lanes; add explicit blocked-proof artifacts for native archival or embedded lanes that cannot be verified honestly here; refine Microsoft support, capability, feature, and test matrices to match actual proof posture; record Microsoft eval status and a phase run log; update root planning and documentation indexes
- Blockers: no reproducible VSSDK-capable Visual Studio environment for `vsix-v2-vssdk`; no reproducible Visual Studio for Mac archival environment for `monodevelop-addin`
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocations for runnable Microsoft lanes, structural blocked-proof checks for non-runnable lanes, anchor checks for Microsoft boot-slice vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every Microsoft lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; Microsoft matrices and eval records match actual outcomes; and verification passes
- Notes: P11 stays Microsoft-only and does not claim Apple or CodeWarrior host success; `local-service` remains deferred even for the modern extensibility lane

### Plan ID: P12

- Title: Apple host boot-slice implementations
- Status: Completed
- Objective: implement the Apple host-family side of the first boot slice using a runnable thin companion proof and an explicit blocked structural XcodeKit proof that keeps the native editor target visible without inventing macOS or Xcode runtime success
- Scope: `hosts/apple/**`, Apple-related matrix rows, Apple eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/apple/**`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P04 Apple ecosystem atlas, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic runtime fixtures, and the existing Apple lane scaffold under `hosts/apple/**`
- Milestones: implement a runnable `cli-bridge` companion proof; add explicit blocked structural records for the required native `xcodekit` lane; refine Apple support, capability, feature, and test matrices to match actual proof posture; record Apple eval status and a phase run log; update root planning and documentation indexes
- Blockers: no reproducible macOS or Xcode environment for `xcodekit`; no verified containing-app or extension packaging flow for the `xcodekit` lane; no verified embedded Swift or XcodeKit bridge to the shared-core runtime under current prompt scope
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocation for the Apple companion lane, structural blocked-proof checks for the non-runnable XcodeKit lane, anchor checks for Apple boot-slice vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every Apple lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; Apple matrices and eval records match actual outcomes; and verification passes
- Notes: P12 stays Apple-only and does not claim Microsoft or CodeWarrior host success; `xcodekit` remains a required native editor target even when its current proof is structural and blocked

### Plan ID: P13

- Title: Legacy host boot-slice implementations and backlog stabilization
- Status: Completed
- Objective: implement the committed CodeWarrior boot-slice wave, keep both legacy lanes honest about runnable versus archival-native limits, and stabilize the broader legacy candidate backlog using what this implementation wave revealed
- Scope: `hosts/metrowerks/**`, `inventory/legacy-ide-families.yaml`, legacy-related matrix rows, legacy eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/metrowerks/**`, `inventory/legacy-ide-families.yaml`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P05 CodeWarrior and legacy atlas research, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic fixtures, and the existing CodeWarrior lane scaffold under `hosts/metrowerks/**`
- Milestones: implement runnable cli-bridge proofs for the committed `ide-sdk` and `companion` lanes; add native-adjacent structural metadata for the archival-native lane; refine legacy support, capability, feature, and test matrices to match actual proof posture; stabilize `inventory/legacy-ide-families.yaml` using post-CodeWarrior guidance; record legacy eval status and a CodeWarrior run log; update root planning and documentation indexes
- Blockers: no reproducible historical CodeWarrior environment for honest in-host IDE SDK or COM loading; no active-document capture path for optional `ide-sdk` editor-marker proof; later Eclipse-era CodeWarrior contract boundaries remain unresolved under the current native lane umbrella
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocations for runnable CodeWarrior lanes, structural verification of native-adjacent metadata for `ide-sdk`, anchor checks for legacy boot-slice and backlog vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every committed legacy lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; legacy matrices and eval records match actual outcomes; the broader legacy backlog is conservatively stabilized; and verification passes
- Notes: P13 stays CodeWarrior-only for implementation work and does not promote any backlog candidate into a new committed `hosts/` lane

### Plan ID: P14

- Title: Documentation normalization, roadmap, contributor guidance, and maintenance automation baseline
- Status: Completed
- Objective: consolidate the repository after the first implementation wave by normalizing root docs, creating contributor and roadmap guidance, establishing the maintenance baseline, adding repo-local maintenance skills, and recording a post-P13 audit
- Scope: root documentation, `scripts/**`, `.agents/**`, `evals/reports/**`, and root planning or documentation indexes only
- Allowed Paths: `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `MAINTENANCE.md`, `CHANGELOG.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `scripts/**`, `.agents/README.md`, `.agents/skills/**`, `evals/reports/**`
- Dependencies: P00 through P13, especially the root control-plane files, current matrix posture, existing repo-local skills, and the first host-family proof waves
- Milestones: normalize `README.md`; add contributor, roadmap, maintenance, and changelog docs; create maintenance task catalog and reusable checklists; add maintenance-oriented repo-local skills; record the bootstrap-phase audit and blocker summary; update root planning and documentation indexes
- Blockers: none for the consolidation phase itself; the new docs must preserve existing blocked and deferred technical areas rather than trying to resolve them
- Verification Intent: structural verification using file and directory existence checks, skill frontmatter checks, anchor scans for roadmap and maintenance vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: the repo has coherent contributor, roadmap, changelog, and maintenance docs; maintenance assets and repo-local skills exist; the bootstrap-phase audit exists; root indexes are updated; and verification passes
- Notes: P14 is consolidation-only and does not add new product features, broaden the boot slice, or create new host families

### Plan ID: P15

- Title: AIDE self-bootstrap queue scaffold
- Status: Completed
- Objective: create the minimal filesystem queue, policies, repo instructions, scripts, and first Q00 ExecPlan needed for future self-hosting work to proceed from repository state rather than chat state
- Scope: `.aide/**`, `.agents/**`, `scripts/**`, `docs/**`, `AGENTS.md`, `README.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`
- Allowed Paths: `AGENTS.md`, `README.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `docs/**`, `.aide/**`, `.agents/**`, `scripts/**`
- Dependencies: P00 through P14, especially current operating law, root documentation indexes, repo-local skills, and maintenance automation boundaries
- Milestones: create `.aide/profile.yaml` and `.aide/toolchain.lock`; create queue policy, index, and Q00 task packet; add autonomy, bypass, and review-gate policies; add queue, ExecPlan, and review skills; add conservative queue scripts; document self-bootstrap usage; update root indexes
- Blockers: none for the scaffold itself; future queue items remain pending until Q00 is processed and reviewed
- Verification Intent: structural file-existence checks, Python syntax checks for queue scripts, read-only queue script execution, anchor scans for canonical queue policy, and an allowed-path audit over repository changes
- Exit Criteria: all required scaffold files exist, queue scripts run without external dependencies, Q00 remains ready for a future worker, root docs link the queue, evidence records validation, and the change is committed
- Notes: P15 is a self-bootstrap scaffold only; it does not implement Runtime, Hosts, Commander, Mobile, app surfaces, provider integrations, or Q01 through Q04

## Reboot Queue Plan Index

### Queue ID: Q00-bootstrap-audit

- Title: Baseline freeze and reboot audit
- Status: Needs Review
- Objective: produce a factual, evidence-backed baseline freeze for the in-place AIDE reboot while preserving P00 through P15 history
- Scope: reboot baseline docs, root documentation links, Q00 status and evidence, and queue plan visibility through Q08
- Allowed Paths: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `docs/**`, `.aide/**`, `.agents/**`, `scripts/**`, `AGENTS.md`
- Dependencies: P00 through P15 and the Q00 queue task packet
- Milestones: create bootstrap-era constitution; create reboot charter; create repo census; create reboot roadmap; update root indexes; write Q00 evidence; run validation; stop at review
- Blockers: none identified at planning time
- Verification Intent: required file checks, queue helper execution, anchor scans for the reboot model, changed-path audit, and documentation sanity checks
- Exit Criteria: Q00 documents and evidence exist, root docs link them, Q01 through Q08 are visible as queue plan, validation is recorded, and status moves to `needs_review`
- Notes: Q00 does not implement Q01 or later work, move files, build runtime or host surfaces, or change forbidden paths

### Queue ID: Q01-documentation-split

- Title: Documentation split and canonical architecture
- Status: Needs Review
- Objective: split reboot documentation into durable families and document the canonical model around AIDE Core, AIDE Hosts, AIDE Bridges, the internal Core split, and the first shipped stack
- Scope: documentation family indexes, focused charters, ADR-like decisions, roadmap/reference records, root documentation pointers, Q01 queue status, and Q01 evidence
- Allowed Paths: `docs/**`, `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `.aide/queue/Q01-documentation-split/**`, `.aide/queue/index.yaml`
- Dependencies: Q00 baseline records and explicit Q01 implementation authorization while Q00 remains `needs_review`
- Milestones: create documentation family indexes; add Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK charters; add initial reboot decisions; add migration and terminology references; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; Q00 still needs review before the reboot baseline is accepted
- Verification Intent: structural file checks, queue helper execution, terminology scans, documentation sanity checks, and an allowed-path audit over the diff
- Exit Criteria: Q01 documentation families are navigable, root docs point to them, evidence and validation are recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q01 is documentation-only and does not implement Q02, Runtime, Hosts, Commander, Mobile, IDE extensions, provider adapters, app surfaces, or automation

### Queue ID: Q02-structural-skeleton

- Title: Minimal self-hosting structural skeleton
- Status: Needs Review
- Objective: introduce target `core/`, new host-category, and `bridges/` README-only skeletons without moving bootstrap-era implementation
- Scope: target skeleton directories, README ownership boundaries, structural migration map, root documentation pointers, Q02 queue status, and Q02 evidence
- Allowed Paths: `core/**`, `hosts/README.md`, `hosts/cli/**`, `hosts/service/**`, `hosts/commander/**`, `hosts/extensions/**`, `bridges/**`, `docs/**`, root docs, `.aide/queue/Q02-structural-skeleton/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00 and Q01 outputs; both are currently `needs_review`, and Q02 proceeded only because the current human prompt explicitly authorized implementation
- Milestones: create Core skeleton; create host-category skeletons; create Dominium Bridge skeleton; add structural migration map; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; Q00 and Q01 still need review before their outputs are accepted
- Verification Intent: skeleton file checks, migration-map checks, root doc checks, queue helper execution, terminology scans, lightweight shared test/import-preservation check, `git diff --check`, and allowed-path audit
- Exit Criteria: target skeleton READMEs exist, current code and proofs remain unmoved, structural map and evidence are recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q02 is structure/documentation-only and does not implement Q03, Runtime, Host behavior, Commander, Mobile, IDE extensions, provider adapters, app surfaces, or autonomous service logic

### Queue ID: Q03-profile-contract-v0

- Title: Profile contract v0
- Status: Needs Review
- Objective: implement the minimal declarative `.aide/` Profile/Contract v0 for the AIDE self-hosting repo
- Scope: `.aide/` contract records, documented Contract shapes, source-of-truth references, root doc pointers, Q03 status, and Q03 evidence
- Allowed Paths: `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/components/**`, `.aide/commands/**`, `.aide/policies/**`, `.aide/tasks/**`, `.aide/evals/**`, `.aide/adapters/**`, `.aide/compat/**`, `core/contract/**`, `docs/reference/profile-contract-v0.md`, `docs/reference/source-of-truth.md`, `AGENTS.md`, `.agents/skills/**`, root docs, `.aide/queue/Q03-profile-contract-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00, Q01, and Q02 outputs; all three remain `needs_review`, and Q03 proceeded only because the current human prompt explicitly authorized implementation
- Milestones: define Profile versus Harness boundaries; refine `.aide/profile.yaml` and `.aide/toolchain.lock`; add component, command, policy, task, eval, adapter, and compat declarations; document v0 shapes; add source-of-truth references; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; prior queue items still need review before their outputs are accepted
- Verification Intent: required file checks, required component checks, command and policy checks, queue helper execution, terminology scans, lightweight YAML/Markdown sanity checks, `git diff --check`, and allowed-path audit
- Exit Criteria: Profile/Contract v0 records and references exist, Profile vs Harness is clear, generated artifacts remain deferred, evidence is recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q03 is contract-only and does not implement Harness commands, generated downstream artifacts, Runtime, Hosts, Dominium Bridge behavior, provider adapters, app surfaces, source refactors, or Q04+ work

### Queue ID: Q04-harness-v0

- Title: Harness v0
- Status: Passed With Notes
- Objective: implement the smallest deterministic AIDE Harness v0 command surface for reading, validating, doctoring, and reporting on the Q03 Profile/Contract v0
- Scope: `scripts/aide`, `core/harness/**`, `docs/reference/harness-v0.md`, minimal root doc updates, Q04 queue status, ExecPlan updates, and evidence
- Allowed Paths: `core/harness/**`, `scripts/aide`, `docs/reference/harness-v0.md`, root docs, `.aide/queue/Q04-harness-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00, Q01, Q02, and Q03 outputs remain `needs_review`; this implementation proceeded under explicit human authorization and the full audit verdict `PROCEED_TO_Q04_IMPLEMENTATION`
- Milestones: implement repo-root entrypoint; add Harness modules; implement init/import/compile/validate/doctor/migrate/bakeoff; add lightweight tests; update docs and evidence; run command smoke and structural validation
- Blockers: none encountered during implementation; Q05 remains blocked until Q04 review passes
- Verification Intent: command smoke checks, `aide validate`, `aide doctor`, compile/migrate/bakeoff reports, lightweight unittest smoke, queue helper checks, generated-artifact absence checks, `git diff --check`, and allowed-path audit
- Exit Criteria: Harness v0 commands run, validation passes with warnings only, evidence is recorded, generated artifacts remain absent, and Q04 review records `PASS_WITH_NOTES`
- Notes: Q04 does not implement Q05 generated artifacts, Q06 compatibility baseline, Q07 Dominium Bridge, Runtime, Hosts, provider integrations, app surfaces, release automation, or autonomous worker execution. Q05 planning may proceed; Q05 implementation still requires its own plan and review gate.

### Queue ID: Q05-generated-artifacts-v0

- Title: Generated artifacts v0
- Status: Needs Review
- Objective: implement deterministic generated downstream artifact v0 for AIDE self-hosting guidance while keeping `.aide/` and `.aide/queue/` canonical
- Scope: bounded Harness-status refresh, generated artifact policy docs, Harness compile/validate updates, managed sections in `AGENTS.md` and selected `.agents/skills/**`, `.aide/generated/manifest.yaml`, preview-only Claude guidance, Q05 status, and Q05 evidence
- Allowed Paths: `core/harness/**`, selected `.aide/**` contract/generated paths allowed by Q05, `AGENTS.md`, `.agents/skills/**`, `docs/reference/generated-artifacts-v0.md`, source-of-truth and Harness references, root docs, `.aide/queue/Q05-generated-artifacts-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes and Q05 planning explicitly authorized the bounded Q03-era Harness wording refresh before generation
- Milestones: refresh stale Harness contract wording; document generated artifact v0; add marker and manifest helpers; add compile dry-run/preview/write behavior; add validate drift checks; generate approved managed/preview outputs; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: pre/post Harness validation and doctor checks, compile dry-run/preview/write flows, command smoke checks, Harness unittest and py_compile checks, queue helper checks, marker/manifest scans, final Claude target absence checks, `git diff --check`, and allowed-path audit
- Exit Criteria: generated artifact policy, manifest, managed sections, preview output, Harness drift checks, evidence, and review-gated `needs_review` status are present without Q06+ or forbidden scope
- Notes: Q05 does not make generated artifacts canonical, create final root `CLAUDE.md`, create final `.claude/**`, implement Compatibility baseline, Dominium Bridge, Runtime, Hosts, provider adapters, app surfaces, release automation, or autonomous service logic.

### Queue ID: Q06-compatibility-baseline

- Title: Compatibility baseline
- Status: Needs Review
- Objective: implement the smallest enforceable Compatibility baseline for known AIDE repo evolution surfaces without building a full migration platform
- Scope: `.aide/compat/**`, `core/compat/**`, Harness validate/migrate compatibility checks, compatibility reference docs, minimal root docs, Q06 status, and Q06 evidence
- Allowed Paths: `core/compat/**`, targeted `core/harness/**` validate/migrate changes, `.aide/compat/**`, `.aide/toolchain.lock`, `.aide/commands/**`, `.aide/evals/**`, `.aide/generated/**` manifest refresh only, reference docs, root docs, `.aide/queue/Q06-compatibility-baseline/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 review evidence records `PASS_WITH_NOTES` and allows Q06 despite raw Q05 queue status remaining `needs_review`
- Milestones: define compatibility docs and records; add version, migration, and replay helpers; extend validate/migrate checks; add compatibility tests; refresh generated manifest if source inputs change; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: pre/post Harness validation, doctor, migrate, compile/bakeoff checks, Harness and Compatibility unittests, py_compile, queue helper checks, compatibility record checks, `git diff --check`, and allowed-path audit
- Exit Criteria: compatibility docs and records exist, `aide validate` and `aide migrate` report Q06 baseline posture, replay baseline and upgrade/deprecation records exist, evidence is recorded, and status moves to `needs_review`
- Notes: Q06 does not implement real migrations, Dominium Bridge, Runtime, Hosts, providers, generated artifact behavior changes, release automation, or Q07+ work.

### Queue ID: Q07-dominium-bridge-baseline

- Title: Dominium Bridge baseline
- Status: Passed With Notes
- Objective: implement the smallest enforceable AIDE-side Dominium Bridge baseline so Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance
- Scope: bridge metadata, Dominium/XStack profile overlay, strict policy overlays, generated target expectations, compatibility/pinning records, bridge reference docs, minimal Harness bridge status checks, Q07 status, and Q07 evidence
- Allowed Paths: `bridges/dominium/**`, minimal `core/harness/**` bridge checks if needed, selected `.aide/**` metadata paths allowed by Q07, bridge/source-of-truth/reference docs, root docs, `.aide/queue/Q07-dominium-bridge-baseline/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 and Q06 review evidence record `PASS_WITH_NOTES` and allow Q07 despite raw Q05/Q06 queue status remaining `needs_review`
- Milestones: define bridge reference; define bridge metadata; define XStack boundary; define profile overlay; define strict policy overlays; define generated target expectations; define compatibility pinning; add minimal Harness bridge checks; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: Harness validate, doctor, compile, and migrate checks; queue helper checks; bridge file and anchor checks; generated manifest drift awareness; `git diff --check`; allowed-path audit
- Exit Criteria: Q07 bridge docs and records exist, Harness reports structural bridge posture, generated target expectations remain metadata-only, no Dominium repo or real Dominium output is touched, evidence is recorded, and Q07 review records `PASS_WITH_NOTES`
- Notes: Q07 does not modify any Dominium repo, emit real Dominium outputs, implement Runtime, Hosts, providers, app surfaces, release automation, or Q08+ work. Q08 planning may proceed; Q08 implementation still requires its own plan, evidence, and review gate.

### Queue ID: Q08-self-hosting-automation

- Title: Self-hosting automation
- Status: Passed With Notes
- Objective: implement the smallest safe self-hosting automation scaffold so AIDE can inspect queue health, drift, doctor guidance, compatibility posture, bridge status, and follow-up recommendations without uncontrolled autonomy
- Scope: self-hosting reference docs, a report-first `aide self-check` command, bounded doctor next-step cleanup, conservative queue-runner helper improvements, non-canonical self-check report outputs, Q08 status, and Q08 evidence
- Allowed Paths: `scripts/aide`, `scripts/aide-queue-run`, read-only queue helpers only if needed, `core/harness/**`, selected `.aide/**` self-hosting declaration/report paths allowed by Q08, reference docs, root docs, `.aide/queue/Q08-self-hosting-automation/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 and Q06 review evidence record `PASS_WITH_NOTES` despite raw `needs_review` statuses; Q07 passed with notes and explicitly permits Q08 planning
- Milestones: define automation policy; add self-hosting reference; implement report-first self-check; keep report outputs non-canonical; improve queue runner without automatic agent invocation; fix stale doctor next-step wording; write evidence; stop at review
- Blockers: none for planning; implementation must not treat stale generated manifest or stale doctor wording as silent execution signals
- Verification Intent: pre/post Harness validate, doctor, compile dry-run, migrate, and bakeoff checks; self-check smoke; queue helper checks; Harness tests and py_compile as needed; generated manifest drift reporting; `git diff --check`; allowed-path audit
- Exit Criteria: Q08 implementation reaches `needs_review` only after self-hosting automation remains local, deterministic, report-first, non-autonomous, and evidence-backed
- Notes: Q08 implements report-first self-check and queue-runner visibility only. It does not invoke Codex or external agents automatically, call models/providers/network, auto-merge, silently refresh generated artifacts, implement Runtime/Service/Commander, or create post-Q08 work. Independent review accepted Q08 with notes; post-Q08 foundation review may proceed while generated manifest drift, command catalog metadata for `aide self-check`, and raw status nuance remain visible cleanup items.

### Queue ID: Q09-token-survival-core

- Title: State reconciliation and token survival core
- Status: Accepted With Notes
- Objective: reconcile live post-Q08 state and add repo-only token-survival scaffolding so future work uses compact task packets, approximate token estimates, and evidence review instead of long chat history
- Scope: Q09 queue packet, post-Q08 profile/catalog/docs metadata, token budget policy, compact memory files, prompt templates, context ignore policy, AIDE Lite token-survival commands, tests, generated compact packet outputs, and evidence
- Allowed Paths: `.aide/queue/Q09-token-survival-core/**`, `.aide/queue/index.yaml`, `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/commands/catalog.yaml`, `.aide/policies/**`, `.aide/prompts/**`, `.aide/context/**`, `.aide/memory/**`, `.aide/scripts/**`, `AGENTS.md`, root docs, selected `docs/reference/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q08 passed with notes; Q05/Q06 raw status nuance remains visible while review evidence permits later dependency use
- Milestones: reconcile stale state; add token policy and compact prompts; implement AIDE Lite doctor/validate/estimate/snapshot/pack/adapt/selftest; add tests; generate Q10 packet; write evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift must be either preserved visibly or refreshed only through the reviewed Harness compile/write path
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke, AIDE Lite unit tests, `git diff --check`, and targeted secret scan
- Exit Criteria: Q09 status moved to `needs_review`, Q10 compact task packet exists with a token estimate, AGENTS.md carries token-survival guidance, validation is recorded, and no secrets/local state/raw prompt logs are committed
- Notes: Q09 does not implement Gateway, providers, model routing, local models, Runtime, Service, Commander, Mobile, MCP/A2A, cloud, autonomous loops, vector search, semantic cache, or host/app surfaces.

### Queue ID: Q10-aide-lite-hardening

- Title: AIDE Lite hardening
- Status: Accepted With Notes
- Objective: harden the Q09 no-install AIDE Lite workflow so future queue phases can generate, validate, adapt, estimate, and self-test compact packets reliably
- Scope: Q10 queue packet, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, token-survival prompt/context/memory/policy records, generated context outputs, AGENTS token-survival managed section, root docs, and narrow Harness/doc touchpoints if needed
- Allowed Paths: `.aide/queue/Q10-aide-lite-hardening/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/policies/token-budget.yaml`, `.aide/prompts/**`, `.aide/context/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `.aide/generated/manifest.yaml` through compile/write only, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs exist and are review-ready; Q10 proceeds under explicit prompt authorization while Q09 awaits review
- Milestones: create Q10 queue packet; harden AIDE Lite helpers and commands; add deterministic write and drift behavior; expand tests; generate Q11 packet; write evidence; stop at review
- Blockers: none identified at planning time; Q09 missing-output blockers must stop Q10 if discovered
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke, `.aide/scripts/tests` unittest discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q10 status moves to `needs_review`, Q11 compact task packet exists with token estimate, AIDE Lite commands and tests pass, adapt is deterministic, snapshot contains no raw contents, and evidence is complete
- Notes: Q10 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, full context compiler, full verifier, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q11 should build Context Compiler v0 from the compact packet generated by Q10.

### Planned Reboot Queue

- `Q01-documentation-split`: documentation split and canonical architecture; implemented and awaiting review
- `Q02-structural-skeleton`: structural skeleton; implemented and awaiting review
- `Q03-profile-contract-v0`: profile contract v0; implemented and awaiting review
- `Q04-harness-v0`: harness v0 passed review with notes
- `Q05-generated-artifacts-v0`: generated artifacts v0 implemented with managed sections, preview-only Claude guidance, manifest records, and drift checks; awaiting review
- `Q06-compatibility-baseline`: compatibility baseline implemented and awaiting review
- `Q07-dominium-bridge-baseline`: Dominium Bridge baseline passed review with notes
- `Q08-self-hosting-automation`: self-hosting automation passed review with notes
- `Q09-token-survival-core` through `Q20-provider-adapter-v0`: token-survival foundation accepted with notes by QFIX-01; substrate readiness only, not product readiness
- `QCHECK-token-survival-foundation-audit`: checkpoint audit recorded PASS_WITH_WARNINGS and recommended repair before Q21
- `QFIX-01-foundation-review-reconciliation`: implemented reconciliation repair; awaiting review
- `QFIX-02-aide-lite-test-discovery-runner`: implemented test-runner repair; awaiting review
- `Q21-cross-repo-pack-export-import-v0`: implemented and awaiting review; fixture validation only
- `Q22-eureka-import-pilot`: completed in the Eureka target repo and awaiting target-repo review
- `Q23-dominium-import-pilot`: completed in the Dominium target repo and awaiting target-repo review
- `Q24-existing-tool-adapter-compiler-v0`: implemented and awaiting review; generated/preview adapter guidance only
- `Q25-importer-scope-and-state-truth-repair`: implemented and awaiting review; repairs pack integrity, safe import scope, provenance, and state truth before Q26

### Queue ID: Q11-context-compiler-v0

- Title: Context Compiler v0
- Status: Accepted With Notes
- Objective: implement deterministic repo-local context maps, test maps, context indexes, exact refs, and context packets so future queue phases can avoid whole-repo or long-history prompting
- Scope: Q11 queue packet, `.aide/context/**`, AIDE Lite index/context/map behavior, `.aide/scripts/tests/**`, selected token-survival prompt/memory/config updates, optional AIDE Lite command metadata, root docs, selected reference/roadmap docs, and narrow Harness test/doc touchpoints if needed
- Allowed Paths: `.aide/queue/Q11-context-compiler-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/context/**`, `.aide/policies/token-budget.yaml`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs and Q10 AIDE Lite hardening outputs exist and are review-ready; Q11 proceeds under explicit prompt authorization while Q09/Q10 await review
- Milestones: create Q11 queue packet; add context compiler config; extend AIDE Lite index/context/map behavior; generate repo-map/test-map/context-index/context packet/Q12 packet; add tests; update docs and evidence; stop at review
- Blockers: none identified at planning time; profile current-focus staleness remains visible because Q11 does not allow profile edits
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including index/context, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q11 status moves to `needs_review`, context artifacts exist without raw file dumps, AIDE Lite commands/tests pass, Q12 compact task packet exists with context refs, and evidence is complete
- Notes: Q11 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, embeddings, vector search, semantic cache, full verifier, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q12 should add Verifier v0 using the context-backed compact packet generated by Q11.

### Queue ID: Q12-verifier-v0

- Title: Verifier v0
- Status: Accepted With Notes
- Objective: implement deterministic repo-local mechanical verification so future AIDE phases can check evidence packets, task packets, file references, line refs, changed-file scope, adapter drift, context packet shape, token warnings, and obvious secret risks before premium-model review
- Scope: Q12 queue packet, `.aide/verification/**`, `.aide/policies/verification.yaml`, AIDE Lite verify behavior, `.aide/scripts/tests/**`, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, generated verification report, and Q12 evidence
- Allowed Paths: `.aide/queue/Q12-verifier-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/verification/**`, `.aide/policies/verification.yaml`, `.aide/policies/token-budget.yaml`, `.aide/context/**`, `.aide/prompts/evidence-review.md`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, and Q11 context compiler outputs exist and are review-ready; Q12 proceeds under explicit prompt authorization while Q09/Q10/Q11 await review
- Milestones: create Q12 queue packet; add verifier policies/templates; extend AIDE Lite verify behavior; add tests and fixtures; generate latest verification report and Q13 packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including verify variants, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q12 status moved to `needs_review`, verifier command and tests pass, latest verification report exists, Q13 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q12 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, golden tasks, LLM-as-judge, automatic repair, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q13 should build the Evidence Review Workflow from Q12 verifier output.

### Queue ID: Q13-evidence-review-workflow

- Title: Evidence Review Workflow
- Status: Accepted With Notes
- Objective: implement deterministic repo-local review-packet generation so GPT-5.5 or a human reviewer can judge compact evidence, verifier output, validation summaries, changed-file summaries, token summaries, risks, and scope boundaries without full chat history or whole repo context
- Scope: Q13 queue packet, `.aide/verification/review-decision-policy.yaml`, review-packet template, evidence-review prompt, AIDE Lite `review-pack` behavior, review-packet validation, `.aide/scripts/tests/**`, generated latest review/task packets, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q13 evidence
- Allowed Paths: `.aide/queue/Q13-evidence-review-workflow/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/verification/**`, `.aide/policies/verification.yaml`, `.aide/policies/token-budget.yaml`, `.aide/context/**`, `.aide/prompts/evidence-review.md`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, Q11 context compiler outputs, and Q12 verifier outputs exist and are review-ready; Q13 proceeds under explicit prompt authorization while Q09-Q12 await review
- Milestones: create Q13 queue packet; refine evidence-review prompt/template/policy; extend AIDE Lite `review-pack`; add review-packet validation and tests; generate latest review packet and Q14 task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including review-pack and verify --review-packet, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q13 status moved to `needs_review`, review-pack command and tests pass, latest review packet exists, Q14 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q13 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, golden tasks, LLM-as-judge automation, automatic GPT calls, automatic repair, full semantic diff analysis, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q14 should formalize token ledger and savings reporting from Q13 packets.

### Queue ID: Q14-token-ledger-savings-report

- Title: Token Ledger and Savings Report
- Status: Accepted With Notes
- Objective: implement deterministic repo-local estimated token accounting so future AIDE phases can record packet/report sizes, compare compact surfaces to named naive baselines, warn on budgets or regressions, and avoid raw prompt/response storage
- Scope: Q14 queue packet, `.aide/policies/token-ledger.yaml`, `.aide/reports/**`, AIDE Lite `ledger` behavior, budget/regression helpers, `.aide/scripts/tests/**`, generated latest task/review/report artifacts, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q14 evidence
- Allowed Paths: `.aide/queue/Q14-token-ledger-savings-report/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/policies/token-budget.yaml`, `.aide/policies/token-ledger.yaml`, `.aide/reports/**`, `.aide/context/**`, `.aide/prompts/compact-task.md`, `.aide/prompts/evidence-review.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, Q11 context compiler outputs, Q12 verifier outputs, and Q13 review-packet outputs exist and are review-ready; Q14 proceeds under explicit prompt authorization while Q09-Q13 await review
- Milestones: create Q14 queue packet; add token-ledger policy and baseline reports; extend AIDE Lite with ledger scan/add/report/compare; add budget/regression tests; generate ledger records, savings summary, Q15 task packet, and review artifacts; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including ledger scan/report/compare, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q14 status moved to `needs_review`, ledger commands and tests pass, token ledger JSONL and savings summary exist, Q15 compact task packet exists, baseline comparison is recorded, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q14 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, real API usage accounting, golden tasks, LLM-as-judge, automatic GPT review, automatic repair, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q15 should add deterministic Golden Tasks v0 quality scaffolding.

### Queue ID: Q15-golden-tasks-v0

- Title: Golden Tasks v0
- Status: Accepted With Notes
- Objective: implement deterministic repo-local golden task quality gates so token-saving workflow changes can prove compact task packets, context packets, verifier failure detection, review packets, token ledger metadata, and adapter managed-section determinism still preserve required behavior
- Scope: Q15 queue packet, `.aide/policies/evals.yaml`, `.aide/evals/**`, AIDE Lite `eval list/run/report` behavior, `.aide/scripts/tests/**`, generated eval/context/review/token report artifacts, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q15 evidence
- Allowed Paths: `.aide/queue/Q15-golden-tasks-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/evals/**`, `.aide/policies/evals.yaml`, selected token/verifier policies, `.aide/reports/**`, `.aide/context/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, and Q14 token ledger outputs exist and are review-ready; Q15 proceeds under explicit prompt authorization while Q09-Q14 await review
- Milestones: create Q15 queue packet; add eval policy and golden task catalog; extend AIDE Lite with eval list/run/report; add golden task tests; generate latest golden-task reports and Q16 compact task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including eval list/run/report, direct `.aide/scripts/tests` discovery, documented hidden-path discovery check, `git diff --check`, and targeted secret scan
- Exit Criteria: Q15 status moved to `needs_review`, eval commands and tests pass, latest golden-task JSON/Markdown reports exist, Q16 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q15 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, external coding benchmarks, LLM-as-judge, automatic GPT review, automatic repair, Q16 Outcome Controller recommendations, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q16 should consume Q15 token-quality signals.

### Queue ID: Q16-outcome-controller-v0

- Title: Outcome Controller v0
- Status: Accepted With Notes
- Objective: implement deterministic repo-local advisory outcome analysis so token, verifier, review, context, validation, and golden-task signals produce bounded recommendations without unsafe autonomy
- Scope: Q16 queue packet, `.aide/policies/controller.yaml`, `.aide/controller/**`, AIDE Lite outcome/optimize behavior, `.aide/scripts/tests/**`, generated controller/context/review/token report artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q16 evidence
- Allowed Paths: `.aide/queue/Q16-outcome-controller-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/controller/**`, `.aide/policies/controller.yaml`, selected token/verifier/eval policies, `.aide/reports/**`, `.aide/evals/runs/**`, `.aide/context/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, and Q15 golden tasks outputs exist and are review-ready; Q16 proceeds under explicit prompt authorization while Q09-Q15 await review
- Milestones: Q16 queue packet created; controller policy and records added; AIDE Lite outcome report/add and optimize suggest added; controller tests added; latest outcome report, recommendations, review packet, token reports, eval reports, and Q17 compact task packet generated; docs/evidence updated; stopped at review
- Blockers: none blocking Q16 completion; generated manifest drift and raw review-gate nuance remain visible existing warnings rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including outcome/optimize, direct `.aide/scripts/tests` discovery, documented hidden-path discovery check, `git diff --check`, and targeted secret scan
- Exit Criteria: Q16 status moves to `needs_review`, outcome/optimize commands and tests pass, latest outcome/recommendation reports exist, Q17 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q16 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, automatic prompt/policy/route mutation, LLM-as-judge, automatic GPT review, automatic repair, Q17 Router Profile behavior, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q17 should define Router Profile v0 from advisory signals only.

### Queue ID: Q17-router-profile-v0

- Title: Router Profile v0
- Status: Accepted With Notes
- Objective: define deterministic advisory routing from compact task/context packets and local token, verifier, review, golden-task, and outcome signals without live provider/model calls
- Scope: Q17 queue packet, `.aide/policies/routing.yaml`, `.aide/models/**`, `.aide/routing/**`, AIDE Lite route behavior, `.aide/scripts/tests/**`, generated route/context/review/token artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q17 evidence
- Allowed Paths: `.aide/queue/Q17-router-profile-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/models/**`, `.aide/routing/**`, `.aide/policies/routing.yaml`, selected token/verifier/eval/controller policies, `.aide/reports/**`, `.aide/controller/**`, `.aide/context/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, Q15 golden tasks, and Q16 outcome-controller outputs exist and are review-ready; Q17 proceeds under explicit prompt authorization while Q09-Q16 await review
- Milestones: create Q17 queue packet; add advisory routing policy and model/provider registry; extend AIDE Lite with route list/explain/validate; add route tests; generate latest route decision, Q18 compact task packet, and docs/evidence; stop at review
- Blockers: none blocking Q17 implementation; generated manifest drift and raw review-gate nuance remain visible existing warnings rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/optimize/route/pack/estimate/selftest, route unit tests, `git diff --check`, and targeted secret scan
- Exit Criteria: Q17 status moves to `needs_review`, route commands and tests pass, latest route decision artifacts exist, Q18 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q17 does not implement Gateway, live provider calls, model calls, local model setup, provider billing, exact tokenizer, cache/local-state boundary, automatic route execution, automatic prompt/policy mutation, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q18 should define cache and local-state boundaries separately.

### Queue ID: Q18-cache-local-state-boundary

- Title: Cache and Local State Boundary
- Status: Accepted With Notes
- Objective: define the first deterministic cache-key and local-state boundary so committed `.aide/` contract state stays separate from ignored `.aide.local/` runtime state before Gateway/provider/cache work exists
- Scope: Q18 queue packet, `.gitignore`, `.aide.local.example/**`, `.aide/policies/cache.yaml`, `.aide/policies/local-state.yaml`, `.aide/cache/**`, AIDE Lite cache commands, `.aide/scripts/tests/**`, generated cache/context/review/route/token artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q18 evidence
- Allowed Paths: `.gitignore`, `.aide/queue/Q18-cache-local-state-boundary/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/cache/**`, `.aide/policies/cache.yaml`, `.aide/policies/local-state.yaml`, `.aide.local.example/**`, `.aide/context/**`, `.aide/routing/**`, `.aide/reports/**`, `.aide/controller/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, Q15 golden tasks, Q16 outcome controller, and Q17 router profile outputs exist and are review-ready; Q18 proceeds under explicit prompt authorization while Q09-Q17 await review
- Milestones: create Q18 queue packet; add `.gitignore`, `.aide.local.example/**`, cache/local-state policies, and cache metadata directory; extend AIDE Lite with cache init/status/key/report; add tests; generate latest cache keys and Q19 compact task packet; update docs/evidence; stop at review
- Blockers: none blocking Q18 implementation; generated manifest drift and raw review-gate nuance remain visible existing warnings rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/optimize/route/cache/pack/estimate/selftest, cache unit tests, `git check-ignore .aide.local/`, `git diff --check`, and targeted secret scan
- Exit Criteria: Q18 status moves to `needs_review`, cache commands and tests pass, `.aide.local/` is ignored and not tracked, cache key reports exist, Q19 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q18 does not implement Gateway, provider calls, live model calls, local model setup, provider billing, exact tokenizer, semantic cache, embeddings/vector DB, live prompt/response cache, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q19 should define Gateway Architecture and Skeleton separately.

### Queue ID: Q19-gateway-architecture-skeleton

- Title: Gateway Architecture and Skeleton
- Status: Accepted With Notes
- Objective: create a local/report-only Gateway architecture and stdlib skeleton that exposes health, status, route explanation, summaries, and version metadata from existing Q09-Q18 repo-local evidence without provider calls, model calls, outbound network calls, raw prompt logging, raw response logging, Runtime, or UI work
- Scope: Q19 queue packet, `.aide/policies/gateway.yaml`, `.aide/gateway/**`, `core/gateway/**`, AIDE Lite gateway commands, `.aide/scripts/tests/**`, generated gateway/context/review/route/cache/token artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q19 evidence
- Allowed Paths: `.aide/queue/Q19-gateway-architecture-skeleton/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/gateway/**`, `.aide/policies/gateway.yaml`, selected cache/local-state/routing policies, `.aide/context/**`, `.aide/routing/**`, `.aide/reports/**`, `.aide/controller/**`, `.aide/cache/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/gateway/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, Q15 golden tasks, Q16 outcome controller, Q17 router profile, and Q18 cache/local-state boundary outputs exist and are review-ready; Q19 proceeds under explicit prompt authorization while Q09-Q18 await review
- Milestones: create Q19 queue packet; add Gateway policy and architecture artifacts; implement core Gateway status/server skeleton and AIDE Lite gateway commands; add tests; generate latest Gateway status and Q20 compact task packet; update docs/evidence; stop at review
- Blockers: none blocking Q19 implementation; generated manifest drift and raw review-gate nuance remain visible existing warnings rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, core Gateway tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/optimize/route/cache/gateway/pack/estimate/selftest, `git check-ignore .aide.local/`, `git diff --check`, and targeted secret scan
- Exit Criteria: Q19 status moves to `needs_review`, Gateway policy/artifacts and core skeleton exist, gateway commands/tests pass, latest Gateway status reports exist, Q20 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs/raw response logs are committed
- Notes: Q19 does not implement provider calls, model calls, outbound network calls, real Gateway proxy forwarding, OpenAI/Anthropic-compatible forwarding, provider adapters, local model setup, provider billing, exact tokenizer, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q20 should add Provider Adapter v0 only after these local safety boundaries are reviewed.

### Queue ID: Q20-provider-adapter-v0

- Title: Provider Adapter v0
- Status: Accepted With Notes
- Objective: implement deterministic offline provider-adapter contracts and capability metadata so AIDE can describe deterministic tools, human review, local model families, remote model families, and aggregators without live provider calls, model calls, outbound network calls, credentials, Gateway forwarding, Runtime, or UI work
- Scope: Q20 queue packet, `.aide/policies/provider-adapters.yaml`, `.aide/providers/**`, `core/providers/**`, AIDE Lite provider commands, `.aide/scripts/tests/**`, generated provider/context/review/route/cache/token/gateway artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q20 evidence
- Allowed Paths: `.aide/queue/Q20-provider-adapter-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/models/**`, `.aide/providers/**`, `.aide/policies/provider-adapters.yaml`, selected gateway/routing/cache/local-state policies, `.aide/context/**`, `.aide/routing/**`, `.aide/reports/**`, `.aide/controller/**`, `.aide/cache/**`, `.aide/gateway/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/providers/**`, `core/gateway/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, Q15 golden tasks, Q16 outcome controller, Q17 router profile, Q18 cache/local-state boundary, and Q19 Gateway skeleton outputs exist and are review-ready; Q20 proceeds under explicit prompt authorization while Q09-Q19 await review
- Milestones: create Q20 queue packet; add provider-adapter policy and provider metadata artifacts; implement core provider contracts/status helpers and AIDE Lite provider commands; add provider tests; generate latest provider status and Q21 compact task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness, Compatibility, and Gateway tests, core provider tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/optimize/route/cache/gateway/provider/pack/estimate/selftest, `git check-ignore .aide.local/`, `git diff --check`, and targeted secret scan
- Exit Criteria: Q20 status moves to `needs_review`, provider policy/catalog/capability/contract/status artifacts exist, provider commands and tests pass, latest provider status reports exist, Q21 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs/raw response logs are committed
- Notes: Q20 does not implement live provider calls, model calls, outbound network calls, provider probes, credentials, local model setup, Gateway forwarding, provider billing, exact tokenizer, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q21 should add cross-repo AIDE Lite Pack export/import before existing-tool adapter work.

### Queue ID: QFIX-01-foundation-review-reconciliation

- Title: Foundation Review Reconciliation
- Status: Needs Review
- Objective: reconcile source-of-truth state after Q09-Q20 so queue index/status files, profile current focus, command catalog posture, and self-check guidance no longer point at stale token-survival review work
- Scope: QFIX-01 queue packet/evidence, Q09-Q20 status and review evidence, Q18 task/status drift repair, `.aide/profile.yaml`, `.aide/commands/catalog.yaml`, Harness self-check next-step guidance, root docs, and bounded Harness tests
- Allowed Paths: the QFIX-01 allowlist in `.aide/queue/QFIX-01-foundation-review-reconciliation/task.yaml`
- Dependencies: QCHECK token survival foundation audit and Q09-Q20 implementation evidence
- Milestones: create repair packet; accept/block/reconcile Q09-Q20; fix Q18 drift; refresh profile/catalog/self-check truth; update compact root docs; run validation; stop at review
- Blockers: none blocking QFIX-01; `.aide/scripts/tests` discovery is explicitly deferred to QFIX-02
- Verification Intent: Harness validate/doctor/self-check, core Harness/Compat/Gateway/Provider tests, AIDE Lite validation and key gates, known failing `.aide/scripts/tests` discovery command, diff check, and targeted secret scan
- Exit Criteria: QFIX-01 reaches `needs_review`, Q09-Q20 truth is coherent, self-check no longer recommends stale Q09, QFIX-02 is clearly next, and no feature work/provider/model/Gateway forwarding is introduced
- Notes: QFIX-01 is reconciliation only. It does not implement QFIX-02, Q21 export/import, live provider calls, model calls, Gateway forwarding, Runtime, UI, host work, or autonomous execution.

### Queue ID: QFIX-02-aide-lite-test-discovery-runner

- Title: AIDE Lite Test Discovery And Runner Fix
- Status: Needs Review
- Objective: make AIDE Lite validation obvious and repeatable before Q21 by diagnosing the hidden `.aide/scripts/tests` discovery failure, adding a canonical `aide_lite.py test` command, and documenting the supported raw unittest form
- Scope: QFIX-02 queue packet/evidence, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/commands/catalog.yaml`, bounded Harness self-check guidance/tests, compact root docs, and AIDE Lite reference docs
- Allowed Paths: the QFIX-02 allowlist in `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/task.yaml`
- Dependencies: QFIX-01 foundation reconciliation and Q09-Q20 token-survival foundation outputs
- Milestones: create repair packet; diagnose failing `-t .` discovery; add canonical `test` alias; add importability and CLI pass/fail tests; update command catalog and docs; run validation; stop at review
- Blockers: none blocking QFIX-02; old `py -3 -m unittest discover -s .aide/scripts/tests -t .` remains intentionally non-canonical
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest, supported `.aide/scripts/tests` discovery, documented failing old discovery command, core Harness/Compat/Gateway/Provider tests, diff check, and targeted secret scan
- Exit Criteria: QFIX-02 reaches `needs_review`, canonical `py -3 .aide/scripts/aide_lite.py test` passes, `selftest` passes, supported unittest discovery passes, old failing command is documented, evidence is complete, and no feature work/provider/model/Gateway forwarding is introduced
- Notes: QFIX-02 is validation-surface repair only. It does not implement Q21 export/import, live provider calls, model calls, Gateway forwarding, Runtime, UI, host work, or autonomous execution.

### Queue ID: Q21-cross-repo-pack-export-import-v0

- Title: Cross-Repo Pack Export / Import v0
- Status: Needs Review
- Objective: make AIDE Lite safely copyable into target repositories through a deterministic portable pack and local fixture import validation before real Eureka or Dominium pilots.
- Scope: Q21 queue packet/evidence, `.aide/policies/export-import.yaml`, `.aide/export/aide-lite-pack-v0/**`, `.aide/import/**`, AIDE Lite export/import/pack-status commands, export/import tests, compact prompt guidance, command catalog truth, root docs, and `docs/reference/cross-repo-pack-export-import.md`.
- Allowed Paths: the Q21 allowlist in `.aide/queue/Q21-cross-repo-pack-export-import-v0/task.yaml`.
- Dependencies: QFIX-01 foundation reconciliation, QFIX-02 canonical AIDE Lite test runner, and Q09-Q20 token-survival foundation outputs.
- Milestones: create Q21 packet; add export/import policy and target templates; add pack export, dry-run import, import, and pack-status behavior; generate pack manifest/checksums/install docs; validate local fixture imports; add tests; update docs/evidence; stop at review.
- Blockers: none blocking Q21 implementation; real Eureka and Dominium imports remain explicitly deferred to Q22 and Q23.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest/export-pack/pack-status/import-pack dry-run/import/pack/estimate, fixture target doctor/snapshot/index/pack, AIDE Lite export/import tests, core Harness/Compat/Gateway/Provider tests, diff check, `.aide.local/` ignore check, and targeted secret scan.
- Exit Criteria: Q21 reaches `needs_review`, the portable pack exists with manifest/checksums/install docs, forbidden source state is excluded, fixture dry-run/import succeeds, fixture target AIDE Lite smoke passes, tests pass, evidence is complete, and no real Eureka/Dominium repos, provider/model/network calls, local state, secrets, raw prompts, or raw responses are introduced.
- Notes: Q21 is portable-pack and fixture-validation only. It does not prove token savings in Eureka or Dominium, implement existing-tool adapters, enable Gateway forwarding, call providers/models/network services, or create live Runtime/UI behavior. Q22 should run the Eureka Import Pilot.

### Queue ID: Q24-existing-tool-adapter-compiler-v0

- Title: Existing Tool Adapter Compiler v0
- Status: Needs Review
- Objective: compile compact AIDE token-survival, context, validation, evidence, and review-gate guidance into generated or preview adapter surfaces for existing tools users already run.
- Scope: Q24 queue packet/evidence, `.aide/policies/adapters.yaml`, `.aide/adapters/**`, `.aide/generated/adapters/**`, AIDE Lite adapter commands, `adapt` alignment, adapter compiler tests, portable pack adapter-template inclusion, prompt guidance, command catalog truth, root docs, and `docs/reference/existing-tool-adapter-compiler-v0.md`.
- Allowed Paths: the Q24 allowlist in `.aide/queue/Q24-existing-tool-adapter-compiler-v0/task.yaml`.
- Dependencies: QFIX-01 foundation reconciliation, QFIX-02 canonical AIDE Lite test runner, Q21 portable pack export/import, and preferably Q22/Q23 target-pilot evidence when available.
- Milestones: create Q24 packet; add adapter compiler policy, targets, and templates; add adapter list/render/preview/validate/drift/generate commands; keep `adapt` deterministic; generate preview outputs and drift report; include portable templates in the export pack; add tests; update docs/evidence; stop at review.
- Blockers: no blocker for implementation; original Q24 started before Q22/Q23 target-pilot evidence was available, but a later post-pilot refresh inspected Eureka and Dominium sibling repos read-only and recorded their pilot results as target-repo evidence awaiting review.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite doctor/validate/test/selftest, adapter list/render/preview/validate/drift, deterministic `adapt`, export-pack refresh, AIDE Lite adapter compiler tests, core Harness/Compat/Gateway/Provider tests, diff check, `.aide.local/` ignore check, and targeted secret scan.
- Exit Criteria: Q24 reaches `needs_review`, adapter policy/templates/targets exist, generated preview outputs and drift report exist, adapter validation checks compact packet/evidence guidance and no-full-history rules, safe managed sections preserve manual content, preview-only targets are not written destructively, export pack includes adapter templates, tests pass, evidence is complete, and no provider/model/network/Gateway/runtime/UI work is introduced.
- Notes: Q24 is deterministic template compilation only. It does not implement Eureka or Dominium pilots, live tool APIs, IDE extensions, provider calls, model calls, network calls, Gateway forwarding, Runtime, Service, Commander, Mobile, MCP/A2A, autonomous loops, exact tokenizer, or provider billing. Eureka and Dominium pilots now strengthen the cross-repo packet evidence, but adapter guidance still needs target-tool usage review.

### Queue ID: Q25-importer-scope-and-state-truth-repair

- Title: Importer Scope And State Truth Repair
- Status: Needs Review
- Objective: repair pack integrity, export provenance, direct importer scope, profile truth, self-check guidance, and command catalog state before Q26 Eureka handover.
- Scope: Q25 queue packet/evidence, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/export/aide-lite-pack-v0/**`, `.aide/import/**`, `.aide/policies/export-import.yaml`, `.aide/profile.yaml`, `.aide/commands/catalog.yaml`, bounded Harness self-check logic/tests, root docs, selected reference/roadmap docs, and regenerated Q26 task packet.
- Allowed Paths: the Q25 allowlist in `.aide/queue/Q25-importer-scope-and-state-truth-repair/task.yaml`.
- Dependencies: QCHECK cross-repo adapter readiness audit, Q21 pack/export-import implementation, Q22/Q23 target-pilot evidence, and Q24 adapter compiler implementation.
- Milestones: create Q25 packet; repair checksum scope and pack-status; narrow import-pack default scope and dry-run reporting; refresh profile/self-check/catalog truth; regenerate pack and Q26 packet; update docs/evidence; stop at review.
- Blockers: none blocking Q25 implementation; broad Eureka handoff remains blocked until Q25 review accepts the repaired surface.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite validate/test/export-pack/pack-status/import-pack dry-run and import, fixture doctor/snapshot/index/pack, AIDE Lite export/import tests, core Harness/Compat/Gateway/Provider tests, diff check, `.aide.local/` ignore check, and targeted secret scan.
- Exit Criteria: Q25 reaches `needs_review`, pack-status passes, checksum/provenance convention is coherent, import defaults to safe scope and preserves manual `AGENTS.md` content, broad roots are excluded by default, fixture import smoke passes, profile/self-check truth is current, Q26 packet exists, evidence is complete, and no Eureka/Dominium repo, provider/model/network, local state, secret, raw prompt, or raw response mutation is introduced.
- Notes: Q25 is repair-only. It does not implement Q26 handover, Dominium golden tasks, new adapters, live Gateway/provider behavior, exact tokenizer, Runtime, Service, Commander, UI, MCP/A2A, autonomous loops, or product features.

### Queue ID: Q26-eureka-pilot-review-and-handover

- Title: Eureka Pilot Review And Handover
- Status: Needs Review
- Objective: review existing Eureka target-pilot evidence read-only after Q25 repaired the pack/import baseline, record controlled handoff posture, and prepare Q27 commit discipline and WorkUnit recovery for redo.
- Scope: Q26 queue packet/evidence, `.aide/queue/index.yaml`, stale Q27-Q29 blocker status reconciliation, `.aide/profile.yaml`, bounded Harness self-check guidance, compact root docs, generated manifest refresh, and regenerated latest task packet.
- Allowed Paths: the Q26 allowlist in `.aide/queue/Q26-eureka-pilot-review-and-handover/task.yaml`.
- Dependencies: Q25 pack/import/state-truth repair evidence and the existing Eureka target-pilot records.
- Milestones: create Q26 packet; inspect sibling Eureka read-only; record pilot review, handover posture, next-task scope, and risks; supersede stale Q27-Q29 blocked attempts; refresh state truth and docs; regenerate Q27 task packet; run validation; stop at review.
- Blockers: none blocking Q26 implementation. Q25 and Q26 still require review before their outputs are treated as accepted.
- Verification Intent: Harness validate/doctor/self-check, AIDE Lite validate/test/pack-status, read-only Eureka doctor/validate/estimate/diff/architecture/secret-scan checks, diff check, generated manifest refresh, and targeted secret scan.
- Exit Criteria: Q26 reaches `needs_review`, Eureka pilot evidence is reviewed read-only, no target repo is mutated, stale Q27-Q29 blockers are superseded for redo, self-check guidance no longer points to the stale Dominium Q27 sequence, latest task packet points to Q27 redo, evidence is complete, and no provider/model/network calls are introduced.
- Notes: Q26 does not implement Eureka work, Dominium work, Q27, branch helpers, Runtime, Service, Commander, UI, MCP/A2A, provider/model calls, or broad handoff claims.

### Queue ID: X-OS-02-capability-reality-ledger-v0

- Title: AIDE Capability Reality Ledger v0
- Status: Needs Review
- Objective: implement deterministic report-only capability reality seeds, scans, ledgers, overclaim reports, validation hooks, tests, golden tasks, docs, and export-pack support over the X-OS-00/X-OS-01 Task OS foundation.
- Scope: X-OS-02 queue packet/evidence, `.aide/capabilities/**`, `.aide/policies/capability-reality.yaml`, `.aide/ledgers/capability-ledger.schema.json`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/evals/golden-tasks/**`, `.aide/reports/capability-*`, export-pack refresh, context/review packets, root planning/execution docs, and selected `docs/reference/**`.
- Dependencies: X-OS-00 Task OS schemas/policies and X-OS-01 report-only command surfaces exist and are review-gated.
- Milestones: create X-OS-02 packet; add capability seeds/schemas; implement `capability status/scan/ledger/overclaim-report/validate`; add validation and six golden tasks; generate reports; refresh docs/export/context; run validation; stop at review.
- Blockers: none identified at planning time.
- Verification Intent: AIDE Lite capability commands, targeted X-OS-02 tests, six capability golden tasks, full AIDE Lite validation/test/selftest/eval where practical, export-pack/pack-status, verifier/review-pack, Harness validation, diff check, commit check, and targeted secret scan.
- Exit Criteria: X-OS-02 reaches `needs_review`, generated capability reports exist, no blocking overclaims are hidden, latest packet points to AIDE-CHECK-OS-01 or a real blocker repair, evidence is complete, and no apply, target, branch, release, provider/model, network, scheduler, worker, Runtime, host, UI, or app-surface behavior is introduced.
- Notes: X-OS-02 classifies evidence; it does not implement live product capabilities or promote report-only evidence to target truth.

### Queue ID: AIDE-BUILD-TESTJOB-SCHEMA-01

- Title: Minimal TestJob Schema
- Status: Needs Review
- Objective: build the next public protocol slice after accepted WorkerRun by adding a metadata-only TestJob schema/helper/projection/validation surface.
- Scope: `.aide/protocol/aide-test-job.schema.json`, `core/protocol/test_job.py`, thin `test-job status/project/validate` dispatch, focused tests, `.aide/reports/test-job/**`, queue evidence, and root indexes.
- Dependencies: accepted `minimal_worker_run_schema` plus existing envelope, EvidencePacket, and WorkUnit protocol slices.
- Verification Intent: focused TestJob tests, schema parse, Python compile, `test-job status/project/validate`, predecessor validations, task inspect/evidence, boundary scans, secret scans, diff check, and commit policy check.
- Exit Criteria: task stops at `needs_review`, TestJob reports and projections exist, focused tests pass, and no runtime/provider/network/GitHub/branch/apply behavior is introduced.
- Notes: This is schema/helper/projection/CLI only. Test Broker runtime, async execution, scheduler, leases, worker execution, WorkUnit lifecycle execution, Service, Commander, providers, and host surfaces remain deferred.

### Queue ID: AIDE-BUILD-RECONCILER-REPORTS-01

- Title: Report-Only Reconciler Reports
- Status: Needs Review
- Objective: add the first Reconciler slice as deterministic drift reporting after OKF acceptance.
- Scope: `core/reconciler/reconciler_reports.py`, thin `reconciler status/report/validate` dispatch, focused tests, `.aide/reports/reconciler/**`, queue evidence, and root planning/execution logs.
- Dependencies: accepted `minimal_okf_knowledge_bundle`, existing OKF, ReferenceID, EventRecord, evidence, and queue reports.
- Verification Intent: compile checks, focused Reconciler tests, Reconciler CLI status/report/validate, JSON parsing, predecessor validators, task inspect/evidence, broad validation, and diff checks.
- Exit Criteria: task stops at `needs_review`, Reconciler reports exist, findings are warning-class/report-only, validation passes with warnings, and no repair/runtime/provider/network/GitHub/branch/apply/release behavior is introduced.
- Notes: This slice detects drift only. CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime Reconciler service, repair behavior, and source truth mutation remain deferred.

### Queue ID: AIDE-CHECK-RECONCILER-REPORTS-01

- Title: Check Report-Only Reconciler Reports
- Status: Needs Review
- Objective: independently review `AIDE-BUILD-RECONCILER-REPORTS-01` as a check-only gate and confirm whether the minimal report-only Reconciler slice is coherent, bounded, validated, and honest about warnings and non-capabilities.
- Scope: `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/**`, `.aide/reports/reconciler-check/**`, `.aide/queue/index.yaml`, and root planning/execution logs.
- Dependencies: `AIDE-BUILD-RECONCILER-REPORTS-01` stopped at `needs_review`, generated Reconciler reports, focused Reconciler tests, and predecessor OKF/ReferenceID/EventRecord/TestJob/WorkerRun/EvidencePacket/WorkUnit/ContractEnvelope validators.
- Verification Intent: Reconciler CLI status/report/validate, focused Reconciler unittest discovery, JSON parsing, predecessor validators, task inspect/evidence checks for build and check tasks, broad validation, and Git diff checks.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, emits check evidence and reports, does not mutate the checked implementation or predecessor artifacts, and recommends `AIDE-ACCEPT-RECONCILER-REPORTS-01`.
- Notes: This check does not accept the build task, repair drift, refresh OKF, rewrite generated context, implement CapabilityManifest, or authorize runtime/provider/network/GitHub/branch/apply/release behavior.

### Queue ID: AIDE-ACCEPT-RECONCILER-REPORTS-01

- Title: Acceptance Review For Report-Only AIDE Reconciler
- Status: Needs Review
- Objective: accept the narrow `minimal_reconciler_reports` capability if the build/check chain remains coherent, evidence-backed, warning-only, and report-only.
- Scope: `.aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/**`, `.aide/reports/reconciler-accept/**`, `.aide/queue/index.yaml`, and root planning/execution logs.
- Dependencies: accepted OKF knowledge bundle, `AIDE-BUILD-RECONCILER-REPORTS-01`, `AIDE-CHECK-RECONCILER-REPORTS-01`, Reconciler reports, and predecessor validators.
- Verification Intent: acceptance JSON parsing, task inspect/evidence, Reconciler status/validate, predecessor validators, broad validation, Git diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `ACCEPTED_WITH_WARNINGS`, admits only `minimal_reconciler_reports`, preserves explicit non-capabilities, and recommends `AIDE-BUILD-CAPABILITY-MANIFEST-01`.
- Notes: This acceptance does not repair drift, refresh OKF, rewrite generated context, implement CapabilityManifest, or authorize runtime/provider/network/GitHub/branch/apply/release behavior.

### Queue ID: AIDE-BUILD-CAPABILITY-MANIFEST-01

- Title: Build Minimal CapabilityManifest
- Status: Needs Review
- Objective: add the first declaration-only CapabilityManifest slice after Reconciler acceptance by projecting accepted AIDE capabilities, evidence refs, status semantics, and non-capabilities into deterministic reports.
- Scope: `.aide/protocol/aide-capability-manifest.schema.json`, `core/protocol/capability_manifest.py`, thin `capability-manifest status/project/validate` dispatch, focused tests, `.aide/reports/capability-manifest/**`, queue evidence, index entry, and root planning/execution logs.
- Dependencies: accepted `minimal_reconciler_reports` plus existing ContractEnvelope, EvidencePacket, WorkUnit, WorkerRun, TestJob, ReferenceID, EventRecord, and OKF reports.
- Verification Intent: compile checks, focused CapabilityManifest tests, CapabilityManifest CLI status/project/validate, JSON parsing, predecessor validators, task inspect/evidence, broad validation, diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, projects 11 accepted capabilities, preserves accepted-with-warnings and metadata/report/projection/runtime/mutating semantics, and recommends `AIDE-CHECK-CAPABILITY-MANIFEST-01`.
- Notes: This build declares capability state only. ConformanceProfile, ConformanceResult, admission, adapter execution, runtime registry, scheduler, leases, supervisor, PatchTransaction, AdapterManifest, ContextPack v2, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, and production readiness remain deferred.

### Queue ID: AIDE-CHECK-CAPABILITY-MANIFEST-01

- Title: Independent Check For Minimal CapabilityManifest
- Status: Needs Review
- Objective: independently review `AIDE-BUILD-CAPABILITY-MANIFEST-01` as a check-only gate and confirm whether the minimal declaration-only CapabilityManifest slice is coherent, bounded, validated, and honest about warnings and non-capabilities.
- Scope: `.aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/**`, `.aide/reports/capability-manifest-check/**`, `.aide/queue/index.yaml`, and root planning/execution logs.
- Dependencies: `AIDE-BUILD-CAPABILITY-MANIFEST-01` stopped at `needs_review`, generated CapabilityManifest reports, focused CapabilityManifest tests, and predecessor Reconciler/OKF/ReferenceID/EventRecord/TestJob/WorkerRun/EvidencePacket/WorkUnit/ContractEnvelope validators.
- Verification Intent: CapabilityManifest CLI status/project/validate, focused CapabilityManifest unittest discovery, JSON parsing, predecessor validators, task inspect/evidence checks for build and check tasks, broad validation, and Git diff checks.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, emits check evidence and reports, does not mutate the checked implementation or predecessor artifacts, and recommends `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`.
- Notes: This check does not accept the build task, repair CapabilityManifest, implement ConformanceProfile, or authorize conformance/admission/execution/runtime/provider/network/GitHub/branch/apply/release behavior.

### Queue ID: AIDE-ACCEPT-CAPABILITY-MANIFEST-01

- Title: Accept Minimal CapabilityManifest
- Status: Needs Review
- Objective: perform a check-only acceptance gate for `AIDE-BUILD-CAPABILITY-MANIFEST-01` and `AIDE-CHECK-CAPABILITY-MANIFEST-01`, accepting only the declaration-only `minimal_capability_manifest` capability if the source chain remains coherent.
- Scope: `.aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/**`, `.aide/reports/capability-manifest-accept/**`, `.aide/queue/index.yaml`, and root planning/execution logs.
- Dependencies: Track B B1 barrier routing to Track A, `AIDE-BUILD-CAPABILITY-MANIFEST-01` at `PASS_WITH_WARNINGS`, `AIDE-CHECK-CAPABILITY-MANIFEST-01` at `PASS_WITH_WARNINGS`, generated CapabilityManifest reports, and predecessor protocol validators.
- Verification Intent: acceptance JSON parsing, CapabilityManifest JSON parsing, focused CapabilityManifest tests, CapabilityManifest CLI status/project/validate, task inspect/evidence checks for build/check/accept tasks, predecessor validators, broad validation, Git diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `ACCEPTED_WITH_WARNINGS`, accepts only `minimal_capability_manifest`, preserves declaration-only and non-capability boundaries, generates the first Track A prompt batch, and recommends `AIDE-BUILD-CONFORMANCE-PROFILE-01`.
- Notes: This acceptance does not implement ConformanceProfile, ConformanceResult, admission, adapter execution, PatchTransaction, AdapterManifest, ContextPack v2, runtime, provider/model/network/GitHub behavior, branch/worktree automation, target apply, active apply, release, or production readiness.

### Queue ID: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit

- Title: Current Truth And Root Authority Audit
- Status: Needs Review
- Objective: perform a fresh check-only structure audit before any file shuffle by reconciling live queue, repo intelligence, root recycling, refactor-map, generated-status, docs, and OKF posture into evidence-backed reports.
- Scope: `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/**`, `.aide/reports/structure-current-state.*`, `.aide/roots/latest-root-authority-candidates.*`, existing generated repo/root/refactor/status reports, `docs/planning/repository-structure/**`, and root planning/execution/documentation logs.
- Dependencies: existing Q37 repo intelligence, Q40 root recycling, Q42 move/salvage/path-alias, Task OS status, and Reconciler/OKF warning surfaces.
- Verification Intent: Git status/plan, Task OS status, repo inventory/status/validate, roots inventory/classify/plan/status/validate, refactor status/map-status/validate-map, task inspect/evidence, broad validate, and diff checks.
- Exit Criteria: task stopped at `needs_review`, recorded current root list, documentation-vs-queue drift, generated-status drift, root authority candidates, follow-up task recommendations, and no-forbidden-ops evidence.
- Notes: This audit does not move files, delete files, rewrite references, create top-level roots, promote generated outputs, repair docs, mutate branches, mutate target repos, call providers/models/network, or claim product/release readiness.

### Queue ID: AIDE-STRUCTURE-01-root-authority-contracts

- Title: Root Authority Contracts
- Status: Needs Review
- Objective: convert the candidate-only Track B structure audit into bounded root authority contracts, layout guidance, overlap reports, migration rules, validation planning, and follow-up prompt shells.
- Scope: `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/**`, `.aide/policies/root-authority.yaml`, `governance/root-authority.md`, `docs/reference/repository-layout.md`, `.aide/reports/root-authority-contracts.*`, `docs/planning/repository-structure/**`, `.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`, and root planning/execution/documentation logs.
- Dependencies: `AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` and existing no-apply repo intelligence, root recycling, refactor-map, source-of-truth, and queue policy records.
- Verification Intent: doctor, broad validate, Task OS status, task inspect/evidence, diff checks, and commit policy checks.
- Exit Criteria: root authority policy, governance note, repository layout reference, reports, and follow-up prompts exist; root authority map, overlap report, candidate target structure, migration rules, and validation plan are recorded; task stops at `needs_review`.
- Notes: This task does not move files, delete files, rewrite references, create aliases or shims, create top-level roots, promote generated outputs, accept CapabilityManifest, implement Track A protocol features, mutate branches, mutate target repos, call providers/models/network, or claim product/release readiness.

### Queue ID: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01

- Title: Report-Only Repository Layout Inventory
- Status: Needs Review
- Objective: inventory current `.aide` and `core` layout pressure for Track B without applying any rationalization.
- Scope: `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/**`, `.aide/reports/repo-layout/**`, `.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`, `docs/planning/repository-structure/**`, and root planning/execution/documentation logs.
- Dependencies: `AIDE-STRUCTURE-01-root-authority-contracts`, root authority policy, repository layout reference, repo status, roots status, and refactor map status.
- Verification Intent: doctor, broad validate, repo/roots/refactor status, Task OS status, task inspect/evidence, diff checks, and commit policy checks.
- Exit Criteria: inventory, recommendations, and migration-risk reports exist; `.aide` and `core` are classified; report/check/accept path risks are recorded; task stops at `needs_review`.
- Notes: This task does not move, delete, rename, rewrite, restructure `.aide/reports`, edit generated OKF pages, generate a rationalization/apply prompt, mutate branches, mutate target repos, call providers/models/network, or implement Track A product protocol.

### Queue ID: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01

- Title: AIDE Self-Management Charter
- Status: Needs Review
- Objective: define the doctrine that AIDE must manage AIDE as a repo using the same protocol, evidence, OKF, reconciler, queue, generated-output, migration-safety, and reviewed-transaction discipline it offers target repositories.
- Scope: `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/**`, `.aide/policies/self-management.yaml`, `docs/reference/aide-self-management.md`, `.aide/reports/self-management/**`, `governance/root-authority.md`, `.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`, and root planning/execution/documentation logs.
- Dependencies: `AIDE-BUILD-REPO-LAYOUT-INVENTORY-01`, root authority policy, repository layout reference, and current source-of-truth doctrine.
- Verification Intent: doctor, broad validate, Task OS status, task inspect/evidence, JSON parse, diff checks, and commit policy checks.
- Exit Criteria: self-management policy, reference doc, charter reports, object backlog, queue sequence, and evidence exist; task stops at `needs_review`.
- Notes: This task does not implement schemas, commands, generated-output ledgers, OKF regeneration, docs truth repair, queue acceptance, structure transactions, filesystem migration, runtime/provider behavior, branch mutation, target mutation, or release work.

### Queue ID: AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01

- Title: Check AIDE Self-Management Charter
- Status: Needs Review
- Objective: independently review `AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01` as a check-only gate and establish GovernanceFinding as a report convention only.
- Scope: `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/**`, `.aide/reports/self-management/check-self-management-charter.*`, `.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`, generated Task OS status reports, and root planning/execution logs.
- Dependencies: `AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`, self-management policy/reference/report artifacts, root-authority contracts, repo-layout inventory, and current queue truth.
- Verification Intent: doctor, broad validate, task inspect/evidence for the build and check tasks, JSON/YAML parsing, GovernanceFinding JSON parsing, Markdown/JSON finding agreement, diff checks, and commit policy checks.
- Exit Criteria: check stops at `needs_review`, records `PASS_WITH_WARNINGS`, emits structured GovernanceFinding records as report convention only, and recommends `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`.
- Notes: This check does not implement schemas, CLI commands, GovernanceFinding helpers, OKF regeneration, generated-output ledgers, doc truth reconcilers, file moves, reference rewrites, migration apply, runtime/provider/Gateway behavior, GitHub/network work, branch/worktree automation, release behavior, or target-repo mutation.

### Queue ID: AIDE-BUILD-MCP-SERVER-CONTRACT-01

- Title: Build Minimal Contract-Only MCP Projection
- Status: Needs Review
- Objective: build the first deterministic, contract-only MCP projection for AIDE, pinned to MCP protocol `2025-11-25` and JSON-RPC `2.0`, without implementing live server behavior.
- Scope: `.aide/protocol/aide-mcp-server-contract.schema.json`, `core/interop/**`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/test_aide_mcp_server_contract.py`, `.aide/interop/mcp/**`, `.aide/reports/mcp-server-contract/**`, `.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-01/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: `AIDE-BUILD-INTEROP-EXPORTS-01`, `AIDE-CHECK-INTEROP-EXPORTS-01`, and `AIDE-ACCEPT-INTEROP-EXPORTS-01` complete with `missing_evidence: 0`; accepted capability `static_interop_export_previews`; live queue routing to this task.
- Verification Intent: Python compile checks, focused MCP contract tests, `mcp-server-contract status/project/validate`, predecessor validators, task inspect/evidence, broad validation, JSON parsing, deterministic projection, source immutability, unsupported command probes, secret-like scans, diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, projects static contract/catalogue/fixture/report artifacts, preserves no-runtime and no-authority boundaries, and recommends `AIDE-CHECK-MCP-SERVER-CONTRACT-01`.
- Notes: This build does not start MCP, implement stdio or Streamable HTTP, authenticate clients, serve resources/prompts, execute tools, dispatch workers, call providers/models/network/Gateway/GitHub, apply PatchTransactions, mutate branches/worktrees/target repositories, implement A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service, scheduler, leases, supervisor, release, promotion, or production readiness.

### Queue ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

- Title: Repair Offline Read-Only AIDE-Dominium Seam v0 Second Pass
- Status: Needs Review
- Objective: close the ten remaining material gaps from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` without broadening the offline read-only seam.
- Scope: `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`, `core/interop/dominium/**`, `.aide/scripts/aide_lite.py`, focused seam tests, generated seam reports/fixtures, `.aide/interop/dominium/**`, `.aide/reports/dominium-readonly-seam-v0-repair-02/**`, `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check source chain, and `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` recommending this targeted repair.
- Verification Intent: Python compile, focused seam tests, Repair 01 and Repair 02 regressions, live seam project/validate/diff/demo, portability proof, JSON parsing, Dominium immutability, task inspect/evidence, broad validation, secret-like scan, diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, dispositions all ten gaps as repaired pending independent check, preserves explicit non-capabilities, and recommends exactly `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.
- Notes: This repair does not modify Dominium, invoke Dominium commands, implement Host runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, workers, preview/apply/rollback, target mutation, branch/worktree automation, GitHub mutation, release, or promotion.

### Queue ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

- Title: Independent Final Verification Of Dominium Read-Only Seam v0 Repair 02
- Status: Needs Review
- Objective: independently verify Repair 02's registry provenance, public schema, fixture replay, conformance evidence, operation observation, and portability claims without modifying the seam.
- Scope: `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/**`, `.aide/reports/dominium-readonly-seam-v0-repair-02-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check chain, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` at `1e8889eeb6cbee55ef9f4b42f6bf5d29405b4358`.
- Verification Intent: task-local independent harness, schema/source inspection, fixture replay, conformance semantic review, operation ledger review, runtime dependency review, portability review, Dominium immutability comparison, focused seam tests, broad validation, diff checks, secret scan, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `REQUEST_CHANGES`, preserves historical evidence, and recommends exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.
- Notes: This check does not repair implementation, alter seam schemas/code/tests/fixtures/generated seam outputs, modify Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, mutate repositories, create branches/worktrees, mutate GitHub, release, or promote.

### Queue ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

- Title: Final Hardened Repair Of Dominium Read-Only Seam v0
- Status: Needs Review
- Objective: close the 15 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` without broadening the offline read-only seam.
- Scope: `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`, `core/interop/dominium/**`, existing neutral protocol helpers only if necessary, `.aide/scripts/aide_lite.py`, focused seam tests, generated seam reports/fixtures, `.aide/interop/dominium/**`, `.aide/reports/dominium-readonly-seam-v0-repair-03/**`, `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check source chain, and `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` recommending this targeted repair with `missing_evidence: 0`.
- Verification Intent: Python compile, focused seam tests through Repair 03, direct regression probes for all 15 findings, live seam status/snapshot/project/validate/diff/demo, portability proof, operation trace recomputation, guard conformance, JSON parsing, Dominium immutability, task inspect/evidence, broad validation, secret-like scan, diff checks, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, dispositions all 15 findings as repaired pending independent check, preserves historical evidence, and recommends exactly `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.
- Notes: This repair does not accept the seam, modify Dominium, invoke Dominium commands, implement Host runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, workers, preview/apply/rollback, target mutation, branch/worktree automation, GitHub mutation, release, promotion, or the WorkUnit validation slice.

### Queue ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

- Title: Independent Final Check Of Dominium Read-Only Seam v0 Repair 03
- Status: Needs Review
- Objective: independently verify Repair 03's closure of the 15 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` without repairing or modifying the seam.
- Scope: `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/**`, `.aide/reports/dominium-readonly-seam-v0-repair-03-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check source chain, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` at `84a154c2f03b304a987a9f017cc48a0b22c3f6d6`.
- Verification Intent: source-chain inspection, independent schema/source inspection, fixture replay, conformance evidence review, operation trace and guard review, runtime manifest and portability review, typed refusal probes, Dominium immutability, focused seam tests, broad validation, diff checks, secret-like scan, task inspect/evidence, and commit policy check.
- Exit Criteria: satisfied for check completion; task stops at `needs_review` with `REQUEST_CHANGES`, 12 material findings, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` as the selected next task.
- Notes: This check did not repair implementation, alter public schemas/code/tests/fixtures/generated seam outputs/Repair 03 reports, modify Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, apply patches, mutate repositories, create branches/worktrees, mutate GitHub, release, promote, or begin the WorkUnit validation slice.

### Queue ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

- Title: Repair Dominium Read-Only Seam v0 Repair 04
- Status: Needs Review
- Objective: close the 12 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` without broadening the offline read-only seam.
- Scope: `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`, `core/interop/dominium/**`, existing neutral protocol helpers only if necessary, `.aide/scripts/aide_lite.py`, focused seam tests including Repair 04, generated seam reports/fixtures, `.aide/interop/dominium/**`, `.aide/reports/dominium-readonly-seam-v0-repair-04/**`, `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check source chain, and `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` recommending this targeted repair with `missing_evidence: 0`.
- Verification Intent: Python compile, focused seam tests through Repair 04, direct regression probes for all 12 findings, live seam status/snapshot/project/validate/diff/demo, portability proof, operation trace recomputation, guard conformance, JSON parsing, Dominium immutability, task inspect/evidence, broad validation, secret-like scan, diff checks, and commit policy check.
- Exit Criteria: satisfied for repair completion; task stops at `needs_review`, records `PASS_WITH_WARNINGS`, dispositions all 12 findings as repaired pending independent check, preserves historical evidence, and recommends exactly `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.
- Notes: This repair does not accept the seam, modify Dominium, invoke Dominium commands, implement Host runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, workers, preview/apply/rollback, target mutation, branch/worktree automation, GitHub mutation, release, promotion, or the WorkUnit validation slice.

### Queue ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

- Title: Final Bounded Independent Check Of Dominium Read-Only Seam v0 Repair 04
- Status: Needs Review
- Objective: independently verify Repair 04's closure of the exact 12 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` without repairing or modifying the seam.
- Scope: `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/**`, `.aide/reports/dominium-readonly-seam-v0-repair-04-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check chain, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` at `270b97dc66e477cd37a2f863c8604854a5e90bdf`.
- Verification Intent: source-chain inspection, independent schema/type/cross-kind checks, extension bypass checks, fixture strictness and negative fixture replay, actual CLI unsupported-operation matrix, Dominium no-write sequence, guard evidence review, operation trace/aggregate recomputation, manifest-driven portability review, regression sampling, full or split seam suites, task inspect/evidence, broad validation, diff checks, secret-like scan, and commit-policy check.
- Exit Criteria: task stops at `needs_review`; if no material findings remain it records `PASS_WITH_WARNINGS` and recommends exactly `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`, otherwise it records `REQUEST_CHANGES` and recommends exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
- Result: `REQUEST_CHANGES` with 4 material findings and 1 warning. The 12-finding closure matrix records 9 `CLOSED` and 3 `OPEN` dispositions, and the check recommends exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
- Notes: This check does not repair implementation, alter public schemas/code/tests/fixtures/generated seam outputs/Repair 04 reports, modify Dominium, invoke Dominium product commands, implement runtime/workbench/provider/worker behavior, apply patches, mutate repositories, create branches/worktrees, mutate GitHub, release, promote, accept the seam, create Repair 05, or begin the WorkUnit validation slice.

### Queue ID: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05

- Title: Final Repair Of Dominium Read-Only Seam v0
- Status: Needs Review
- Objective: repair only the four material blockers from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` without broadening the read-only seam or beginning acceptance.
- Scope: public seam schema, `core/interop/dominium/**`, focused seam tests, generated seam artifacts, `.aide/reports/dominium-readonly-seam-v0-repair-05/**`, `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: Repair 04 check at `0dd7eabc10508fe4a15965495314a15eeb02e495` with `REQUEST_CHANGES`, 4 material findings, and `missing_evidence: 0`.
- Verification Intent: schema surface audit, extension denylist matrix, real guard nonce probes, guard report digest recomputation, operation coverage derivation, focused Repair 05 tests, individual seam modules, seam CLI status/snapshot/project/validate/diff/demo, task inspect/evidence, broad validation, secret-like scan, and commit-policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, repairs all four findings pending independent check, and recommends exactly `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
- Result: `PASS_WITH_WARNINGS`; four findings are recorded as `REPAIRED_PENDING_INDEPENDENT_CHECK`.
- Notes: This repair does not accept the seam, create or run the Repair 05 check, begin acceptance, mutate Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, create branches/worktrees, mutate GitHub, release, promote, or begin the WorkUnit validation slice.

### Queue ID: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05

- Title: Final Independent Check Of Dominium Read-Only Seam Repair 05
- Status: Needs Review
- Objective: independently verify Repair 05's closure of the four material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` without repairing or modifying the seam.
- Scope: `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/**`, `.aide/reports/dominium-readonly-seam-v0-repair-05-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: Repair 05 build commit `05cb2b82980d1dbb9fb18524f0ba191a460b7962`, `missing_evidence: 0`, clean worktree, and route to this check.
- Verification Intent: evidence-local independent harness, schema surface traversal, production validation subprocess extension matrix, direct guard dispatcher probes, guard report digest recomputation, critical regression sampling, production tree hash comparison, Dominium immutability, task inspect/evidence, broad validation, diff checks, secret-like scan, and commit-policy check.
- Exit Criteria: task stops at `needs_review`, records `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, and recommends exactly `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.
- Result: `PASS_WITH_WARNINGS`; all four source findings are `CLOSED`.
- Notes: This check does not repair implementation, alter public schemas/code/tests/fixtures/generated seam outputs/Repair 05 reports, modify Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, create branches/worktrees, mutate GitHub, release, promote, accept the seam, or begin the WorkUnit validation slice.

### Queue ID: AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01

- Title: Accept Dominium Read-Only Seam v0
- Status: Needs Review
- Objective: accept only `dominium_readonly_seam_v0` after the final Repair 05 independent check reported zero material findings.
- Scope: `.aide/queue/AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01/**`, `.aide/reports/dominium-readonly-seam-v0-accept/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: Repair 05 check commit `cfecdd3f4802b3571919e8e0f8b3d12dd1c19229`, `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, and a clean worktree.
- Verification Intent: source-chain review, historical failure preservation, accepted scope review, final schema/evidence/portability/safety review, task inspect/evidence, broad validation, JSON parsing, secret-like scan, Dominium clean-state check, diff checks, and commit-policy check.
- Exit Criteria: task stops at `needs_review`, records `ACCEPTED_WITH_WARNINGS`, accepts `dominium_readonly_seam_v0`, preserves explicit non-capabilities, and recommends exactly `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
- Result: `ACCEPTED_WITH_WARNINGS`; next task prompt generated only.
- Notes: This acceptance does not modify seam implementation, alter public schemas/code/tests/fixtures/generated seam outputs/Repair 05 reports/check reports, modify Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, create branches/worktrees, mutate GitHub, release, promote, or begin the WorkUnit validation slice.
