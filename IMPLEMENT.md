# AIDE Implementation Log

## Purpose

`IMPLEMENT.md` is the engineering execution log for repository changes. It records what changed, why it changed, how it was verified, which risks were avoided, and what remains unresolved. It is not a changelog.

## What To Record

- the work item or prompt id
- the changed paths
- the rationale for the change
- notable design decisions and policy choices
- tradeoffs accepted
- verification that was run
- regressions or scope errors explicitly avoided
- remaining issues, blockers, or deliberate deferrals

## Entry Template

```md
## Work Item: PX

### Status

### Changed Paths

### Rationale

### Notable Design Decisions

### Tradeoffs

### Verification

### Regressions Avoided

### Remaining Issues
```

## Current Execution Log

## Work Item: AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

Completed as a projection-only build and awaiting independent check.

Changed:

- `core/protocol/trust_authorization.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-principal.schema.json`
- `.aide/protocol/aide-admission-record.schema.json`
- `.aide/protocol/aide-policy-decision.schema.json`
- `.aide/protocol/aide-capability-grant.schema.json`
- `.aide/protocol/aide-delegation-record.schema.json`
- `.aide/protocol/aide-revocation-record.schema.json`
- `.aide/protocol/aide-authorization-evaluation.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_trust_authorization_contract.py`
- `.aide/reports/trust-authorization-contract-v0/**`
- `.aide/queue/AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Implemented:

- projection-only `Principal`, `AdmissionRecord`, `PolicyDecision`,
  `CapabilityGrant`, `DelegationRecord`, `RevocationRecord`, and
  `AuthorizationEvaluation` records;
- exact-digest admission fields and explicit conformance/admission separation;
- policy and grant separation;
- narrowing-only delegation and revocation projection fields;
- deterministic authorization-evaluation fixtures with stable refusal codes;
- seven schema files and helper/schema alignment checks;
- AIDE Lite `trust status`, `trust project`, and `trust validate` commands;
- focused tests and generated reports.

Result:

```text
PASS_WITH_WARNINGS
proposed_capability: trust_and_authorization_contract_v0
missing_evidence: 0
```

Recommended next task:

```text
AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```

No live identity, credentials, secrets, OIDC/IAM, live policy engine, live
grants, runtime enforcement, worker execution, transaction approval,
Service/runtime behavior, provider/model/network calls, preview/apply/rollback,
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion was implemented.

## Work Item: AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01

Completed as an acceptance-only consolidation and awaiting review.

Changed:

- `.aide/queue/AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01/**`
- `.aide/reports/local-process-execution-host-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Accepted capability:

```text
local_process_execution_host_fixture_v0
```

Accepted meaning:

```text
bounded fixture-backed LocalProcessExecutionHost v0 reference capability
```

The acceptance preserves the complete source chain, including the historical
`REQUEST_CHANGES` check records, and records `ACCEPTED_WITH_WARNINGS`,
`material_finding_count: 0`, and `missing_evidence: 0`.

Recommended next task:

```text
AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```

This acceptance did not repair implementation, accept arbitrary command
execution, accept a generic worker harness, start autonomous AI worker behavior,
create Service/runtime or Workbench/MCP behavior, call provider/model/network
surfaces, implement preview/apply/rollback, mutate repositories, create
branches/worktrees, call GitHub, release, or promote.

## Work Item: AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02

Completed as a check-only review and awaiting acceptance.

Changed:

- `.aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02/**`
- `.aide/reports/local-process-execution-host-repair-02-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The independent check harness exercised the Repair 02 behavior as system under
test and found no remaining material findings.

Closed source findings:

- `local_host.path_escape_not_proven`
- `local_host.raw_event_stream_not_proven`
- `local_host.content_addressed_artifacts_not_proven`
- `local_host.workerrun_lifecycle_not_proven`

Result:

```text
PASS_WITH_WARNINGS
material_finding_count: 0
missing_evidence: 0
```

Recommended next task:

```text
AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```

This check did not repair implementation, accept the capability, modify
`RegisteredProcessExecutionProvider v0`, alter the accepted ExecutionHost
contract, mutate source repair reports, create `.aide.local` Service state,
start Workbench/MCP/provider/model/network behavior, mutate repositories, create
branches/worktrees, call GitHub, release, or promote.

## Work Item: AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02

Completed as a bounded repair build and awaiting independent check.

Changed:

- `core/execution/local_process_host.py`
- `.aide/scripts/tests/test_aide_local_process_execution_host.py`
- `.aide/reports/local-process-execution-host/**`
- `.aide/reports/local-process-execution-host-repair-02/**`
- `.aide/queue/AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Repair 02 targets the seven material assertions from
`AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01` and preserves the
already-closed disposable workspace and descriptor-scope findings.

Implemented:

- deterministic lexical path classification for POSIX, Windows drive, UNC, and
  rooted Windows path forms before filesystem resolution;
- stable separation of absolute, traversal, workspace escape, symlink/reparse,
  artifact path, and artifact link refusals;
- duplicate terminal event classification as
  `AIDE_LOCAL_PROCESS_HOST_DUPLICATE_TERMINAL_EVENT`;
- explicit WorkerRun state, terminal-state, and transition constants including
  `cancelled` and `reconciliation_required`;
- duplicate artifact declaration refusal;
- final artifact access revalidation and verified-byte content-addressed report
  persistence through temporary files and atomic replacement;
- expanded focused behavioral tests for path containment, event streams,
  artifact integrity, and lifecycle transitions.

Validation run so far:

- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"`: `PASS`
- `py -3 .aide/scripts/aide_lite.py local-process-execution-host run`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py local-process-execution-host validate`: `PASS_WITH_WARNINGS`

The proposed capability remains:

```text
local_process_execution_host_fixture_v0
```

Recommended next task:

```text
AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
```

No `RegisteredProcessExecutionProvider v0`, accepted ExecutionHost contract,
protocol schema, fixture worker, interop domain, host adapter, `.aide.local`
Service state, provider/model/network behavior, Workbench/MCP behavior,
preview/apply/rollback, repository mutation, branch/worktree automation, GitHub
mutation, release, or promotion was implemented or modified.

## Work Item: AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01

Completed as an acceptance-only consolidation and awaiting review.

Changed:

- `.aide/queue/AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01/**`
- `.aide/reports/execution-host-contract-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Accepted exactly:

```text
execution_host_contract_v0
```

The accepted scope is projection-only: ExecutionHost descriptor, run binding,
event, artifact, approval, usage, v0 operation vocabulary, false-boundary
fields, explicit non-capabilities, and the AIDE Lite
`execution-host status/project/validate` projection surface.

Recommended next task:

```text
AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```

No live ExecutionHost, LocalProcessExecutionHost, RemoteExecutionHost, worker
execution, worker harness, scheduler, provider/model/network call,
Service/runtime behavior, Workbench behavior, PreviewSession,
DevelopmentTransaction, PatchTransaction apply, repository mutation,
branch/worktree mutation, GitHub mutation, release, or promotion was accepted
or implemented.

## Work Item: AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01

Completed with warnings and awaiting acceptance review.

Changed:

- `.aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01/**`
- `.aide/reports/execution-host-contract-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check independently reviewed `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`
at commit `4a1f1aa` and found zero material findings. It verified the
projection-only contract boundary, schema kind discrimination, six projection
records, capability-execution separation, operation vocabulary, false-boundary
fields, explicit non-capabilities, CLI status/project/validate behavior,
parser rejection of `execution-host run`, report truthfulness, deterministic
reruns, and leak hygiene.

Accepted warnings:

- reduced independence because the same Codex thread also built the source task;
- projection-only contract with no live host;
- no separate external Draft 2020-12 validator installation;
- nested Python launcher selection differs on this host, so the harness used the
  active interpreter path and scrubbed it from evidence.

Recommended next task:

```text
AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01
```

No implementation was repaired. No live ExecutionHost, LocalProcessExecutionHost,
RemoteExecutionHost, worker execution, worker harness, scheduler,
provider/model/network call, Service/runtime behavior, Workbench behavior,
PreviewSession, DevelopmentTransaction, PatchTransaction apply, repository
mutation, branch/worktree mutation, GitHub mutation, release, or promotion was
implemented or accepted.

## Work Item: AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01

Completed with warnings and awaiting independent check.

Changed:

- `core/protocol/execution_host.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-execution-host.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_execution_host_contract.py`
- `.aide/reports/execution-host-contract/**`
- `.aide/queue/AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The build defines projection-only records for:

- `ExecutionHostDescriptor`
- `ExecutionHostRunBinding`
- `ExecutionHostEvent`
- `ExecutionHostArtifact`
- `ExecutionHostApproval`
- `ExecutionHostUsage`

The contract reserves the v0 operation vocabulary for future host work and
records `registered_process_execution_provider_v0` as a distinct deterministic
capability-execution provider rather than collapsing it into worker/session
execution.

Recommended next task:

```text
AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
```

No live ExecutionHost, LocalProcessExecutionHost, RemoteExecutionHost, worker
execution, worker harness, scheduler, provider/model/network call,
Service/runtime behavior, Workbench behavior, PreviewSession,
DevelopmentTransaction, PatchTransaction apply, repository mutation,
branch/worktree mutation, GitHub mutation, release, or promotion was
implemented.

## Work Item: AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

Completed as an acceptance-only consolidation and awaiting review.

Changed:

- `.aide/queue/AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/**`
- `.aide/reports/registered-process-execution-provider-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Accepted exactly:

```text
registered_process_execution_provider_v0
```

The accepted scope is deterministic, pre-registered, shell-free local process
capability execution with immutable specs, precondition checks, bounded
timeout/output capture, stream scrubbing, state-probe hooks, decoder hooks,
`ProcessExecutionReceipt`, `CapabilityOutcome`, and fail-closed behavior.

Recommended next task:

```text
AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
```

Warnings remain for unsupported cancellation, child-process-tree termination,
persistent idempotency, resource quotas, streaming artifact storage, unproven
non-Git state providers, and Eureka's implicit public-alpha smoke schema.

No arbitrary command execution, worker execution, ExecutionHost,
provider/model/network call, Service/runtime behavior, Workbench behavior,
preview/apply/rollback, repository mutation, branch/worktree automation, GitHub
mutation, release, or promotion was accepted or implemented.

## Work Item: AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01

Completed as a check-only independent review and awaiting review.

Changed:

- `.aide/queue/AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01/**`
- `.aide/reports/eureka-readonly-process-adapter-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check found zero material findings. Evidence confirms:

- source build commit `961add0` remains `PASS_WITH_WARNINGS` with missing evidence zero;
- provider core and neutral process protocol files were not changed by the Eureka build;
- provider core contains no Eureka-specific branches;
- selected Eureka command evidence originates from Eureka public-alpha smoke JSON;
- exactly one shell-free process launch is recorded in the source receipt;
- the final Eureka checkout remains clean at the pinned revision;
- state remained unchanged within declared Git probe coverage;
- Dominium, AIDE, and Eureka all reuse `registered_process_execution_provider_v0`;
- focused Eureka/provider/AIDE/Dominium regressions and broad validation passed;
- reports are scrubbed and provider acceptance remains unclaimed.

Recommended next task:

```text
AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```

No implementation repair, provider acceptance, second live Eureka invocation,
provider-core mutation, Eureka or Dominium mutation, provider/model/network call,
worker runtime, Service, Workbench implementation, preview/apply/rollback,
branch/worktree automation, GitHub mutation, release, or promotion was performed.

## Work Item: AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01

Completed with warnings and awaiting independent check.

Changed:

- `core/interop/eureka/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_eureka_readonly_process_adapter.py`
- `.aide/reports/eureka-readonly-process-adapter/**`
- `.aide/queue/AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The build adds a thin Eureka public-alpha read-only process adapter over the
unchanged proposed `RegisteredProcessExecutionProvider v0`. It deliberately
does not edit provider core, neutral process protocol files, the accepted AIDE
self-validation adapter, the Dominium adapter, or the Eureka checkout.

The requested `scripts/validate_public_alpha_readonly.py --json` command is not
present in the pinned local Eureka checkout. The build therefore selects
`scripts/public_alpha_smoke.py --json` as the narrowest existing Eureka-owned
read-only JSON command and records that substitution as a warning.

Recommended next task:

```text
AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01
```

No provider acceptance, generic arbitrary-command interface, provider/model or
network call, worker execution, Service/runtime, Workbench behavior,
preview/apply/rollback, source or target repository mutation, branch/worktree
automation, GitHub mutation, release, or promotion was performed.

## Work Item: AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Completed as a check-only independent review and awaiting review.

Changed:

- `.aide/queue/AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01/**`
- `.aide/reports/aide-self-validation-process-adapter-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check found zero material findings. Independent evidence confirms:

- the source build did not change the generic provider or neutral protocol files;
- the adapter uses the proposed provider without defining or forking it;
- the committed receipt records the exact AIDE Lite validate command with `shell: false`;
- one valid fake-runner proof launches exactly once;
- unsupported capability, wrong revision, missing workspace, missing executable, digest mismatch, and binding mismatch cases launch zero processes;
- successful output originates from AIDE Lite validate stdout, not a constructed success result;
- direct `aide_lite.py validate` does not recursively invoke the self-validation adapter;
- source build report validation causes no generated-report churn;
- focused self-adapter, generic provider, and Dominium parity tests pass;
- committed source reports/evidence are scrubbed and the provider remains proposed and unaccepted.

Recommended next task:

```text
AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01
```

No implementation repair, provider acceptance, Eureka build, arbitrary command
runner, provider-core mutation, Dominium or target-repository mutation,
provider/model/network call, worker runtime, Service, Workbench implementation,
preview/apply/rollback, branch/worktree automation, GitHub mutation, release, or
promotion was performed.

## Work Item: AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Completed with warnings and awaiting independent check.

Changed:

- `core/interop/aide/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_self_validation_process_adapter.py`
- `.aide/reports/aide-self-validation-process-adapter/**`
- `.aide/queue/AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The build adds a thin AIDE self-validation adapter over the unchanged proposed
`RegisteredProcessExecutionProvider v0`. The successful proof invokes the exact
allowlisted AIDE Lite validate process through the shared provider and records:

- `ProcessExecutionReceipt`;
- `CapabilityOutcome`;
- typed result mapping from AIDE Lite validate stdout;
- before/after AIDE state evidence with no mutation observed within declared
  probe coverage;
- EvidencePacket, EventRecord, projection, and human-readable reports.

Focused fake-runner tests cover exact argv, required environment constraints,
exactly-one process accounting, zero-launch unsupported and wrong-revision
refusals, timeout/malformed/nonzero mappings, deterministic projections,
scrubbing, and mutation detection.

Recommended next task:

```text
AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

The provider remains proposed and unaccepted. This build does not implement a
generic command runner, mutate provider core, add Eureka behavior, mutate
Dominium or target repositories, call provider/model/network services, run
workers, start Service or Workbench behavior, preview/apply/rollback, mutate
GitHub, create branches/worktrees, release, or promote.

## Work Item: AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Completed as a check-only independent repair review and awaiting review.

Changed:

- `.aide/queue/AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01/**`
- `.aide/reports/registered-process-execution-provider-v0-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check found zero remaining material findings from the repaired
registered-process provider. Independent behavior evidence confirms:

- binding mismatches launch zero processes;
- valid launch accounting and launch metadata are per invocation;
- decoder failures mark validation/evidence incomplete;
- state-probe failures fail closed without typed domain result preservation;
- process cancellation is explicitly unsupported in v0.

The check also reconfirms generic provider source cleanliness, Dominium parity,
scrubbed task/report surfaces, and proposed-only provider status.

Recommended next task:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

No implementation repair, provider acceptance, cancellation implementation, live
Dominium command rerun, Dominium or target-repository mutation,
provider/model/network call, worker runtime, Service, Workbench implementation,
preview/apply/rollback, branch/worktree automation, GitHub mutation, release, or
promotion was performed.

## Work Item: AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01

Completed as a docs-only tentative synthesis and awaiting review.

Changed:

- `docs/planning/product-vision/tentative-product-vision-roadmap.md`
- `.aide/reports/tentative-product-vision-roadmap/summary.md`
- `.aide/queue/AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

The document captures the current product direction as AIDE as universal
development control plane, compatibility kernel, governance fabric, and living
project twin. It keeps Omnigent as a candidate replaceable ExecutionHost
package, separates role-specific extension interfaces, explicitly separates
capability execution from worker execution, and records TranslationReceipt,
knowledge fabric, Project Twin, and preview-first mutation as future planning
concepts.

Recommended next task:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

No provider acceptance, repair-check execution, ExecutionHost implementation,
Omnigent integration, runtime, Workbench, worker execution, provider/model or
network call, live MCP/A2A/ACP behavior, preview/apply/rollback, Dominium or
target-repository mutation, branch/worktree automation, GitHub mutation, release,
or promotion was performed.

## Work Item: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Completed with warnings and awaiting independent repair check.

Changed:

- `core/execution/registered_process.py`
- `.aide/scripts/tests/test_aide_registered_process_provider.py`
- `.aide/reports/registered-process-execution-provider-v0-repair/**`
- `.aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The repair closes the five material findings from
`AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`:

- mismatched capability/provider/spec bindings now fail closed before launch;
- valid launch receipts now report current invocation launch count and metadata;
- decoder exceptions and undecoded outcomes no longer report complete
  validation/evidence axes;
- state-probe failures fail closed without preserving typed domain results;
- process cancellation is explicitly declared unsupported in v0.

Focused provider tests and Dominium parity tests pass. The provider remains
proposed and unaccepted.

Recommended next task:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

No provider acceptance, cancellation implementation, live Dominium command
rerun, Dominium or target-repository mutation, provider/model/network call,
worker runtime, Service, Workbench implementation, preview/apply/rollback,
branch/worktree automation, GitHub mutation, release, or promotion was
performed.

## Work Item: AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

Completed as a check-only independent review and awaiting repair.

Changed:

- `.aide/queue/AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/**`
- `.aide/reports/registered-process-execution-provider-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `REQUEST_CHANGES`. The check confirms source build evidence
completeness, generic provider/protocol domain-scan cleanliness, no committed
absolute-path or secret-like leakage in source build reports/evidence, and
Dominium parity preservation.

It records five material provider safety findings:

- mismatched capability/provider bindings still launch a process;
- receipt launcher accounting and launch metadata are cumulative or stale when
  a provider instance is reused;
- decoder exceptions report complete validation and evidence axes;
- state-probe failures can still report a complete typed result;
- cancellation is neither implemented nor declared as an explicit
  non-capability.

Recommended next task:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

No implementation repair, provider acceptance, live Dominium rerun, Dominium or
target-repository mutation, provider/model/network call, worker runtime,
Service, Workbench implementation, preview/apply/rollback, branch/worktree
automation, GitHub mutation, release, or promotion was performed.

## Work Item: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

Completed with warnings and awaiting independent review.

Changed:

- `core/protocol/process_invocation.py`
- `core/protocol/execution_receipt.py`
- `core/protocol/__init__.py`
- `core/execution/**`
- `core/interop/dominium/registered_validation_backend.py`
- `.aide/scripts/tests/test_aide_registered_process_provider.py`
- `.aide/scripts/tests/test_aide_dominium_registered_validation_backend.py`
- `.aide/reports/registered-process-execution-provider-v0/**`
- `.aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The proposed capability is:

```text
registered_process_execution_provider_v0
```

The provider introduces neutral CapabilityInvocation, CapabilityBinding,
ExecutionProvider, RegisteredProcessExecutionProvider, OutputDecoder,
CapabilityOutcome, ProcessExecutionReceipt, and evidence/event projection
shapes. The generic provider owns shell-free bounded process launch mechanics,
preconditions, timeout, controlled environment, state probes, stream scrubbing,
decoder invocation, neutral receipts, and fake-runner test seams.

The Dominium registered validation backend is now a thin domain adapter over
the generic provider. The accepted observable boundary is preserved: one
launcher call, exact argv, `shell=False`, typed Dominium refusal semantics,
declared probe-scoped no-mutation observation, and no aggregate-validation
success claim. The live Dominium command was not rerun.

Recommended next task:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```

This build does not accept the provider, implement a universal execution
ontology, arbitrary-command CLI, runtime, worker, provider/model/network
behavior, preview/apply/rollback, target-repository mutation, branch/worktree
automation, GitHub mutation, release, or promotion.

## Work Item: AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Completed as acceptance-only metadata work and awaiting review.

Changed:

- `.aide/queue/AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/**`
- `.aide/reports/dominium-registered-validation-backend-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is exactly:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

This accepts one narrowly registered Dominium validation command-boundary
invocation through one bounded local process boundary with repository preflight,
exact argv, `shell=False`, environment constraints, timeout, typed result or
refusal capture, declared state-probe comparison, evidence, and event
projection.

Preserved warnings:

- the observed domain outcome was a typed refusal;
- aggregate validation did not succeed and aggregate validation execution is not accepted;
- service-adapter entry is not accepted without independent Dominium-produced evidence;
- mutation observation is limited to declared probe coverage;
- local Dominium remains clean but behind `origin/main`.

Recommended next task:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```

No implementation code, active backend reports, predecessor evidence, Dominium
files, live Dominium invocation, generic provider behavior, provider/model/network
call, worker runtime, Service, Workbench implementation, preview/apply/rollback,
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion was performed.

## Work Item: AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01

Completed as a check-only task and awaiting review.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01/**`
- `.aide/reports/dominium-registered-validation-backend-relabel-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS` with `material_finding_count: 0`. The check
verified that active reports use:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

It also verified that the old label appears only as superseded or historical
data, predecessor evidence was not rewritten, boundary classifications remain
separate, the domain result is still a typed refusal, and aggregate validation
success is not claimed.

Recommended next task:

```text
AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```

No implementation repair, active report rewrite, live Dominium command rerun,
Dominium mutation, generic provider behavior, provider/model/network call,
worker runtime, Service, Workbench implementation, preview/apply/rollback,
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion was performed.

## Work Item: AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01

Completed with warnings and awaiting independent review.

Changed:

- `core/interop/dominium/registered_validation_backend.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_registered_validation_backend.py`
- `.aide/reports/dominium-registered-validation-backend/**`
- `.aide/reports/dominium-registered-validation-backend-relabel/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The active capability label is now:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

The prior label `live_dominium_validation_command_readonly_v0` is preserved as
superseded or historical data only. Active reports now separate process start,
launcher call count, structured output parsing, registered command boundary,
service-adapter boundary, aggregate-validation execution, aggregate-validation
success, typed refusal, and probe-scoped mutation observation.

The active reports were regenerated from saved invocation artifacts. The live
Dominium CLI was not rerun and the Dominium checkout remained unchanged.

Recommended next task:

```text
AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
```

No capability acceptance, generic provider extraction, provider/model/network
call, worker runtime, Service, Workbench implementation, preview/apply/rollback,
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion was performed.

## Work Item: AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Completed as a check-only task and awaiting review.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/**`
- `.aide/reports/dominium-registered-validation-backend-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `REQUEST_CHANGES`. The independent check proves the live
registered Dominium command boundary, typed refusal origin, no-fixture executor
claim, Dominium service-adapter refusal path, unchanged Dominium state, and
scrubbed generated reports. It records one material finding: the proposed
capability label `live_dominium_validation_command_readonly_v0` should be
relabelled before acceptance because the observed result is a typed refusal,
not successful aggregate validation.

Recommended next task:

```text
AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
```

The check did not repair implementation, rerun the live Dominium CLI, mutate
Dominium, broaden dispatch, implement Workbench/Service/runtime behavior, call
providers/models/network, run workers, preview/apply/rollback, mutate
repositories, create branches/worktrees, mutate GitHub, release, or promote.

## Work Item: AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Completed for review as a bounded build task.

Changed:

- `.aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/**`
- `.aide/reports/dominium-registered-validation-backend/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `core/interop/dominium/registered_validation_backend.py`
- `core/interop/dominium/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_registered_validation_backend.py`

This task builds a separate registered validation backend so the accepted
`fixture_backed_dominium_validation_adapter` remains unchanged. The intended
proof is one shell-free subprocess invocation of the Dominium-owned
`dominium.validation.run` CLI boundary against a pinned clean local checkout,
with normalized AIDE evidence and no Dominium mutation.

Result:

```text
PASS_WITH_WARNINGS
```

The backend entered the Dominium CLI process exactly once and parsed stdout JSON
from `dominium.validation.run`. Dominium returned a typed refusal because the
aggregate validation suite service is not bound in this Workbench validation
slice. That proves the live command boundary and service-adapter path were
reached; it does not prove successful aggregate validation.

Validation:

- focused fake-runner tests passed, 7 tests;
- report-only backend validation passed with `PASS_WITH_WARNINGS`;
- strict report/evidence local-path and secret-like scan found 0 findings;
- Dominium remained clean and unchanged;
- broad `aide_lite.py validate` passed.

Recommended next task:

```text
AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```

## Work Item: AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Completed for review as an acceptance task.

Changed:

- `.aide/queue/AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/**`
- `.aide/reports/dominium-workunit-validation-slice-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is exactly:

```text
fixture_backed_dominium_validation_adapter
```

Acceptance preserves the source check's authority distinction: the completed
slice proves a registered, local, read-only, fixture-backed adapter path and
does not prove live Dominium-owned `dominium.validation.run` command execution.

No implementation, fixture, build report, check report, Dominium checkout,
Workbench, Service/runtime, worker, provider/model/network, preview/apply,
rollback, source or target mutation, branch/worktree automation, GitHub
mutation, release, or promotion behavior was modified or accepted.

Recommended next task:

```text
AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```

## Work Item: AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Completed for review as a check-only independent task.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/**`
- `.aide/reports/dominium-workunit-validation-slice-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS` with `material_finding_count: 0`. The check
independently verifies the source build at
`8d8f511c77388b96118eb530f5361090b66911c1`, instruments the fixture-backed
success executor, verifies unsupported and malformed requests do not enter that
executor, recomputes workspace digests, checks deterministic clean reruns,
scans for local path and secret leakage, and validates the generated
ContextDescriptor, ContextPack, WorkUnit, EvidencePacket, EventRecord, and
false-boundary claims.

The check deliberately classifies the achieved capability as:

```text
fixture_backed_dominium_validation_adapter
```

It does not prove live Dominium-owned `dominium.validation.run` execution, and
acceptance must not claim that stronger capability.

Recommended next task:

```text
AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

## Work Item: AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Completed for review as a bounded build task.

Changed:

- `core/interop/dominium/workunit_validation.py`
- `core/interop/dominium/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_workunit_validation_slice.py`
- `.aide/fixtures/dominium-workunit-validation-slice/**`
- `.aide/reports/dominium-workunit-validation-slice/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The build adds a narrow Dominium WorkUnit
validation slice that creates a temporary fixture workspace, projects a
ContextDescriptor and ContextPack, builds a WorkUnit, performs exactly one
registered local read-only `dominium.validation.run` capability invocation, and
records the typed result as EvidencePacket, EventRecord, and deterministic
read-only projection evidence.

The adapter intentionally refuses unsupported capability IDs with typed refusal
data and does not provide a shell fallback, private tool bypass, broad Dominium
dispatcher, provider/model/network call, worker execution, Workbench behavior,
Service runtime, preview/apply/rollback, PatchTransaction apply, repository
mutation, branch/worktree automation, GitHub mutation, release, or promotion.

Verification passed for compile, focused WorkUnit validation tests,
`dominium-workunit-validation status/run/validate`, task inspect/evidence,
WorkUnit inspect, diff checks, broad `aide_lite.py validate`, and the latest
Repair 04/05 Dominium seam suites. The full historical
`test_aide_dominium_readonly_seam*.py` discovery and four older exact-pattern
historical seam modules timed out under bounded reruns, so those are recorded as
warning-class unproven checks rather than passes.

Recommended next task:

```text
AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01

Completed for review as a check-only independent repair verification task.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `REQUEST_CHANGES`. The check verified the local repair commit `30931ba1f17b1bc4d9d2b9b12ef18133831ad8fd`, source build/check/repair evidence completeness, and Dominium immutability, then used task-local independent harnesses to review the repaired seam without importing production seam validation, production conformance, production negative-fixture mutators, or repair finding-disposition logic as material proof.

The repair check closed 13 of the 18 original material finding rows and left 5 finding rows open, with 10 material gaps: incomplete diagnostic/refusal projection disclosure, insufficient public schema constraints for kind-specific `spec` fields and status facts, one or more negative fixture replay failures, missing required conformance assertion fields, incomplete operation ledger counts/coverage, and cross-process determinism failure.

No repair, acceptance, production seam modification, generated seam output rewrite, repair report rewrite, Dominium command invocation, Dominium mutation, runtime/workbench/provider/worker behavior, patch apply, target mutation, branch/worktree automation, GitHub mutation, release, or promotion was performed.

Recommended next task:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02
```

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01

Completed for review as a check-only independent adversarial task.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/**`
- `.aide/reports/dominium-readonly-seam-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `REQUEST_CHANGES`. The check found 18 bounded material defects in the offline read-only seam build, including repository lookalike identity acceptance, stale final bundle self-digest, insufficient public schema constraints, non-replayable negative fixtures, aggregate-only conformance evidence, unmeasured demo elapsed time, undisclosed diagnostic/refusal truncation, and validator gaps for mixed revisions, snapshot digest corruption, singleton cardinality, dangling refs, wrong semantic ownership, mutation capability IDs, duplicate event sequences, arbitrary diagnostic severity, invented refusals, and missing required fields.

The check confirmed current remote Dominium `main` still equals `623ab08ae8c867719d5abc2e60c16a6fbb37b313`, ran supported seam commands against a temporary AIDE root, verified unsupported verbs refuse closed, and confirmed Dominium status/refs/index/selected pinned source bytes were unchanged.

No repair, acceptance, production seam modification, build report rewrite, Dominium command invocation, Dominium mutation, runtime/workbench/provider/worker behavior, patch apply, target mutation, release, or promotion was performed.

Recommended next task:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01
```

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01

Completed for review as a milestone-sized build task.

Changed:

- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `core/interop/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The build adds an offline read-only seam that snapshots the pinned Dominium checkout, projects HostManifest, HostCapabilitySet, WorkspaceDescriptor, ContextDescriptor, ArtifactReference, DiagnosticProjection, RefusalProjection, EvidenceReferenceSet, EventEnvelope, DominiumBridgeManifest, and a deterministic SeamBundle, then validates and demonstrates the projection without mutating Dominium.

The implementation keeps `aide_lite.py` as thin dispatch and puts seam behavior in `core/interop/dominium/`. The CLI supports `dominium-seam status`, `snapshot`, `project`, `validate`, `diff`, and `demo`; unsupported runtime or mutation verbs refuse closed.

Verification includes Python compilation, all six seam CLI paths, deterministic projection comparison, source digest recomputation, a full offline demo, 33 fixtures, 20 conformance expectations, and 108 focused tests. Dominium remained unchanged at `## main...origin/main [behind 24]`, with source mutation count zero and forbidden operation count zero.

No Dominium command invocation, fetch, pull, checkout, remote-ref update, Host runtime, Host SDK, Workbench implementation, bridge runtime, service, database runtime, transport, provider/model/network call, worker execution, PatchTransaction apply, preview/apply/rollback, target-repository mutation, branch/worktree automation, GitHub mutation, release, or promotion was implemented or authorized.

Recommended next task:

```text
AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01
```

## Work Item: AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01

Completed for review as an acceptance task.

Changed:

- `.aide/queue/AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01/**`
- `.aide/reports/dominium-integration-charter-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted planning artifact is `aide_dominium_integration_charter_v0`: the ownership, mapping, compatibility, authority, recovery, and task-sequencing plan for a future AIDE-Dominium integration.

The acceptance verified the A2A predecessor, charter build, and independent check source chain; confirmed `missing_evidence: 0` for source tasks; confirmed check material findings remain zero; confirmed current remote Dominium `main` still equals `623ab08ae8c867719d5abc2e60c16a6fbb37b313`; and preserved warnings that local Dominium is behind remote and that the charter is planning-only.

No charter repair, Dominium modification, downstream queue task materialization, Host Contract, Dominium Bridge, Workbench, runtime, service, provider/model/network call, worker execution, preview, apply, rollback, repository mutation, branch/worktree automation, GitHub mutation, release, promotion, or cross-repository integration was performed or authorized.

Recommended next task:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01
```

## Work Item: AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01

Completed for review as a check-only task.

Changed:

- `.aide/queue/AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01/**`
- `.aide/reports/dominium-integration-charter-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check verifies that the charter-pinned Dominium snapshot at `c92b386027890c1bbf14aef6eaafe0357b7b03dd` is stale versus current remote `main` at `623ab08ae8c867719d5abc2e60c16a6fbb37b313`, 24 commits ahead, but the staleness is warning-class because canonical queue, canon, planning, contract, and audit inputs remain byte-identical and the changed public docs are derived summaries that defer to higher-authority artifacts.

The check found zero material findings. It verified the AIDE source chain, charter evidence completeness, Dominium remote delta, source-of-truth hierarchy, semantic ownership, namespaces, object mapping, command/refusal/diagnostic/evidence/event mappings, transaction layering, host/bridge/provider/experience boundaries, Workbench non-authority, compatibility, security, recovery, first read-only seam, first validation slice, critical path, parallel lane, turn-size policy, report consistency, and explicit non-capabilities.

No charter repair, Dominium file modification, downstream queue task materialization, Host Contract, Dominium Bridge, Workbench, runtime, service, provider/model/network call, worker execution, preview, apply, rollback, repository mutation, branch/worktree automation, GitHub mutation, release, or promotion was performed or authorized.

Recommended next task:

```text
AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01
```

## Work Item: AIDE-DOMINIUM-INTEGRATION-CHARTER-01

Completed for review as a planning-only charter task.

Changed:

- `.aide/queue/AIDE-DOMINIUM-INTEGRATION-CHARTER-01/**`
- `.aide/reports/dominium-integration-charter/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The charter pins AIDE at commit `7e80ea2f18b404af68a752502a7491fceaa7abea` and the local Dominium checkout at commit `c92b386027890c1bbf14aef6eaafe0357b7b03dd`, records Dominium's current task as `PRESENTATION-CONTRACT-01`, next task as `PROJECTION-CONFORMANCE-01`, alternate next task as `WORKBENCH-SHELL-READONLY-01`, and broad feature work as blocked.

The charter freezes ownership and mapping law for AIDE, Dominium, Domino, and Workbench without flattening their authority models. It defines the first read-only seam and first validation slice as future build/check/accept programs, and records the downstream critical path plus a parallel read-only RepoGraph lane as planning graph nodes only.

No Dominium file, Domino file, Workbench source, sibling repository, downstream queue directory, branch, worktree, remote ref, GitHub state, Host Contract implementation, Dominium Bridge implementation, Workbench implementation, runtime, service, provider/model/network call, worker execution, command invocation, PatchTransaction apply, target-repository mutation, release, or promotion was performed or authorized.

Recommended next task:

```text
AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01
```

## Work Item: AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01

Completed for review as an acceptance task.

Changed:

- `.aide/queue/AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01/**`
- `.aide/reports/a2a-agent-card-contract-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is `minimal_a2a_agent_card_contract`: deterministic A2A 1.0 AgentCard contract representation, version pinning, a standards-clean non-publishable fixture, supportedInterfaces, candidate-skill governance outside the official AgentCard, structural validation, deterministic projection, inspection, reporting, conformance expectations, and refusal metadata.

The original failed independent check remains historical evidence with eight material findings. The bounded repair and independent repair check remain preserved, and the repair check reports zero remaining material findings.

No A2A endpoint, `.well-known` publication, agent registration, authentication, authorization, task submission, task delegation, worker execution, provider/model/network call, Host Contract, Dominium Bridge, Workbench, Runtime, Service, PatchTransaction apply, branch/worktree automation, GitHub mutation, release, promotion, or target-repository mutation was implemented or authorized.

Recommended next task:

```text
AIDE-DOMINIUM-INTEGRATION-CHARTER-01
```

## Work Item: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01

Completed for review as an independent check task.

Changed:

- `.aide/queue/AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01/**`
- `.aide/reports/a2a-agent-card-contract-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check independently verified that the eight original A2A AgentCard findings remain repaired: external A2A pins exist, the official AgentCard projection is standards-clean for the supported subset, `supportedInterfaces` is present, provider is omitted, legacy top-level fields are absent, unsupported capability fields are absent, AIDE candidate skill governance is outside official AgentSkill objects, and no unimplemented skills are advertised in official `skills`.

The check preserved the original failed check, repair reports, A2A implementation, schema, focused tests, fixtures, generated build reports, and no-runtime boundaries. No live endpoint, well-known publication, agent registration, authentication, authorization, task delegation, worker execution, provider/model/network call, Host Contract, Dominium Bridge, Workbench, Runtime, Service, PatchTransaction apply, branch/worktree automation, GitHub mutation, release, promotion, or target-repository mutation was performed.

Recommended next task:

```text
AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01
```

## Work Item: AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01

Completed for review as a bounded repair task.

Changed:

- `core/interop/a2a_agent_card_contract.py`
- `.aide/protocol/aide-a2a-agent-card-contract.schema.json`
- `.aide/scripts/tests/test_aide_a2a_agent_card_contract.py`
- `.aide/interop/a2a/**`
- `.aide/reports/a2a-agent-card-contract/**`
- `.aide/queue/AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01/**`
- `.aide/reports/a2a-agent-card-contract-repair/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The repair adds explicit A2A `1.0.0` specification and `1.0` protocol pins, emits a standards-clean non-publishable A2A AgentCard fixture with one `.invalid` HTTPS JSON-RPC supported interface, omits provider by default, removes legacy top-level URL and extended-card fields, removes unsupported `stateTransitionHistory`, moves AIDE governance fields to outer candidate-skill metadata, and advertises zero official skills while preserving four candidate skills.

The validator and focused tests now fail closed for reintroductions of the eight original material defects. No failed-check evidence was rewritten.

No live A2A endpoint, well-known publication, agent registration, authentication, authorization, task delegation, streaming, push notification runtime, AgentCard signing, worker execution, provider/model/network call, Host Contract, Dominium Bridge, Workbench, Runtime, Service, PatchTransaction apply, branch/worktree automation, GitHub mutation, release, promotion, or target-repository mutation was implemented.

Recommended next task:

```text
AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01
```

## Work Item: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01

Completed for review as a check task.

Changed:

- `.aide/queue/AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01/**`
- `.aide/reports/a2a-agent-card-contract-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `FAILED_VALIDATION`. The independent check found eight material A2A standards-alignment defects in the contract-only Agent Card projection: missing external A2A version pinning, missing `supportedInterfaces`, legacy/null top-level URL shape, null provider URL, legacy extended-card placement, unsupported capability field, AIDE governance fields inside AgentSkill objects, and advertised-but-unimplemented skills in an official-looking skills array.

No A2A implementation repair, schema/helper/test change, projected artifact rewrite, endpoint publication, agent registration, authentication, task delegation, worker execution, provider/model/network call, Host Contract, Dominium Bridge, Workbench, Runtime, Service, PatchTransaction apply, branch/worktree automation, GitHub mutation, release, promotion, or target-repository mutation was performed.

Recommended next task:

```text
AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01
```

## Work Item: AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01

Completed for review as a build task.

Changed:

- `.aide/protocol/aide-a2a-agent-card-contract.schema.json`
- `core/interop/a2a_agent_card_contract.py`
- `core/interop/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_a2a_agent_card_contract.py`
- `.aide/interop/a2a/**`
- `.aide/reports/a2a-agent-card-contract/**`
- `.aide/queue/AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The task builds the
`minimal_a2a_agent_card_contract` slice as a deterministic contract-only
projection for an inactive A2A agent-card shape, read-only future skill
catalogue, security/authentication boundary, refusal mappings, conformance
expectations, structural validation, inspection, and reporting.

No A2A endpoint, agent registration, authentication, authorization, task
delegation, worker execution, provider/model/network call, Host Contract,
Dominium Bridge, Workbench, Runtime, Service, PatchTransaction apply,
branch/worktree automation, GitHub mutation, release, promotion, or
target-repository mutation was implemented.

Recommended next task:

```text
AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01
```

## Work Item: AIDE-ACCEPT-MCP-SERVER-CONTRACT-01

Completed for review as an acceptance task.

Changed:

- `.aide/queue/AIDE-ACCEPT-MCP-SERVER-CONTRACT-01/**`
- `.aide/reports/mcp-server-contract-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is
`minimal_mcp_server_contract`: a deterministic, contract-only projection of the
pinned MCP `2025-11-25` and JSON-RPC `2.0` subset for AIDE catalogues,
fixtures, refusal mappings, transport expectations, authorization expectations,
conformance expectations, structural validation, inspection, and reporting.

The original failed check remains historical evidence. Its two material
findings were repaired and independently rechecked: absent pagination cursor
fields are omitted, present cursor values must be strings, and the
resource-not-found fixture uses `-32002` while custom AIDE refusal codes remain
unchanged.

No MCP schema, helper, focused test, fixture, build report, failed-check report,
repair report, repair-check report, accepted Interop Export artifact, runtime,
provider, worker, host, VCS, network, GitHub, release, or target-repository file
was modified. No live MCP server, transport, endpoint, authorization, resource
serving, prompt serving, tool execution, worker dispatch, provider/model call,
PatchTransaction apply, branch/worktree automation, A2A, Host Contract,
Dominium Bridge, Workbench, Runtime, Service, release, promotion, or production
readiness was implemented.

Recommended next task:

```text
AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01
```

## Work Item: AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01

Completed for review as an independent repair check.

Changed:

- `.aide/queue/AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01/**`
- `.aide/reports/mcp-server-contract-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS` with zero material findings. The check
independently verified that absent pagination cursor fields are omitted, present
cursor values are strings, `resource-not-found-refusal.json` uses `-32002`, and
custom AIDE refusal codes remain unchanged.

The check also verified temporary invalid cursor/error mutations fail
validation, JSON-RPC fixture shape remains intact, focused MCP tests pass,
projection remains deterministic, accepted Interop Export artifacts and failed
check reports remain unchanged, and no runtime behavior was added.

No MCP helper, schema, focused test, fixture, build report, repair report,
failed-check report, accepted predecessor artifact, generated OKF page, runtime,
provider, worker, host, VCS, network, GitHub, release, or target-repository file
was modified.

Recommended next task:

```text
AIDE-ACCEPT-MCP-SERVER-CONTRACT-01
```

## Work Item: AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01

Completed for review as a bounded repair task.

Changed:

- `core/interop/mcp_server_contract.py`
- `.aide/scripts/tests/test_aide_mcp_server_contract.py`
- `.aide/interop/mcp/fixtures/*list-request.json`
- `.aide/interop/mcp/fixtures/*list-result.json`
- `.aide/interop/mcp/fixtures/resource-not-found-refusal.json`
- `.aide/reports/mcp-server-contract/fixture-index.*`
- `.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01/**`
- `.aide/reports/mcp-server-contract-repair/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The repair fixes the two material findings from
`AIDE-CHECK-MCP-SERVER-CONTRACT-01`: optional pagination cursor fields are now
omitted when absent and validated as strings when present, and the
resource-not-found fixture now uses the pinned MCP Resources error code
`-32002`.

The failed independent check was preserved. The repair also adds focused
regressions for null and non-string cursors, valid opaque string cursors,
resource-not-found code enforcement, preserved custom AIDE refusal codes,
JSON-RPC identity, ID alignment, deterministic projection, and unsupported
command rejection.

No live MCP server, transport, endpoint, authorization, resource serving,
prompt serving, tool execution, worker dispatch, provider/model/network call,
A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service,
PatchTransaction apply, branch/worktree automation, GitHub mutation, release,
promotion, or target-repository mutation was implemented.

Recommended next task:

```text
AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01
```

## Work Item: AIDE-CHECK-MCP-SERVER-CONTRACT-01

Completed for review as an independent check task.

Changed:

- `.aide/queue/AIDE-CHECK-MCP-SERVER-CONTRACT-01/**`
- `.aide/reports/mcp-server-contract-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `FAILED_VALIDATION`. The source chain is valid and the build
evidence reports `missing_evidence: 0`, but independent fixture review found
two material MCP standards-alignment defects:

- list request/result fixtures emit `null` for optional `cursor` or
  `nextCursor` fields;
- `resource-not-found-refusal.json` uses `-32043` instead of the pinned MCP
  resource-not-found code `-32002`.

The check did not repair the MCP schema, helper, tests, fixtures, build reports,
or accepted predecessor records. No server, transport, endpoint, authorization,
resource serving, prompt serving, tool execution, worker dispatch,
provider/model/network call, PatchTransaction apply, branch/worktree
automation, GitHub mutation, release, promotion, or target-repository mutation
occurred.

Recommended next task:

```text
AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01
```

## Work Item: AIDE-ACCEPT-INTEROP-EXPORTS-01

Completed for review as an acceptance task.

Changed:

- `.aide/queue/AIDE-ACCEPT-INTEROP-EXPORTS-01/**`
- `.aide/reports/interop-exports-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is
`static_interop_export_previews`: deterministic, manifest-backed, preview-only
interop artifacts for AGENTS, Claude, Copilot, Aider, MCP manifest, and A2A
agent-card formats.

Acceptance does not install instruction files, overwrite live `AGENTS.md` or
`CLAUDE.md`, write `.github` Copilot files, install Aider configuration, start
MCP or A2A, contact external tools, execute workers, call providers/models or
network services, implement Host Contract, implement Dominium Bridge, implement
Workbench, apply PatchTransactions, create branches/worktrees, mutate GitHub,
publish releases, or mutate target repositories.

Recommended next task:

```text
AIDE-BUILD-MCP-SERVER-CONTRACT-01
```

## Work Item: AIDE-CHECK-INTEROP-EXPORTS-01

Completed for review as an independent check task.

Changed:

- `.aide/queue/AIDE-CHECK-INTEROP-EXPORTS-01/**`
- `.aide/reports/interop-exports-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check independently verifies the
static interop export build for complete source-chain evidence, preview artifact
presence, SHA-256 hash binding, JSON parseability, manifest/report consistency,
queue-authority wording, explicit non-capability boundaries, and build-artifact
immutability.

No material findings were identified. No static preview artifact, build report,
implementation file, schema, helper, test, accepted predecessor, generated OKF
page, runtime, provider, host, VCS, GitHub, release, or target-repository file
was modified.

Recommended next task:

```text
AIDE-ACCEPT-INTEROP-EXPORTS-01
```

## Work Item: AIDE-BUILD-INTEROP-EXPORTS-01

Completed for review as a static interop export build task.

Changed:

- `.aide/queue/AIDE-BUILD-INTEROP-EXPORTS-01/**`
- `.aide/interop/exports/**`
- `.aide/reports/interop-exports/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The task creates preview-only exports for
agent-facing guidance, Claude-facing guidance, Copilot-style instructions,
Aider-style config, an MCP manifest preview, and an A2A agent-card preview.
Artifact hashes are recorded in `.aide/interop/exports/manifest.json` and the
interop export reports.

No accepted interop capability, live MCP server, live A2A endpoint, Host
Contract, Dominium Bridge conformance, Workbench, Commander, Service, runtime,
worker execution, provider/model/network/Gateway/GitHub call, PatchTransaction
apply, branch/worktree automation, release, promotion, or target-repository
mutation was implemented.

Recommended next task:

```text
AIDE-CHECK-INTEROP-EXPORTS-01
```

## Work Item: AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01

Completed for review as a planning-only roadmap incorporation task.

Changed:

- `.aide/queue/AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01/**`
- `.aide/reports/intent-to-transaction-roadmap/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The task records the 2026-06-19 through
2026-06-20 architecture synthesis as an intent-to-transaction roadmap update:
AIDE coordinates and proves, domains own product semantics, capability
providers execute admitted deterministic operations, and hosts present shared
WorkUnit, transaction, evidence, and event state.

The update preserves `AIDE-BUILD-INTEROP-EXPORTS-01` as the live serialized
next AIDE task after ContextPack v2 acceptance. Future candidate lanes are
recorded for an AIDE/Dominium integration charter, CapabilityInvocation, Host
Contract v0, Dominium Bridge manifest and conformance, a validation slice,
DevelopmentTransaction, PreviewSession, and read-only Workbench.

No schema, helper, command, test, Host Contract, Host SDK, CapabilityInvocation,
DevelopmentTransaction, PreviewSession, ShadowWorkspace, Dominium Bridge
conformance, Workbench, Commander, Service, runtime, worker execution,
provider/model/network call, branch/worktree automation, PatchTransaction
apply, target mutation, release, or promotion was implemented.

Recommended next task:

```text
AIDE-BUILD-INTEROP-EXPORTS-01
```

## Work Item: AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01

Completed for review as a resume acceptance task.

Changed:

- `.aide/queue/AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01/**`
- `.aide/reports/context-pack-v2-resume-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The task accepts only
`context_pack_v2` as a deterministic projection capability for source/report
references by path and hash, structural validation subset, inspection, and
reporting.

The original blocked ContextPack build/check records remain historical evidence
and were not rewritten. The acceptance does not call models, providers, Gateway,
or network services; generate embeddings; execute agents, workers, or commands;
admit or trust adapters; apply patches; mutate target repositories; or implement
runtime behavior.

Recommended next task:

```text
AIDE-BUILD-INTEROP-EXPORTS-01
```

## Work Item: AIDE-RESUME-CHECK-CONTEXTPACK-V2-01

Completed for review as a resume check task.

Changed:

- `.aide/queue/AIDE-RESUME-CHECK-CONTEXTPACK-V2-01/**`
- `.aide/reports/context-pack-v2-resume-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check independently reviewed the
resume ContextPack v2 build for source-chain integrity, schema/helper alignment,
source hash binding, deterministic projection, source immutability, section and
reference shape, authority boundaries, CLI fail-closed behavior, report
consistency, and complete evidence.

No material findings were identified. The original blocked
`AIDE-CHECK-CONTEXTPACK-V2-01` record remains historical evidence and was not
rewritten. No ContextPack v2 implementation, schema, tests, build reports,
runtime, adapter, provider, host, VCS, branch/worktree, GitHub, release,
promotion, or target-repository file was intentionally changed.

Recommended next task:

```text
AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01
```

## Work Item: AIDE-RESUME-BUILD-CONTEXTPACK-V2-01

Completed for review as a resume build task.

Changed:

- `.aide/protocol/aide-context-pack-v2.schema.json`
- `core/protocol/context_pack_v2.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_context_pack_v2.py`
- `.aide/reports/context-pack-v2-resume/**`
- `.aide/queue/AIDE-RESUME-BUILD-CONTEXTPACK-V2-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The task builds the minimal
`context_pack_v2` slice as a deterministic evidence-bound projection record for
bounded queue, protocol, report, OKF, Reconciler, capability, conformance, and
explicit non-capability context.

The original blocked `AIDE-BUILD-CONTEXTPACK-V2-01` record remains historical
evidence and was not rewritten. The slice does not call models, providers,
Gateway, or network services; generate embeddings; execute agents, workers, or
commands; admit or trust adapters; apply patches; mutate target repositories;
or implement runtime behavior.

Recommended next task:

```text
AIDE-RESUME-CHECK-CONTEXTPACK-V2-01
```

## Work Item: AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01

Completed for review as a resume acceptance task.

Changed:

- `.aide/queue/AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest-resume-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The task accepts only
`minimal_adapter_manifest_schema` as a declaration-only capability for
representation, projection, structural validation, reference linkage,
declaration inspection, and reporting.

The original blocked `AIDE-ACCEPT-ADAPTER-MANIFEST-01` record remains
historical evidence and was not rewritten. The acceptance does not admit or
trust adapters, execute workers/tests, create sandboxes, resolve credentials,
call providers/models/network/Gateway/GitHub, create branches/worktrees, apply
patches, mutate target repositories, or implement runtime behavior.

Recommended next task:

```text
AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
```

## Work Item: AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01

Completed for review as a resume check task.

Changed:

- `.aide/queue/AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest-resume-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check independently reviewed the resume
AdapterManifest build for schema/helper alignment, ReferenceID forms,
declaration-only authority boundaries, deterministic projection, CLI behavior,
complete evidence, and report consistency.

No material findings were identified. The original blocked
`AIDE-CHECK-ADAPTER-MANIFEST-01` record remains historical evidence and was not
rewritten.

No AdapterManifest implementation, schema, focused test, build report, runtime,
adapter execution, provider, host, VCS, OKF, branch/worktree, GitHub, release,
promotion, or target-repository file was intentionally changed. No admission,
trust, approval, apply, rollback, policy, credential, network, or execution
behavior was added.

Recommended next task:

```text
AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01
```

## Work Item: AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01

Completed for review as a resume build task.

Changed:

- `.aide/protocol/aide-adapter-manifest.schema.json`
- `core/protocol/adapter_manifest.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_adapter_manifest.py`
- `.aide/reports/adapter-manifest-resume/**`
- `.aide/queue/AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The task builds the minimal
`minimal_adapter_manifest_schema` slice as a declaration-only protocol record
for adapter integration shape, prerequisites, reference linkage, projection,
inspection, validation, and reporting.

The original blocked `AIDE-BUILD-ADAPTER-MANIFEST-01` record remains historical
evidence and was not rewritten. The slice does not admit, trust, execute,
launch, sandbox, resolve credentials, call providers, call network services,
mutate GitHub, create branches/worktrees, apply patches, mutate target
repositories, or implement runtime behavior.

Focused AdapterManifest tests and CLI validation pass with warnings. The
warnings are deliberate: AdapterManifest remains unaccepted, admission/trust and
execution are absent, and JSON Schema validation remains a bounded local subset
plus semantic checks.

Recommended next task:

```text
AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01
```

## Work Item: AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01

Completed for review as a resume acceptance task.

Changed:

- `.aide/queue/AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01/**`
- `.aide/reports/patch-transaction-resume-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `ACCEPTED_WITH_WARNINGS`. The task accepts only the repaired
`minimal_patch_transaction_schema` capability as a no-apply protocol slice for
representation, projection, structural validation, scope validation, reference
linkage, inspection, and reporting.

The original blocked `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` record remains
historical evidence and was not rewritten. The build/check/repair/repair-check
chain remains preserved.

No PatchTransaction implementation, schema, focused test, original blocked
acceptance record, failed-check report, repair report, CapabilityManifest record,
runtime, adapter, provider, host, VCS, OKF, branch/worktree, GitHub, release,
promotion, or target-repository file was intentionally changed. No approval,
apply, rollback, policy, admission, or trust behavior was added.

Recommended next task:

```text
AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01
```

## Work Item: AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Completed for review as an independent repair check.

Changed:

- `.aide/queue/AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01/**`
- `.aide/reports/patch-transaction-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The check independently confirms the
PatchTransaction repair closes both material path-scope defects:

- drive-prefixed relative paths now fail closed;
- duplicate-normalized entries now fail closed in `allowed_paths`,
  `forbidden_paths`, and `declared_changed_paths`.

Diagnostics preserve both original conflicting values and the shared canonical
path. Existing scope protections remain intact, unsupported execution-like CLI
operations fail closed, repeated projection is deterministic, and source inputs
remain unchanged. The original failed check and the already-blocked downstream
tasks remain historical records.

No PatchTransaction implementation, schema, focused test, failed-check report,
repair report, blocked downstream task, runtime, adapter, provider, host, VCS,
OKF, branch/worktree, GitHub, release, promotion, or target-repository file was
intentionally changed. No approval, apply, rollback, policy, admission, or trust
behavior was added.

Recommended next task:

```text
AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01
```

## Work Item: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Completed for review as a bounded PatchTransaction path-scope repair.

Changed:

- `core/protocol/patch_transaction.py`
- `.aide/scripts/tests/test_aide_patch_transaction.py`
- `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01/**`
- `.aide/reports/patch-transaction-repair/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The repair addresses the two material
findings from `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`:

- drive-prefixed relative paths such as `C:repo/file.txt` now fail validation;
- duplicate-normalized declarations such as `src//file.py` and `src/file.py`
  now fail validation.

The repair adds focused regression tests and preserves PatchTransaction as a
schema/projection/validation-only no-apply record. No PatchTransaction schema,
CLI dispatch, build/check evidence, accepted predecessor, runtime, adapter,
provider, host, VCS, OKF, branch/worktree, GitHub, release, promotion, or
target-repository file was intentionally changed. No approval, apply, rollback,
policy, admission, or trust behavior was added.

A follow-up prompt alignment pass expanded duplicate diagnostics to include both
original inputs and the shared canonical path, added explicit drive-prefix and
duplicate-normalization regression coverage, and completed the stricter repair
report set.

Recommended next task:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-CHECK-CONTEXTPACK-V2-01

Completed for review as a blocked ContextPack v2 independent-check gate.

Changed:

- `.aide/queue/AIDE-CHECK-CONTEXTPACK-V2-01/**`
- `.aide/reports/context-pack-v2-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. The prompt required the ContextPack v2 build result to
be `PASS` or `PASS_WITH_WARNINGS`, but live queue truth shows
`AIDE-BUILD-CONTEXTPACK-V2-01` is `BLOCKED` and recommends
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

The check did not execute ContextPack v2 schema/helper/projection/CLI/test,
digest, budget, path-scope, rendering, or v0 compatibility review because no
passed ContextPack v2 build exists. No ContextPack implementation, repair,
schema, helper, CLI dispatch, focused tests, projection, generated pack, accepted
record, OKF page, model call, embedding generation, adapter/provider selection,
agent/worker execution, PatchTransaction apply, target-repository mutation,
release, or promotion was intentionally changed or performed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-BUILD-CONTEXTPACK-V2-01

Completed for review as a blocked ContextPack v2 build gate.

Changed:

- `.aide/queue/AIDE-BUILD-CONTEXTPACK-V2-01/**`
- `.aide/reports/context-pack-v2/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. The prompt required AdapterManifest acceptance to be
`ACCEPTED` or `ACCEPTED_WITH_WARNINGS` and PatchTransaction acceptance to remain
accepted, but live queue truth shows `AIDE-ACCEPT-ADAPTER-MANIFEST-01` and
`AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` are both `BLOCKED`.

ContextPack v2 implementation was not started. No ContextPack schema, helper,
CLI dispatch, focused tests, deterministic pack projection, context-pack
output, model call, embedding generation, adapter/provider selection, agent or
worker execution, command execution beyond validation, PatchTransaction apply,
credential resolution, branch/worktree automation, target-repository mutation,
release, or promotion was intentionally changed or performed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-ACCEPT-ADAPTER-MANIFEST-01

Completed for review as a blocked AdapterManifest acceptance gate.

Changed:

- `.aide/queue/AIDE-ACCEPT-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. The prompt required AdapterManifest build/check to be
`PASS` or `PASS_WITH_WARNINGS` and PatchTransaction acceptance to remain
accepted, but live queue truth shows both AdapterManifest source tasks are
`BLOCKED` and `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` is also `BLOCKED`.

AdapterManifest is not accepted by this task. No AdapterManifest schema,
helper, CLI dispatch, focused tests, projection, manifest records, adapter
admission, adapter trust, worker/test execution, provider/model/network call,
branch/worktree automation, PatchTransaction apply, target-repository mutation,
release, or promotion was intentionally changed or performed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-CHECK-ADAPTER-MANIFEST-01

Completed for review as a blocked AdapterManifest independent-check gate.

Changed:

- `.aide/queue/AIDE-CHECK-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. The prompt required the AdapterManifest build result to
be `PASS` or `PASS_WITH_WARNINGS`, but live queue truth shows
`AIDE-BUILD-ADAPTER-MANIFEST-01` is `BLOCKED` and recommends
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

The check did not execute AdapterManifest schema/helper/projection/CLI/test
review because no passed AdapterManifest build exists. No AdapterManifest
implementation, repair, schema, helper, CLI dispatch, focused tests, projection,
adapter execution, endpoint contact, credential resolution, admission, trust,
provider/model/network call, branch/worktree automation, PatchTransaction apply,
target-repository mutation, release, or promotion was intentionally changed or
performed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-BUILD-ADAPTER-MANIFEST-01

Completed for review as a blocked AdapterManifest build gate.

Changed:

- `.aide/queue/AIDE-BUILD-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. The prompt required PatchTransaction acceptance to be
`ACCEPTED` or `ACCEPTED_WITH_WARNINGS`, but live queue truth shows
`AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` is `BLOCKED` after the independent
check reported `FAILED_VALIDATION`.

AdapterManifest implementation was not started. No AdapterManifest schema,
helper, CLI dispatch, focused tests, projection, manifest records, adapter
admission, adapter trust, worker/test execution, provider/model/network call,
branch/worktree automation, PatchTransaction apply, target-repository mutation,
release, or promotion was intentionally changed or performed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01

Completed for review as a blocked PatchTransaction acceptance gate.

Changed:

- `.aide/queue/AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01/**`
- `.aide/reports/patch-transaction-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `BLOCKED`. Live queue evidence shows the build task is complete
with `missing_evidence: 0`, but the independent check result is
`FAILED_VALIDATION` and recommends
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

PatchTransaction is not accepted by this task. The failed check is preserved,
including the two material path-scope findings:

- `path_scope_drive_prefixed_relative_accepted`;
- `path_scope_duplicate_normalization_accepted`.

No implementation, schema, helper, test, build/check report, accepted
predecessor, runtime, adapter, provider, host, VCS, OKF, branch/worktree,
GitHub, release, promotion, or target-repository file was intentionally changed.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01

Completed for review as an independent check-only PatchTransaction review.

Changed:

- `.aide/queue/AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01/**`
- `.aide/reports/patch-transaction-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `FAILED_VALIDATION`. The check verified the build source chain,
complete build evidence, sample patch artifact digest binding, report
consistency, lifecycle/no-apply invariants, authority boundaries, unsupported
execution-command closure, canonical repeated projection, and source
immutability.

The check found two material path-scope fail-closed defects:

- drive-prefixed relative paths such as `C:repo/file.txt` are accepted as valid
  repository-relative scope;
- duplicate-normalized declared paths such as `src//file.py` and `src/file.py`
  are accepted without an ambiguity error.

No implementation, schema, helper, test, build report, accepted predecessor,
runtime, adapter, provider, host, VCS, OKF, branch/worktree, GitHub, release,
promotion, or target-repository file was intentionally changed. Acceptance is
blocked until a bounded repair is built and independently rechecked.

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Work Item: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01

Completed for review as a minimal schema-only PatchTransaction protocol slice.

Changed:

- `.aide/protocol/aide-patch-transaction.schema.json`
- `core/protocol/patch_transaction.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_patch_transaction.py`
- `.aide/reports/patch-transaction/**`
- `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The slice defines a deterministic
PatchTransaction record for a proposed bounded mutation, validates ReferenceID
syntax, digest shape and binding, fail-closed scope rules, lifecycle/no-apply
consistency, required capability and ConformanceResult refs, explicit
non-capabilities, deterministic projection, and source immutability.

The generated example is synthetic and writes only reports under
`.aide/reports/patch-transaction/`, including a sample `unified_diff` artifact.
It does not apply a patch, mutate a target repository, grant approval, evaluate
policy, roll back, admit or trust a subject, activate profiles, run workers,
implement AdapterManifest or ContextPack v2, call providers/models/network/
Gateway/GitHub, create branches/worktrees, publish releases, or promote
anything.

Validation covered Python compile checks, 22 focused tests, `patch-transaction`
status/project/validate, predecessor validators, task inspect/evidence, broad
AIDE validation, JSON parsing, deterministic projection comparison, source
immutability, secret-like scan, Git diff checks, and commit policy checks.

Recommended next task:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
```

## Work Item: AIDE-OPERATIONAL-HEALTH-PAUSE-01

Completed for review as a report-only operational-health pause before
PatchTransaction.

Changed:

- `.aide/queue/AIDE-OPERATIONAL-HEALTH-PAUSE-01/**`
- `.aide/reports/operational-health-pause/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The result is `PASS_WITH_WARNINGS`. The pause confirms that live queue truth is
unambiguous after `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`, the accepted
ConformanceResult digest chain remains intact, the historical failed digest
check remains preserved, and the accepted result still binds to the pristine
accepted ConformanceProfile payload using `sha256-canonical-json-v1`.

Operational warning debt remains: many historical queue entries still show
`needs_review`, generated status/task packet surfaces can be stale, ReportIndex
tracks 479 reports with 70 ambiguity records, GeneratedOutputLedger tracks 1381
classified candidates with 67 unknown-generator records, OKF lint reports one
stale-context finding, and Reconciler remains report-only with four
warning-class findings.

No blocker was found for beginning `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` as
a schema-only, no-apply, inspectable mutation-record task. This work does not
implement PatchTransaction, repair protocols, activate profiles, execute
conformance cases, admit or trust subjects, create AdapterManifest or
ContextPack v2, run workers, implement runtime/Test Broker/Service/Commander/
Workbench, call providers/models/network/Gateway/GitHub, mutate branches or
target repositories, publish releases, or promote anything.

Validation covered git state and diff checks, predecessor validators,
OKF/Reconciler checks, ReportIndex/GeneratedOutputLedger/Track B JSON parse
checks, task inspect/evidence, broad AIDE validation, health-report JSON
parsing, secret-like scan, generated churn cleanup, and commit policy checks.

Recommended next gated task:
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`.

## Work Item: AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01

Completed for review as the acceptance/consolidation gate for the minimal
ConformanceResult schema capability.

Changed:

- `.aide/queue/AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01/**`
- `.aide/reports/conformance-result-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The acceptance result is `ACCEPTED_WITH_WARNINGS`. It accepts only the
evidence-projected, runnerless ConformanceResult record
`aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01`
for profile `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.

The historical failed digest check remains preserved as
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01` with result `FAILED_VALIDATION`. The
accepted digest after repair is
`sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`,
using `sha256-canonical-json-v1` over the pristine accepted ConformanceProfile
payload.

The accepted record remains bounded: case results count 10, required cases
count 8, aggregate outcome `PASS_WITH_WARNINGS`, record valid true, record
complete true, and profile requirements satisfied true. These facts do not
activate the profile, admit the subject, or grant trust.

The acceptance deliberately avoids implementation repair, schema/helper/test
changes, conformance runner, case execution, automatic observation collection,
profile activation, admission, subject trust, adapter admission/execution,
PatchTransaction, AdapterManifest, ContextPack v2, runtime, Service, Commander,
provider/model/Gateway/network/GitHub calls, branch/worktree automation, target
apply, release, promotion, production readiness, and broad autonomous runtime
behavior.

Validation covered JSON parsing for acceptance and predecessor reports, Python
compile checks, focused ConformanceResult tests, ConformanceResult/Profile/
CapabilityManifest validators, task inspect/evidence checks, broad AIDE
validation, diff checks, secret-like scan, generated churn cleanup, and commit
policy validation.

Recommended next gated task:
`AIDE-OPERATIONAL-HEALTH-PAUSE-01`.

## Work Item: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Checked for review as the independent gate after
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

Changed:

- `.aide/queue/AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01/**`
- `.aide/reports/conformance-result-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check result is `PASS_WITH_WARNINGS`. The historical failed check remains
preserved with recorded digest
`sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`
and raw-profile digest
`sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`.

The repaired ConformanceResult now records profile digest
`sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`.
Independent recomputation with `hashlib.sha256` over the pristine accepted
profile payload using `sha256-canonical-json-v1` produced the same digest.

Negative checks confirm that an incorrect digest fails validation, a changed
profile payload changes the digest, and lifecycle-warning mutation on a profile
copy does not become authoritative digest source. Projection remains
deterministic and does not mutate the accepted profile source.

Semantic impact remains bounded. Case results, aggregate outcome, record
completeness, profile satisfaction, execution state, admission state, subject
admission, and trust remain unchanged. The result remains evidence-projected,
runnerless, inactive, not admitted, and not trusted.

Validation covered Python compile checks, focused ConformanceResult tests,
`conformance-result status/project/validate`, independent digest recomputation,
bad-digest validation, copy-mutation checks, repeated projection determinism,
generated report parsing, task inspect/evidence, predecessor validators, broad
AIDE validation, diff checks, secret-like scan, and generated churn cleanup.

Recommended next gated task:
`AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`.

## Work Item: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Completed for review as a bounded repair to the ConformanceResult profile digest
binding defect found by `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.

Changed:

- `core/protocol/conformance_result.py`
- `.aide/scripts/tests/test_aide_conformance_result.py`
- `.aide/reports/conformance-result/**`
- `.aide/queue/AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01/**`
- `.aide/reports/conformance-result-repair/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The root cause was that `load_accepted_conformance_profile()` appended a
candidate-lifecycle warning into the loaded profile object before
`profile_digest()` was computed. Projection and validation then both used the
same warning-mutated in-memory profile representation, allowing a false-positive
digest match.

The repair adds a pristine profile loader, defines `sha256-canonical-json-v1`
using sorted compact UTF-8 JSON, computes the result digest from the pristine
accepted profile payload, and validates against a freshly loaded pristine
profile source. The corrected digest is
`sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`.

Regression tests now independently compute the expected digest with
`hashlib.sha256` and canonical `json.dumps`, verify lifecycle-warning mutation
on a copy cannot validate the pristine-bound result, prove digest changes when
the pristine payload changes, and confirm projection/validation do not mutate
the profile source.

Semantic impact was intentionally limited. Case results, aggregate outcome,
record completeness, profile satisfaction, admission state, and trust state
remain unchanged. The result remains evidence-projected, runnerless, not
activated, not admitted, and not trusted.

Validation covered Python compile checks, focused ConformanceResult tests,
`conformance-result project/validate`, independent digest recomputation,
repeated projection determinism, generated report parsing, task
inspect/evidence, predecessor validators, broad AIDE validation, source
mutation review, diff checks, secret-like scan, and commit policy validation.

Remaining required work is an independent recheck:
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

## Work Item: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01

Checked for review as the independent gate after
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.

Changed:

- `.aide/queue/AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01/**`
- `.aide/reports/conformance-result-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check result is `FAILED_VALIDATION`. The source ConformanceResult records
profile digest
`sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`,
but independent recomputation against the raw accepted ConformanceProfile
report payload produced
`sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`.

The material finding is `profile_digest_mismatch`. The helper loads the
accepted profile, appends a lifecycle warning to the in-memory profile, and then
computes and validates the digest against that mutated view. That makes the
current validator report a false-positive digest match for the built result.

The check did not repair the implementation. Schema shape, result inventory,
case-result binding, required-case aggregation, evidence projection, evidence
links, admission/trust separation, CLI surface, generated reports, and
forbidden-operation boundaries were reviewed and recorded as evidence.

Validation covered preflight predecessor validators, check-report JSON parsing,
task inspect/evidence checks, `conformance-result status/validate`, broad AIDE
validation, independent digest recomputation, generated-report churn
containment, secret-like scan, diff whitespace checks, and commit policy
validation.

Remaining required work is a bounded repair task:
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`. The repair must make the
profile digest bind to the raw accepted profile payload, add regression coverage
for raw-profile digest recomputation, regenerate the result/reports, and then
rerun this check chain. ConformanceResult acceptance, PatchTransaction, adapter
work, runtime, provider/model/network/Gateway calls, target apply,
branch/worktree automation, release, and promotion remain deferred.

## Work Item: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01

Completed for review as the first minimal evidence-projected
`ConformanceResult` slice for the accepted `minimal_capability_manifest`
ConformanceProfile candidate.

Changed:

- `.aide/protocol/aide-conformance-result.schema.json`
- `core/protocol/conformance_result.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_conformance_result.py`
- `.aide/reports/conformance-result/**`
- `.aide/queue/AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The implemented result ref is
`aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01`.
It binds to profile
`aide://conformance-profile/minimal_capability_manifest-v1.0.0`, records a
stable profile digest, projects one case result per accepted profile case, and
aggregates the current evidence state as `PASS_WITH_WARNINGS`.

The model keeps `record_valid`, `profile_requirements_satisfied`, and
admission/trust state independent. The first projection records
`record_valid: true`, `record_complete: true`, and
`profile_requirements_satisfied: true`, while preserving
`execution_performed: false`, `runner_ref: null`, `admission_performed: false`,
`subject_admitted: false`, and `trusted: false`.

Validation covered Python compile, focused ConformanceResult tests,
`conformance-result status/project/validate`, generated report JSON parsing,
task inspect/evidence checks, predecessor validators, broad repository
validation, generated-report churn containment, secret-like scan, diff
whitespace checks, and commit policy validation.

Remaining deliberate deferrals: conformance runner, case execution, command
execution, automatic result collection, profile activation, conformance
admission, subject admission, trust grants, adapter admission/execution,
PatchTransaction, AdapterManifest, ContextPack v2, runtime, worker execution,
provider/model/network/Gateway calls, target apply, branch/worktree automation,
release, promotion, production readiness, and broad autonomous runtime behavior.

## Work Item: AIDE-ACCEPT-CONFORMANCE-PROFILE-01

Accepted for review as the consolidation gate over
`AIDE-BUILD-CONFORMANCE-PROFILE-01` and
`AIDE-CHECK-CONFORMANCE-PROFILE-01`.

Changed:

- `.aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/**`
- `.aide/reports/conformance-profile-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The accepted capability is `minimal_conformance_profile`: versioned
ConformanceProfile schema, profile-scoped ConformanceCase model, deterministic
candidate profile projection, profile and case indexes, required/optional/
advisory requirement semantics, fail-closed required-case aggregation policy,
evidence requirement declarations, versioning and compatibility policy,
CapabilityManifest subject integration, Track B governance evidence integration,
and `conformance-profile status/project/validate` CLI.

The result is `ACCEPTED_WITH_WARNINGS`. The profile
`aide://conformance-profile/minimal_capability_manifest-v1.0.0` remains
`candidate` and inactive. No ConformanceResult was generated, no cases were
executed, no conformance runner was added, no admission was performed,
`minimal_capability_manifest` was not admitted by conformance, and no trust was
granted.

Warnings remain non-blocking for the profile-only boundary, deferred
ConformanceResult, deferred runner/execution/admission, inline case modeling
rather than a separate `$defs` block, stale generated latest-task-packet drift,
and later PatchTransaction, AdapterManifest, ContextPack v2, adapter, runtime,
provider, target apply, branch/worktree, release, and promotion layers.

Validation covered Python compile, focused ConformanceProfile tests,
`conformance-profile status/validate`, profile/check/acceptance report JSON
parsing, task inspect/evidence checks, predecessor validators, broad repository
validation, generated-report churn containment, secret-like scan, diff
whitespace checks, and commit policy validation.

The next recommended queue task is exactly
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.

## Work Item: AIDE-CHECK-CONFORMANCE-PROFILE-01

Checked for review as the independent gate after
`AIDE-BUILD-CONFORMANCE-PROFILE-01`.

Changed:

- `.aide/queue/AIDE-CHECK-CONFORMANCE-PROFILE-01/**`
- `.aide/reports/conformance-profile-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check reviewed the candidate profile
`aide://conformance-profile/minimal_capability_manifest-v1.0.0` for subject
`aide://capability/minimal_capability_manifest`. It confirmed 10 profile-scoped
cases: 8 required, 1 optional, and 1 advisory.

The result is `PASS_WITH_WARNINGS`. No blockers were found. Non-blocking
warnings remain for deferred ConformanceResult, conformance runner/execution,
admission/trust promotion, adapter admission/execution, PatchTransaction,
AdapterManifest, ContextPack v2, runtime surfaces, target apply,
branch/worktree automation, release/promotion, production readiness, stale
`.aide/context/latest-task-packet.md`, and inline schema case modeling rather
than a separate `$defs` block.

The work deliberately avoids implementation repair, ConformanceResult,
conformance execution, conformance admission, automatic admission, policy
decision, adapter admission, adapter execution, capability execution, runtime
capability registry, scheduler, leases, supervisor, runtime, Service,
Commander, PatchTransaction, AdapterManifest, ContextPack v2, Test Broker
runtime, async execution, worker execution, provider adapters, branch/worktree
automation, target apply, active apply, rollback execution, uninstall execution,
release, promotion, GitHub mutation, Gateway calls, network calls,
model/provider calls, target repo mutation, production readiness, release
readiness, and broad autonomous runtime behavior.

Validation covered Python compile, focused ConformanceProfile tests,
`conformance-profile status/project/validate`, predecessor protocol validators,
report JSON parsing, task inspect/evidence checks, determinism/source-mutation
sentinel, broad repository validation, diff whitespace checks, generated-report
churn containment, secret-like scan, and commit policy validation.

The next recommended queue task is exactly
`AIDE-ACCEPT-CONFORMANCE-PROFILE-01`; if accepted, proceed to
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.

## Work Item: AIDE-BUILD-CONFORMANCE-PROFILE-01

Implemented for review as the first minimal ConformanceProfile protocol slice.

Changed:

- `.aide/protocol/aide-conformance-profile.schema.json`
- `core/protocol/conformance_profile.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_conformance_profile.py`
- `.aide/reports/conformance-profile/**`
- `.aide/queue/AIDE-BUILD-CONFORMANCE-PROFILE-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The new profile targets the accepted `minimal_capability_manifest` capability:

- `profile_ref`: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- `profile_id`: `minimal_capability_manifest`
- `profile_version`: `1.0.0`
- `lifecycle`: `candidate`
- `subject.ref`: `aide://capability/minimal_capability_manifest`

The helper builds one deterministic candidate profile with profile-scoped
ConformanceCase records, fail-closed aggregation policy for required cases,
warning-only handling for unknown optional/advisory evaluators, evidence
requirements, profile/case indexes, projection reports, validation reports, and
explicit non-capabilities.

The CLI now exposes:

- `conformance-profile status`
- `conformance-profile project`
- `conformance-profile validate`

The work deliberately avoids ConformanceResult, conformance runner/execution,
admission policy, automatic admission, adapter admission/execution, capability
execution, runtime capability registry, PatchTransaction, AdapterManifest,
ContextPack v2, scheduler, leases, supervisor, Test Broker runtime, worker
execution, provider/model/Gateway/network calls, branch/worktree automation,
target apply, active apply, release, promotion, target repo mutation, production
readiness, release readiness, and broad autonomous runtime behavior.

Validation covered Python compile checks, focused ConformanceProfile unit tests,
`conformance-profile status/project/validate`, JSON parsing for generated
reports, predecessor validators, task inspect/evidence checks, broad AIDE
validation, diff whitespace checks, generated churn containment, and commit
policy validation.

The result is `PASS_WITH_WARNINGS` because the profile defines requirements but
does not execute them. The next recommended queue task is exactly
`AIDE-CHECK-CONFORMANCE-PROFILE-01`.

## Work Item: AIDE-ADOPT-APACHE-2-LICENSE-01

Completed for review as a policy/docs-only legal posture update.

Changed:

- `LICENSE.md`
- `NOTICE.md`
- `LICENSING.md`
- `GENERATED_OUTPUTS.md`
- `TRADEMARKS.md`
- `LICENSE_SUMMARY.md`
- `README.md`
- `CONTRIBUTING.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/AIDE-ADOPT-APACHE-2-LICENSE-01/**`
- `.aide/queue/index.yaml`

The repository now has a standard Apache License, Version 2.0 (`Apache-2.0`)
packet rather than the previous no-public-license README warning.

The new legal docs preserve a permissive open-source posture for use,
redistribution, modification, forks, packaging, hosted use, commercial use,
adapters, integrations, protocols, schemas, templates, and docs. They keep
remaining boundaries in notices, Apache-2.0 patent and warranty terms,
trademark/project identity policy, generated-output policy, contribution policy,
and governance.

Generated outputs are explicitly bounded: AIDE does not claim ownership of a
target repository or repo-local facts, metadata, analysis, docs, patches, OKF
pages, WorkUnits, WorkerRuns, TestJobs, EvidencePackets, EventRecords,
ContextPacks, or reports produced from that repository, except that copied AIDE
material remains Apache-2.0 and third-party material keeps its own terms.

Contribution guidance now records inbound=outbound under Apache-2.0, optional
DCO sign-off, no default CLA requirement, and provenance expectations for
AI-assisted contributions.

The work deliberately avoids runtime behavior changes, protocol schema changes,
support-tier or capability-level changes, generated-output source-truth
promotion, release publication, tags, GitHub mutation, branch creation or
promotion, provider/model/network calls, target-repository mutation, trademark
registration, CLA adoption, and legal-advice claims.

Validation covered AIDE doctor, AIDE validation, intent validation, task
inspect/evidence checks, diff whitespace checks, changed-file review, generated
helper drift containment, and post-commit commit-policy validation. Counsel
review remains recommended before public release or commercial/legal
publication decisions.

## Work Item: AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01

Completed for review as a check-only acceptance gate for the deterministic OKF-compatible AIDE knowledge bundle.

Changed:

- `.aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/**`
- `.aide/reports/okf-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The acceptance reviewed `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`, `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`, `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`, the generated OKF bundle, OKF validation and lint reports, okf-check reports, concept and link indexes, ReferenceID integration, EventRecord integration, warnings, and explicit non-capabilities.

The result is `ACCEPTED_WITH_WARNINGS`. The accepted capability is limited to `minimal_okf_knowledge_bundle`: deterministic OKF-compatible markdown projection, reserved `index.md` and `log.md`, required concept pages, deterministic frontmatter and non-empty type, concept index, link index, `okf status/project/validate/lint`, ReferenceID integration, EventRecord integration, stale latest-task-packet surfacing, and preserved protocol/evidence/reference/event authority.

Warnings are non-blocking: full YAML parser integration remains deferred, stdlib structural frontmatter validation is used, `.aide/context/latest-task-packet.md` remains stale, Reconciler is not implemented, and later CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 work remains deferred.

The work deliberately avoids implementation repair, OKF execution authority, protocol/evidence authority from markdown, runtime knowledge service, LLM-authored wiki behavior, network enrichment, web crawling, provider/model calls, search/vector indexes, OKF visualizer, Reconciler implementation, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, event sourcing runtime, append-only event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

Validation covered acceptance report JSON parsing, task inspect/evidence checks, OKF status/validate/lint, predecessor protocol validators, broad repository validation, generated-report churn containment, diff whitespace checks, and commit policy validation.

The next recommended queue task is exactly `AIDE-BUILD-RECONCILER-REPORTS-01`.

## Work Item: AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01

Completed for review as a check-only independent review of the deterministic OKF-compatible AIDE knowledge bundle.

Changed:

- `.aide/queue/AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01/**`
- `.aide/reports/okf-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check reviewed `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`, the reported build commit `c51859006e8cf4ac429bbaf9663917d0fdbe904b`, the live HEAD `744503c56d37c132410485aacee3c26347cd96c4`, OKF generated bundle structure, frontmatter, projection reports, concept and link indexes, CLI dispatch, ReferenceID integration, EventRecord integration, predecessor compatibility, tests, and validation outputs.

The result is `PASS_WITH_WARNINGS`. No blocking defects were found. Warnings remain for the deterministic stdlib structural frontmatter subset, stale `.aide/context/latest-task-packet.md`, stale prompt-reported dirty intake state, and deferred later OKF-adjacent capabilities.

The check deliberately avoids implementation repair, OKF execution authority, protocol/evidence authority from markdown, runtime knowledge service, LLM-authored broad wiki, network enrichment, web crawling, provider/model calls, search/vector indexes, OKF visualizer, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, event sourcing runtime, append-only event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

Validation covered diff whitespace checks, Python compile checks, focused OKF tests, `okf status/project/validate/lint`, OKF and okf-check JSON parsing, EventRecord and ReferenceID validators, task inspect/evidence checks for the build and check tasks, broad repository validation, generated-report churn containment, and commit policy validation.

The next recommended queue task is exactly `AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01`. Reconciler is not recommended directly from this check.

## Work Item: DOCS-PUBLIC-README-POSITIONING-01

Completed as a docs-only public positioning refresh under explicit user authorization after the initial intake preflight blocked the broad README/public-doc prompt.

Changed:

- `README.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/intake/preflight-or-blocker-report.md`

The README now presents AIDE as a portable agentic development control plane for real repositories. It adds a top architecture diagram, public maturity warning, differentiation table, quick example, OKF knowledge-plane explanation, agentic workflow, multi-IDE and legacy support vision, Workshop/Workbench vision, safety/truth model, near-term roadmap, implementation-status table, getting-started commands, repo layout, design principles, external references, contributor expectations, and license boundary.

The supporting docs add public-claim discipline, roadmap alignment for the current protocol and OKF sequence, documentation-index updates for README and OKF projection authority, and this plan/execution record.

Notable boundary choices:

- AIDE is described as infrastructure around agents, not an AI editor, VS Code competitor, Codex wrapper, prompt pack, RAG system, or project-management tool.
- WorkerRun and TestJob remain metadata-only.
- EventRecord remains projection-only.
- OKF remains an explanatory markdown projection, not execution authority or protocol/evidence truth.
- Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, Runtime, Test Broker, Workshop/Workbench, live provider adapters, legacy IDE bridges, release publication, and promotion remain planned or not started unless current queue evidence says otherwise.

Verification covered live task status, broad AIDE validation, OKF status, OKF validation, intent validation, external reference checks for OKF, LLM Wiki, and Codex `AGENTS.md` context, and diff whitespace checks. Generated latest-intake and task-status report churn from preflight commands was contained after validation.

Remaining issues are documentation-level only: the README is now public-facing, but the project still has no public license file and remains pre-product/pre-runtime.

## Work Item: AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01

Implemented for review as the first deterministic OKF-compatible AIDE knowledge bundle projection.

Changed:

- `core/knowledge/__init__.py`
- `core/knowledge/okf_bundle.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_okf_knowledge_bundle.py`
- `.aide/knowledge/okf/**`
- `.aide/reports/okf/**`
- `.aide/queue/AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The slice adds deterministic markdown/frontmatter projection, a stdlib structural frontmatter writer/parser/validator, OKF structural validation, OKF lint, concept and link indexes, generated current-state/protocol/capability/decision/risk pages, and thin AIDE Lite `okf status/project/validate/lint` dispatch. The generated bundle has 24 concept pages plus reserved `index.md` and `log.md`.

The work deliberately preserves the authority boundary: protocol executes, evidence proves, references identify, events remember, and OKF knowledge explains. OKF pages do not become queue truth, protocol schema truth, evidence truth, execution authority, or future-work authority.

Validation is recorded in `.aide/queue/AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01/evidence/validation.md`. Focused tests cover frontmatter round trips, temp-root projection, source artifact immutability, required pages, reserved files, validation/lint behavior, EventRecord projection-only classification, CLI dispatch, rejected runtime/network subcommands, and JSON report parsing.

Remaining warnings are non-blocking: full YAML parser integration is deferred in favor of deterministic stdlib structural validation, and `.aide/context/latest-task-packet.md` remains stale relative to queue truth.

The work deliberately avoids OKF execution authority, protocol/evidence authority from markdown, runtime knowledge service, LLM-authored broad wiki, network enrichment, web crawling, provider/model calls, search/vector indexes, OKF visualizer, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, event sourcing runtime, append-only event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

The next recommended queue task is exactly `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.

## Work Item: AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01

Completed for review as a check-only acceptance gate for the projection-only EventRecord schema slice.

Changed:

- `.aide/queue/AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01/**`
- `.aide/reports/event-record-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The acceptance reviewed `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`, `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`, and the accepted ReferenceID predecessor. The result is `ACCEPTED_WITH_WARNINGS`: accepted capability is limited to `minimal_event_record_schema`, including EventRecord schema, helper/projection/validation, `event-record status/project/validate`, deterministic event-family index, deterministic projection-only example events, ReferenceID integration, reserved event-family vocabulary, projection-only status, and `recorded: false` examples.

Warnings are non-blocking: EventRecord remains projection-only, full Draft 2020-12 JSON Schema validation remains deferred, event family names are reserved vocabulary only, runtime event store/log/replay/state reconstruction are not implemented, latest-task-packet state remains stale, and OKF/Reconciler/CapabilityManifest/ConformanceProfile/PatchTransaction/AdapterManifest/ContextPack v2 remain future work.

Validation covered task inspect/evidence checks for build and check, EventRecord status/project/validate, EventRecord report JSON parsing, predecessor protocol validators, broad repository validation, generated-report churn containment, and diff whitespace checks.

The work deliberately avoids implementation repairs, event sourcing runtime, append-only runtime event store, runtime event log, replay, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF implementation, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

The next recommended queue task is exactly `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`.

## Work Item: AIDE-CHECK-EVENT-RECORD-SCHEMA-01

Completed for review as an independent check of the projection-only EventRecord schema slice.

Changed:

- `.aide/queue/AIDE-CHECK-EVENT-RECORD-SCHEMA-01/**`
- `.aide/reports/event-record-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check reviewed `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`, commit `0e686040b18dff32672bc421bbdd95882f9822f0`, the EventRecord schema/helper, thin CLI dispatch, event family index, projection-only examples, generated reports, focused tests, predecessor compatibility, source artifact traceability, and no-overclaiming boundaries. The result is `PASS_WITH_WARNINGS`: no blocking defects were found, while full JSON Schema Draft 2020-12 validation, runtime event sourcing/store/replay behavior, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and broader runtime remain intentionally deferred.

Validation covered Python compile, focused EventRecord tests, EventRecord status/project/validate, predecessor protocol validators, schema/report JSON parsing, task inspect/evidence checks, broad repository validation, and diff whitespace checks. Preflight generated report churn outside the check scope was restored before writing check artifacts.

The work deliberately avoids implementation repairs, event sourcing runtime, append-only runtime event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

The next recommended queue task is exactly `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`; OKF remains gated behind EventRecord acceptance.

## Work Item: AIDE-BUILD-EVENT-RECORD-SCHEMA-01

Implemented for review as the minimal projection-only EventRecord schema slice.

Changed:

- `core/protocol/event_record.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-event-record.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_event_record_schema.py`
- `.aide/reports/event-record/**`
- `.aide/queue/AIDE-BUILD-EVENT-RECORD-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The slice adds EventRecord record construction and validation, EventRecord schema alignment checks, fail-closed required event type handling, optional future event type warnings, ReferenceID-backed event/subject/causation/correlation/evidence/report refs, deterministic event family index projection, projection-only example events, and local status/projection/validation reports.

The AIDE Lite changes are thin dispatch only: `event-record status`, `event-record project --source accepted-reference-id`, and `event-record validate` call into `core/protocol/event_record.py` and print explicit non-capability boundaries.

The work deliberately avoids event sourcing runtime, append-only runtime event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, and broad autonomous runtime behavior.

Validation is recorded in `.aide/queue/AIDE-BUILD-EVENT-RECORD-SCHEMA-01/evidence/validation.md`. Focused EventRecord tests cover schema shape, event family vocabulary, event type parsing, fail-closed unknown required event types, optional future event warnings, ReferenceID integration, projection immutability, report generation, CLI dispatch, parser preservation, and non-runtime boundaries.

Remaining issues are intentionally scoped: EventRecord is metadata-only and projection-only, full JSON Schema Draft 2020-12 validation is deferred, and the next recommended task is exactly `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`, not OKF.

## Work Item: AIDE-ACCEPT-REFERENCE-ID-SCHEME-01

Completed for review as a check-only acceptance gate for the minimal ReferenceID scheme slice.

Changed:

- `.aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/**`
- `.aide/reports/reference-id-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The acceptance reviewed `AIDE-BUILD-REFERENCE-ID-SCHEME-01` and `AIDE-CHECK-REFERENCE-ID-SCHEME-01`, including the ReferenceID schema/helper, thin CLI dispatch, generated ReferenceID reports, reference map, focused tests, warning disposition, and predecessor compatibility. The accepted capability is `minimal_reference_id_scheme` with stable `aide://<kind>/<id>` identity syntax, ReferenceID schema/helper/projection/validation, `reference-id status/project/validate`, deterministic reference-map reports, file paths as locators, optional SHA-256 locator metadata, required unknown-kind fail-closed behavior, and optional unknown-kind warnings.

The result is `ACCEPTED_WITH_WARNINGS`: no blocking defects were found, while full JSON Schema Draft 2020-12 validation, runtime reference resolution, EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and broader runtime remain intentionally deferred.

Validation covered the requested preflight commands with a corrected runner after one malformed wrapper attempt, ReferenceID status/project/validate, predecessor protocol validators, task inspect/evidence checks, JSON parsing, locator/SHA checks, broad repository validation, generated-report churn containment, and diff whitespace checks. Post-artifact validation is recorded in `.aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/evidence/validation.md`.

The work deliberately avoids ReferenceID repairs, EventRecord implementation, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, and broad autonomous runtime behavior.

The next recommended queue task is exactly `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`.

## Work Item: AIDE-CHECK-REFERENCE-ID-SCHEME-01

Completed for review as an independent check of the minimal ReferenceID scheme slice.

Changed:

- `.aide/queue/AIDE-CHECK-REFERENCE-ID-SCHEME-01/**`
- `.aide/reports/reference-id-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check reviewed `AIDE-BUILD-REFERENCE-ID-SCHEME-01`, commit `ae1089bf4d56dd8b46b29ee152ed7c27c8d07f3e`, the ReferenceID schema/helper, thin CLI dispatch, generated ReferenceID reports, reference map, focused tests, and predecessor protocol validation surfaces. The result is `PASS_WITH_WARNINGS`: no blocking defects were found, while full JSON Schema Draft 2020-12 validation, runtime registry/resolver behavior, EventRecord, OKF, PatchTransaction, adapter manifests, ContextPack v2, and broader runtime remain intentionally deferred.

Validation covered Python compile, focused ReferenceID tests, ReferenceID status/project/validate, predecessor protocol validators, JSON parsing, locator/SHA checks, task inspect/evidence checks, overclaim scans, broad repository validation, and diff whitespace checks. Preflight generated report churn outside the check scope was restored before writing check artifacts.

The work deliberately avoids implementation repairs, EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, and broad autonomous runtime behavior.

The next recommended queue task is `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`; EventRecord remains gated behind ReferenceID acceptance.

## Work Item: AIDE-BUILD-REFERENCE-ID-SCHEME-01

Implemented for review as the minimal ReferenceID scheme slice.

Changed:

- `core/protocol/reference_id.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-reference-id.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_reference_id_scheme.py`
- `.aide/reports/reference-id/**`
- `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The slice adds stable `aide://<kind>/<id>` identity parsing and formatting, fail-closed required-kind validation, optional future-kind warnings, locator hashing, ReferenceID record construction, additive reference-map projection, and local validation reports.

The AIDE Lite changes are thin dispatch only: `reference-id status`, `reference-id project`, and `reference-id validate` call into `core/protocol/reference_id.py` and print explicit non-capability boundaries.

The work deliberately avoids EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, and broad autonomous runtime behavior.

Validation is recorded in `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/evidence/validation.md`. Focused ReferenceID tests cover parser behavior, helper/schema alignment, projection immutability, CLI dispatch, compatibility preservation, and overclaim boundaries.

Remaining issues are intentionally scoped: ReferenceID is syntactic/projection-only, full JSON Schema Draft 2020-12 validation is deferred, and the next recommended task is `AIDE-CHECK-REFERENCE-ID-SCHEME-01`, not EventRecord.

## Work Item: AIDE-ACCEPT-TESTJOB-SCHEMA-01

Completed for review as an acceptance review of the minimal metadata-only TestJob schema slice.

Changed:

- `.aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/**`
- `.aide/reports/test-job-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The acceptance reviewed `AIDE-BUILD-TESTJOB-SCHEMA-01`, `AIDE-CHECK-TESTJOB-SCHEMA-01`, the accepted WorkerRun predecessor, generated TestJob reports, and the independent check evidence. The result is `ACCEPTED_WITH_WARNINGS`: the accepted capability is limited to metadata-only TestJob schema/helper/projection/validation behavior, additive projections, and `test-job status/project/validate` CLI dispatch.

Warnings are non-blocking: full JSON Schema Draft 2020-12 validation remains deferred, TestJob remains metadata-only, Test Broker runtime and async execution are not implemented, the latest task packet is stale relative to queue truth, the prior check corrected scan invocations by rerun, generated report churn must remain contained, and ReferenceID is the next task before PatchTransaction.

The work deliberately avoids implementation code changes, Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, and model/provider calls.

Validation is recorded in `.aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/test-and-validation-review.md`. The next recommended queue task is `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.

## Work Item: AIDE-CHECK-TESTJOB-SCHEMA-01

Completed for review as an independent check of the minimal metadata-only TestJob schema slice.

Changed:

- `.aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/**`
- `.aide/reports/test-job-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The check reviewed `AIDE-BUILD-TESTJOB-SCHEMA-01`, the TestJob schema/helper, CLI dispatch, focused tests, generated TestJob reports, and predecessor protocol validation surfaces. The result is `PASS_WITH_WARNINGS`: no blocking defects were found, while full JSON Schema Draft 2020-12 validation remains deferred, TestJob remains metadata-only, the latest task packet is stale relative to queue truth, and the attached frozen plan updates post-acceptance ordering to ReferenceID before PatchTransaction.

Validation covered Python compile, schema/report JSON parsing, 29 focused TestJob tests, `test-job status/project/validate`, WorkerRun/WorkUnit Queue/EvidencePacket/Contract Envelope validations, unsupported `test-job submit/run/retry/summarize` fail-closed checks, corrected secret and overclaim scans, task evidence inspection, and whitespace checks. Generated report churn from validation was restored before writing the check artifacts.

The work deliberately avoids implementation repairs, Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, and model/provider calls.

The next recommended queue task is `AIDE-ACCEPT-TESTJOB-SCHEMA-01`; after acceptance, the user-supplied frozen sequence points to `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.

## Work Item: AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01

Implemented for review as the minimal EvidencePacket schema slice.

Changed:

- `core/protocol/evidence_packet.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-evidence-packet.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_evidence_packet_schema.py`
- `.aide/reports/evidence-packet/**`
- `.aide/queue/AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The slice adds an envelope-backed `EvidencePacket` helper with required
metadata/spec/status validation, claim and validation status enums, explicit
non-capability preservation, unknown optional field tolerance, and unknown
required capability fail-closed behavior.

Generated projections convert accepted lifecycle fixture runner reports,
lifecycle acceptance, contract-envelope validation, and contract-envelope
acceptance into additive EvidencePacket JSON files. Source reports remain
canonical and are not destructively migrated.

The AIDE Lite changes are thin dispatch only: `evidence-packet status`,
`evidence-packet project --source accepted-slices`, and `evidence-packet
validate` call into `core/protocol/evidence_packet.py`.

The work deliberately avoids a full evidence engine, EvidenceStore, WorkUnit
schema or CLI, TestJob schema, Test Broker, Checkpoint, PromotionPolicy,
Service, Commander, provider adapters, branch/worktree automation, target
apply, active apply, rollback execution, release, promotion, network, Gateway,
GitHub mutation, and model/provider calls.

Validation is recorded in
`.aide/queue/AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01/evidence/validation.md`.
Focused EvidencePacket tests currently cover 35 helper, schema, projection, CLI,
compatibility, and overclaiming checks.

Remaining issues are intentionally scoped: EvidencePacket is minimal and
`v1alpha1`, full JSON Schema Draft 2020-12 validation is deferred, and the
evidence engine/WorkUnit/TestJob/Test Broker layers remain future work after
independent review and acceptance.

## Work Item: AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01

Implemented for review as contract-envelope schema runtime alignment.

Changed:

- `core/protocol/envelope.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_contract_envelope.py`
- `.aide/reports/contract-envelope/**`
- `.aide/reports/contract-envelope-harden/**`
- `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

The hardening loads `.aide/protocol/aide-envelope.schema.json` during
`contract-envelope validate`, executes a stdlib-only minimal JSON Schema subset
validator against generated envelope projections, and checks that the schema's
required public fields and basic types align with the helper validator.

Validation reports now state whether the schema file exists, loaded, parsed,
whether schema validation executed, which validation mode was used, whether
schema/helper alignment was checked, and which limitations remain. The CLI
prints those same status fields without moving runtime logic into
`.aide/scripts/aide_lite.py`.

Focused tests now cover schema parsing, required public fields, schema-based
missing-field and wrong-type rejection, unknown optional field tolerance,
unknown required capability fail-closed behavior, lifecycle run/verify
projection agreement, malformed projection rejection, alignment success and
failure, and validation report fields.

The work deliberately avoids a full JSON Schema engine, EvidencePacket schema,
WorkUnit schema or CLI, TestJob schema, Test Broker, Service, Commander,
providers, branch/worktree automation, target apply, active repo apply,
rollback execution, release, promotion, network, Gateway, GitHub mutation, and
model/provider calls.

Validation is recorded under
`.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01/evidence/validation.md`.
The next expected action is independent review via
`AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01`.

## Work Item: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01

Implemented for review as a temp-only lifecycle fixture runner.

Changed:

- `.aide/intake/latest-*`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/**`
- `.aide/queue/index.yaml`
- `.aide/reports/lifecycle-fixture-runner/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lifecycle_fixture_runner.py`
- `core/apply/__init__.py`
- `core/apply/lifecycle_fixture_runner.py`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

The task creates one protocol-shaped vertical slice rather than a kernel
scaffold. The runner loads the canonical `install-managed-section` fixture,
copies it into `.aide/reports/lifecycle-fixture-runner/workspaces/latest`,
applies the scoped managed-section transaction there, verifies the latest
completed run report, and emits rollback-compatible report evidence.

The implementation keeps `.aide/scripts/aide_lite.py` limited to parser and
dispatch wiring. Runner behavior is isolated behind small local seams:
`ScenarioLoader`, `TransactionCompiler`, `ScopedExecutor`, `FixtureVerifier`,
and `EvidenceReporter`.

The path-jail check resolves every mutating path under the temp workspace and
rejects absolute paths, parent traversal, wildcard paths, root mutation, and
symlink escapes. The emitted reports label the capability as
`fixture_temp_apply_only` and explicitly deny active repo apply, target repo
apply, general lifecycle apply, rollback execution, uninstall execution,
release readiness, and production readiness.

The implementation deliberately avoids AIDE kernel scaffolding, service,
Commander, provider adapters, branch/worktree automation, target-repo
mutation, network/model/Gateway calls, OpenTelemetry, SARIF, SPDX,
CycloneDX, SLSA, in-toto, OpenAPI, rollback execution, uninstall execution,
and release behavior.

Validation is recorded under
`.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/evidence/validation.md`.
The next expected action is independent review via
`AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`.

A follow-up alignment pass for the attached full build prompt added stable
`verify.json` / `verify.md` aliases, runner-level future and unfinished work
reports, six additional task-local evidence files, expanded negative
capability labels for service/Commander/provider-adapter readiness, and
focused tests for unsupported scenario/mode rejection, rollback non-execution,
report aliases, and the CLI-dispatch boundary.

## Work Item: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01

Implemented for review as lifecycle fixture temp-runner hardening.

Changed:

- `core/apply/lifecycle_fixture_runner.py`
- `.aide/scripts/tests/test_aide_lifecycle_fixture_runner.py`
- `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01/**`
- `.aide/queue/index.yaml`
- `.aide/reports/lifecycle-fixture-runner/**`
- `PLANS.md`
- `IMPLEMENT.md`

The hardening adds required run-report field checks, forbidden true
readiness/apply/rollback flag checks, rollback-compatible record parsing, and
rollback record truth checks during `lifecycle-fixture verify`.

Focused tests now cover unsupported operation and malformed plan rejection,
overclaiming fail-closed behavior, malformed rollback record fail-closed
behavior, missing required run fields, empty/wildcard path-jail rejection, and
missing managed-section marker failure.

The implementation deliberately avoids service, Commander, provider adapters,
branch/worktree automation, target repo apply, active repo apply, rollback
execution, uninstall execution, release, promotion, network, Gateway, GitHub
mutation, and model/provider calls.

Validation is recorded under
`.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01/evidence/validation.md`.

## Work Item: AIDE-BUILD-CONTRACT-ENVELOPE-01

Implemented for review as a minimal contract envelope slice.

Changed:

- `core/protocol/envelope.py`
- `core/protocol/__init__.py`
- `.aide/protocol/aide-envelope.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_contract_envelope.py`
- `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-01/**`
- `.aide/queue/index.yaml`
- `.aide/reports/contract-envelope/**`
- `PLANS.md`
- `IMPLEMENT.md`

The slice adds a small `apiVersion` / `kind` / `metadata` / `spec` /
`status` envelope helper, SemVer-like compatibility validation, unknown
optional-field tolerance, unknown required-capability rejection, and additive
projections for the accepted lifecycle fixture run, verify, and acceptance
reports.

The implementation deliberately avoids full kernel schemas, WorkUnit CLI, Test
Broker, Service, Commander, provider adapters, branch/worktree automation,
target repo apply, active repo apply, rollback execution, uninstall execution,
release, promotion, network, Gateway, GitHub mutation, and model/provider calls.

Validation is recorded under
`.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-01/evidence/validation.md`.

## Work Item: AI-LONG-TURN-OPERATING-PROTOCOL-00

Implemented for review as a docs-only long-turn operating protocol.

Changed:

- `.aide/intake/latest-*`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/**`
- `.aide/queue/index.yaml`
- `docs/planning/ai_long_turn_protocol/**`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`

The attached prompt was compiled through AIDE intake before implementation.
The broader prompt was blocked by the deterministic compiler because it mixed
docs work with branch-sensitive and publication-class language, so this
WorkUnit records a safe docs-only split. The protocol adds templates for
single-task, connected-queue, and long-turn prompts plus commit cadence,
validation ladder, stop conditions, evidence rules, final report format, and
failure recovery guidance.

The implementation deliberately avoids runtime behavior, branch mutation,
publication action, target-repo mutation, provider/model calls, Gateway calls,
network calls, external discovery execution, and evidence fabrication.

Validation is recorded under
`.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/evidence/validation.md`.

## Work Item: AIDE-REVIEW-APPLY-00

Implemented for review as the acceptance checkpoint for AIDE-APPLY-00 and AIDE-CHECK-APPLY-00.

Changed:

- `.aide/queue/AIDE-REVIEW-APPLY-00-transaction-model-review-acceptance/**`
- `.aide/reports/apply-review-00-*.md`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- generated validation and review artifacts
- `PLANS.md`
- `IMPLEMENT.md`

The review accepts AIDE-APPLY-00 and AIDE-CHECK-APPLY-00 with notes, confirms the no-real-apply boundary, classifies known warnings, and leaves AIDE-APPLY-01 as the next fixture-safe managed-section patcher task.

The implementation deliberately avoids AIDE-APPLY-01 code, real repository apply, target mutation, branch/worktree mutation, merge/push/promotion, tag/release/publication, GitHub API mutation, provider/model/network calls, Gateway forwarding, and install/repair/upgrade/rollback/uninstall apply behavior.

Validation is recorded under `.aide/queue/AIDE-REVIEW-APPLY-00-transaction-model-review-acceptance/evidence/validation.md`.

## Work Item: AIDE-CHECK-APPLY-00

Implemented for review as an audit-only checkpoint for AIDE-APPLY-00.

Changed:

- `.aide/queue/AIDE-CHECK-APPLY-00-transaction-model-review/**`
- `.aide/reports/apply-check-00-*.md`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- report-only preflight outputs under `.aide/intake/latest-*`, `.aide/git/latest-helper-plan.*`, `.aide/git/aide-dev-main-plan.*`, and `.aide/reports/task-os-*`

The checkpoint reviews transaction model schemas, examples, docs, command surface, evidence, generated transaction reports, export-pack inclusion, and no-real-apply boundaries before AIDE-APPLY-01. It records `PASS_WITH_NOTES`: no apply-capable transaction command was found, rollback records remain non-executable evidence, managed-section behavior is modeled but not implemented, and AIDE-APPLY-01 remains the next appropriate queue item.

The implementation deliberately avoids managed-section patcher code, real repository apply, target mutation, branch/worktree mutation, merge/push/promotion, tag/release/publication, GitHub API mutation, provider/model/network calls, Gateway forwarding, and install/repair/upgrade/rollback/uninstall apply behavior.

Validation is recorded under `.aide/queue/AIDE-CHECK-APPLY-00-transaction-model-review/evidence/validation.md`.

## Work Item: X-OS-01

Implemented for review as local Task OS report-only inspection and planning commands.

Changed:

- `.aide/queue/X-OS-01-aide-task-os-report-only-commands/**`
- `.aide/reports/task-os-*`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_x_os_01_task_os_commands.py`
- `.aide/evals/golden-tasks/task_os_*_golden/**`
- `.aide/evals/golden-tasks/catalog.yaml`
- `docs/reference/task-os-report-only-commands.md`
- `docs/reference/task-os-v0.md`
- `docs/reference/README.md`
- `.aide/tasks/README.md`
- `.aide/ledgers/README.md`

X-OS-01 adds `task status`, `task classify`, `task repair-plan`,
`task requeue-plan`, `task resume-plan`, `blocker status`, `blocker classify`,
`wave status`, `wave plan`, `checkpoint status`, and `checkpoint plan`.
The commands write deterministic `.aide/reports/task-os-*` evidence and
surface lifecycle, blocker, repair, requeue, resume, wave, checkpoint, and
next-plan information without executing tasks or applying repairs.

The implementation deliberately keeps task execution, scheduler/worker
behavior, repair apply, requeue apply, checkpoint apply, branch/worktree
mutation, GitHub mutation, release publication, target-repo mutation,
provider/model calls, and network calls out of scope.

Validation is recorded under
`.aide/queue/X-OS-01-aide-task-os-report-only-commands/evidence/validation.md`.
X-OS-02 remains the next planned Task OS phase for Capability Reality Ledger v0.

## Work Item: X-OS-00

Implemented for review as the Task OS v0 schema and policy foundation.

Changed:

- `.aide/queue/X-OS-00-aide-task-os-schemas-policies/**`
- `.aide/policies/task-lifecycle.yaml`
- `.aide/policies/blockers.yaml`
- `.aide/policies/repair-loop.yaml`
- `.aide/policies/waves.yaml`
- `.aide/policies/checkpoints.yaml`
- `.aide/policies/dev-main-promotion.yaml`
- `.aide/policies/capability-reality.yaml`
- `.aide/tasks/**`
- `.aide/ledgers/**`
- `.aide/examples/task-os/**`
- `.aide/evals/golden-tasks/task_os_*_golden/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_x_os_00_task_os.py`
- `docs/reference/task-os-v0.md`
- `docs/reference/workunit-lifecycle.md`
- `docs/reference/blocker-and-repair-model.md`
- `docs/reference/checkpoint-and-promotion-model.md`

X-OS-00 defines lifecycle state, blocker, repair, wave, checkpoint, branch
provenance, and capability reality contracts, plus examples and local
validation. It does not add a `task-os` command group, execute repairs,
operate workers, mutate branches, mutate target repositories, call
providers/models/network services, merge, promote, publish releases, or apply
changes outside the source policy/schema/docs/eval surface.

The next expected phase is X-OS-01 Task OS report-only commands.

## Work Item: Q48

Implemented for review as local-only GitHub Release draft generation from the
Q47 AIDE Lite release bundle.

Changed:

- `.aide/queue/Q48-github-release-draft-v0/**`
- `.aide/policies/github-release-draft.yaml`
- `.aide/policies/release-publication-boundary.yaml`
- `.aide/policies/release-upload-plan.yaml`
- `.aide/policies/release-checklist.yaml`
- `.aide/release/github-release-*.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q48_github_release_draft.py`
- `.aide/evals/golden-tasks/**`
- `docs/reference/github-release-draft.md`

Q48 generates local draft Markdown/JSON, asset lists with checksums, no-upload
plans, publication checklists, publication-boundary reports, and draft
validation. It does not create tags, call GitHub APIs, create GitHub Releases,
upload assets, publish packages, mutate branches, install CI, mutate target
repos, call providers/models/network, or apply install/repair/upgrade/rollback/
uninstall actions.

The next phase is Q49 Dominium Fresh Install Preflight, because target install
readiness still needs target-local evidence.

## Work Item: Q47

### Status

Implemented for review as local-only AIDE Lite release bundle generation and
validation.

### Scope

- `.aide/queue/Q47-aide-lite-release-bundle-v0/**`
- `.aide/policies/release-bundle.yaml`
- `.aide/policies/release-artifacts.yaml`
- `.aide/policies/release-provenance.yaml`
- `.aide/policies/release-validation.yaml`
- `.aide/policies/release-versioning.yaml`
- `.aide/release/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q47_release_bundle.py`
- `.aide/evals/golden-tasks/release_*_golden/**`
- docs, latest Q48 task packet, and export-pack updates

### Rationale

Q47 turns the validated portable AIDE Lite Pack into local downloadable
artifacts before any public release draft or publication work. The bundle must
be inspectable, checksummed, extractable, and explicit about its no-publish and
no-apply boundaries before target installation or upgrade phases can use it as
a stable source.

### Notable Design Decisions

The release command surface uses Python standard-library archive, checksum, and
temporary extraction support only. Archives are built from
`.aide/export/aide-lite-pack-v0/`, not from arbitrary source paths, and release
validation rejects forbidden archive paths such as `.git/`, `.aide.local/`,
`.env`, secrets, and raw prompt or response logs.

### Tradeoffs

Q47 can generate `.zip` and `.tar.gz` archives locally, but it deliberately
does not publish them, tag a commit, upload artifacts, create a GitHub Release,
or install AIDE into a target repository. Release notes and changelog copies
remain preview-only.

### Verification

Q47 evidence records release bundle generation, archive extraction validation,
checksum verification, forbidden-path checks, targeted release tests, golden
tasks, pack-status, and broader AIDE validation.

### Regressions Avoided

No Git tag, GitHub Release, artifact upload, branch mutation, target-repo
mutation, active CI installation, install/repair/upgrade/rollback/uninstall
apply, provider/model/network call, or release publication is introduced.

### Remaining Issues

- Q47 is local bundle generation only; Q48 is needed for GitHub Release draft
  planning.
- Target repositories still need their own install, repair, upgrade, rollback,
  or uninstall preflights.
- Apply-capable install and upgrade behavior remains future-gated.

## Work Item: QFIX-05

### Status

Implemented for review as a bounded release-readiness warning reconciliation.

### Changed Paths

- `.aide/queue/QFIX-05-release-readiness-warning-reconciliation/**`
- `.aide/queue/index.yaml`
- `.aide/generated/manifest.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The broad request to make every prior task production-ready cannot safely bypass
AIDE queue law or review gates. QFIX-05 inventories the current state, fixes the
mechanical generated-manifest warning, and records the remaining release
blockers explicitly.

### Notable Design Decisions

- Preserved Q36-Q46 and QFIX-04 as `needs_review`.
- Used the deterministic Harness compiler for generated artifact refresh.
- Treated release publication, tag creation, GitHub mutation, branch mutation,
  target repo mutation, and provider/model/network calls as out of scope.

### Verification

Validation is recorded in
`.aide/queue/QFIX-05-release-readiness-warning-reconciliation/evidence/validation.md`.

### Remaining Issues

Immediate public release is still blocked by review gates and the future Q48
release-draft phase.

## Work Item: QFIX-04

### Status

Implemented for review as a bounded AIDE Lite selftest performance hotfix.

### Changed Paths

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_golden_tasks.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/queue/QFIX-04-aide-lite-selftest-performance/**`
- `.aide/queue/index.yaml`

### Rationale

The broad performance request was not safe to execute as a speculative
repo-wide rewrite. Profiling identified one concrete hot path: AIDE Lite
`test`/`selftest` spent most of its time running the full golden-task catalog,
even though full catalog validation is already available through `eval run`.

### Notable Design Decisions

- Kept full `eval run` behavior intact.
- Limited selftest golden coverage to a representative smoke set.
- Reused one context compilation result for snapshot, index, and context
  assertions.
- Avoided repeated path normalization in ignore matching.

### Verification

Validation is recorded in
`.aide/queue/QFIX-04-aide-lite-selftest-performance/evidence/validation.md`.

### Remaining Issues

This is not a complete performance program. Follow-up WorkUnits should target
full golden-task data caching, inventory scan reuse, and harness subprocess
overhead.

## Work Item: Q46

### Status

Implemented for review as deterministic rollback and uninstall observe/plan/
dry-run planning with preservation-first ownership gates.

### Scope

- `.aide/queue/Q46-rollback-uninstall-model-v0/**`
- `.aide/policies/rollback.yaml`
- `.aide/policies/rollback-classes.yaml`
- `.aide/policies/rollback-safety.yaml`
- `.aide/policies/rollback-verification.yaml`
- `.aide/policies/uninstall.yaml`
- `.aide/policies/uninstall-classes.yaml`
- `.aide/policies/uninstall-safety.yaml`
- `.aide/policies/uninstall-verification.yaml`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q46_rollback_uninstall.py`
- `.aide/evals/golden-tasks/rollback_*_golden/**`
- `.aide/evals/golden-tasks/uninstall_*_golden/**`
- docs, latest Q47 task packet, and export-pack updates

### Rationale

Q46 closes the no-apply install governance loop created by Q43-Q45. Future
target installs, repairs, and upgrades need explicit rollback and uninstall
contracts before any target mutation can be reviewed as reversible.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q46. Rollback and uninstall read install ownership ledgers and prior
install, upgrade, or repair plans when present, but missing ownership evidence
does not become removal permission. Unknown ownership is preserved, blocked, or
sent to manual review.

### Tradeoffs

The current AIDE-source rollback and uninstall plans are conservative. They may
list many portable-file future candidates, but all operations carry
`apply_allowed: false`, deletion and managed-section removal are disabled by
default, and target-specific state is preserved.

### Verification

Q46 evidence records rollback observe/plan/dry-run/validate/status/classes/
explain commands, uninstall observe/plan/dry-run/validate/status/classes/
explain commands, targeted Q46 tests, golden tasks, pack-status, and broader
AIDE validation.

### Regressions Avoided

No rollback apply, uninstall apply, install apply, repair apply, upgrade apply,
delete, overwrite, managed-section removal, migration apply, file move,
reference rewrite, target-repo mutation, branch mutation, provider/model/network
call, release publishing, or source-generated rollback/uninstall plan export is
introduced.

### Remaining Issues

- Q46 is planning only; rollback apply, uninstall apply, and release bundle
  behavior remain future phases.
- Target repositories must generate their own rollback and uninstall plans.
- Q47 AIDE Lite Release Bundle v0 is needed before a release-shaped portable
  bundle can be reviewed.

## Work Item: Q45

### Status

Implemented for review as deterministic observe-current/observe-source/compare/
plan/dry-run upgrade planning and compatibility reporting.

### Scope

- `.aide/queue/Q45-upgrade-model-v0/**`
- `.aide/policies/upgrade.yaml`
- `.aide/policies/upgrade-compatibility.yaml`
- `.aide/policies/upgrade-preservation.yaml`
- `.aide/policies/upgrade-conflicts.yaml`
- `.aide/policies/upgrade-migrations.yaml`
- `.aide/policies/upgrade-verification.yaml`
- `.aide/upgrade/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q45_upgrade_model.py`
- `.aide/evals/golden-tasks/upgrade_*_golden/**`
- docs, latest Q46 task packet, and export-pack updates

### Rationale

Q45 turns Q43 install planning and Q44 repair diagnosis into upgrade planning
infrastructure. Future target upgrades can compare current installed AIDE state
to a source pack, preserve target-specific memory and evidence, classify
compatibility, and dry-run candidate updates before any target file is changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q45. It reads export-pack manifests and payloads when present,
preserves target queue, memory, evidence, generated target state, target golden
tasks, manual guidance, and existing tools, and writes generated planning
outputs under `.aide/upgrade/`.

### Tradeoffs

Compatibility classification is structural and conservative. When evidence is
uncertain, the plan uses warning, preserve, skip, manual review, or future
migration language rather than treating a difference as safe to apply.

### Verification

Q45 evidence records upgrade observe-current/observe-source/compare/plan/
dry-run/validate/status/compatibility/conflicts/migrations/explain commands,
targeted Q45 tests, golden tasks, pack-status, and broader AIDE validation.

### Regressions Avoided

No upgrade apply, install apply, repair apply, overwrite, delete, migration
apply, file move, reference rewrite, target-repo mutation, branch mutation,
provider/model/network call, release publishing, or source-generated upgrade
plan export is introduced.

### Remaining Issues

- Q45 is planning only; upgrade apply, rollback, uninstall, and release bundle
  behavior remain future phases.
- Target repositories must generate their own upgrade observations and plans.
- Q46 Rollback / Uninstall Model v0 is needed before future apply phases can
  rely on reversible target mutation contracts.

## Work Item: Q44

### Status

Implemented for review as deterministic observe/diagnose/plan/dry-run repair
planning and advisory doctor reporting.

### Scope

- `.aide/queue/Q44-repair-doctor-model-v0/**`
- `.aide/policies/repair.yaml`
- `.aide/policies/repair-classes.yaml`
- `.aide/policies/repair-safety.yaml`
- `.aide/policies/repair-detection.yaml`
- `.aide/policies/repair-verification.yaml`
- `.aide/policies/doctor.yaml`
- `.aide/repair/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q44_repair_doctor.py`
- `.aide/evals/golden-tasks/repair_*_golden/**`
- docs, latest Q45 task packet, and export-pack updates

### Rationale

Q44 turns Q43 install planning, conflict reporting, preservation rules, and
pack references into repair diagnosis infrastructure. Future target repairs can
be observed, classified, planned, dry-run, and reviewed before any target file
is changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q44. It reads install artifacts and pack files when present, writes
generated planning outputs under `.aide/repair/`, preserves target memory,
queue, evidence, docs, tools, and manual content, and treats local state,
secrets, unsupported schemas, and source-state contamination as blockers or
manual-review issues rather than automatic repair work.

### Verification

Q44 evidence records repair observe/diagnose/plan/dry-run/validate/status/
classes/doctor/explain commands, targeted unit tests, golden tasks, AIDE Lite
validation, export-pack regeneration, pack-status, diff checks, core unittest
suites where available, and secret scan results.

### Remaining Issues

- Q44 is planning only; repair apply, upgrade, rollback, uninstall, and install
  apply behavior remain future work.
- Repair classification is heuristic and must be reviewed before target
  mutation.
- Target repositories must generate their own `.aide/repair/latest-*` outputs;
  AIDE source-generated repair outputs are not portable target truth.
- Q45 Upgrade Model v0 is needed before upgrade decisions can use repair
  diagnosis and install preservation evidence.

## Work Item: Q43

### Status

Implemented for review as deterministic observe/plan/dry-run install planning.

### Scope

- `.aide/queue/Q43-install-plan-model-v0/**`
- `.aide/policies/install.yaml`
- `.aide/policies/install-preservation.yaml`
- `.aide/policies/install-ownership.yaml`
- `.aide/policies/install-conflicts.yaml`
- `.aide/policies/install-migrations.yaml`
- `.aide/policies/install-verification.yaml`
- `.aide/install/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q43_install_plan.py`
- `.aide/evals/golden-tasks/install_*_golden/**`
- docs, command catalog, latest Q44 task packet, and export-pack updates

### Rationale

Q43 turns Q37-Q42 repo, quality, refactor, root, tool, and map evidence into
install planning infrastructure. Future target installs can be observed,
planned, dry-run, reviewed, and checked for preservation, ownership, conflicts,
mandatory migration candidates, and verification before any target file is
changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q43. It reads the current portable pack when present, writes
generated planning outputs under `.aide/install/`, preserves target memory,
queue, evidence, docs, tools, and manual content, and treats source-generated
state as evidence to regenerate locally rather than target truth.

### Verification

Q43 evidence records install observe/plan/dry-run/validate/status/ownership/
conflicts/explain commands, targeted unit tests, golden tasks, AIDE Lite
validation, export-pack regeneration, pack-status, diff checks, core unittest
suites where available, and secret scan results.

### Remaining Issues

- Q43 is planning only; install apply, repair, upgrade, rollback, and uninstall
  behavior remain future work.
- Conflict and ownership classification is heuristic and must be reviewed before
  target mutation.
- Target repositories must generate their own `.aide/install/latest-*` outputs;
  AIDE source-generated install outputs are not portable target truth.
- Q44 Repair / Doctor Model v0 is needed before repair decisions can consume
  Q43 conflict and preservation evidence.

## Work Item: Q42

### Status

Implemented for review as deterministic no-apply map and alias planning.

### Scope

- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/**`
- `.aide/policies/move-map.yaml`
- `.aide/policies/salvage-map.yaml`
- `.aide/policies/path-aliases.yaml`
- `.aide/policies/reference-rewrite.yaml`
- `.aide/policies/migration-ledger.yaml`
- `.aide/refactors/*map*.schema.json`
- `.aide/refactors/path-alias*.schema.json`
- `.aide/refactors/reference-rewrite*.schema.json`
- `.aide/refactors/migration-ledger*.schema.json`
- `.aide/refactors/current-*`, `path-aliases.*`, `reference-rewrite-plan.*`, `migration-ledger.draft.jsonl`, and `map-validation-report.*`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q42_move_map_aliases.py`
- `.aide/evals/golden-tasks/*map*_golden/**`
- `.aide/evals/golden-tasks/path_alias_policy_golden/**`
- `.aide/evals/golden-tasks/reference_rewrite_plan_golden/**`
- `.aide/evals/golden-tasks/migration_ledger_policy_golden/**`
- docs, command catalog, latest Q43 task packet, and export-pack updates

### Rationale

Q42 turns Q37 repo intelligence, Q38 quality evidence, Q39 refactor controls,
Q40 root evidence, and Q41 tool preservation plans into map-level planning
evidence. Future install, repair, upgrade, rollback, root recycling, and tool
absorption phases can cite candidate path mappings before any file move,
salvage extraction, alias, shim, or reference rewrite is considered.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
candidate-only in Q42. It writes current move/salvage/alias/rewrite/ledger
draft artifacts under `.aide/refactors/`, but every current entry remains
`apply_allowed: false`. It never moves files, deletes files, rewrites
references, creates aliases or shims, applies maps, mutates branches, mutates
target repos, calls providers/models/network services, or treats
`drop_candidate` as deletion approval.

### Verification

Final Q42 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, roots, tools, and map commands, Q42 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q42 is candidate planning only; no concrete Dominium, Eureka, or AIDE root
  migration is implemented.
- Current move-map generation is intentionally sparse until a future reviewed
  task selects a concrete root or target path plan.
- No alias, shim, salvage extraction, reference rewrite, install, repair,
  upgrade, rollback, or apply behavior exists yet.
- Target repositories must generate their own maps after import; source
  `.aide/refactors/current-*` outputs are not portable target truth.

## Work Item: Q41

### Status

Implemented for review as deterministic no-execution existing-tool absorption
planning.

### Scope

- `.aide/queue/Q41-existing-tool-absorption-v0/**`
- `.aide/policies/tool-absorption.yaml`
- `.aide/policies/tool-inventory.yaml`
- `.aide/policies/tool-fates.yaml`
- `.aide/policies/tool-wrapping.yaml`
- `.aide/policies/tool-risk.yaml`
- `.aide/policies/tool-capabilities.yaml`
- `.aide/tools/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q41_tool_absorption.py`
- `.aide/evals/golden-tasks/tool_*_golden/**`
- `.aide/evals/golden-tasks/tools_no_execution_golden/**`
- docs, command catalog, latest Q42 task packet, and export-pack updates

### Rationale

Q41 turns Q37 repo intelligence, Q38 quality evidence, Q39 refactor controls,
and Q40 root evidence into tool-level planning evidence. Future target repos
can discover XStack, AuditX, RepoX, TestX, project validators, scripts,
command catalogs, and CI wrappers before AIDE decides whether to keep, wrap,
adapt, extract, convert, shim, or leave them for review.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-execution in Q41. It writes `.aide/tools/` inventory, classification, wrap
plan, adapter map, and risk outputs. It never executes unknown tools, deletes
tools, renames tools, migrates tools, actively wraps tools, mutates branches,
mutates target repos, calls providers/models/network services, or treats
`drop_candidate` as deletion approval.

### Verification

Final Q41 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, roots, and tools commands, Q41 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q41 is advisory planning only; no concrete Dominium XStack/AuditX/RepoX/TestX
  or Eureka validator absorption is implemented.
- No active wrappers, current move maps, salvage maps, path aliases, install,
  upgrade, rollback, or apply behavior exists yet.
- Tool capabilities and risks are deterministic heuristics, not semantic proof.
- Target repositories must generate their own tool inventories after import;
  source-generated `.aide/tools/latest-*` outputs are not portable target truth.

## Work Item: Q40

### Status

Implemented for review as deterministic no-apply root recycling planning.

### Scope

- `.aide/queue/Q40-root-recycling-framework-v0/**`
- `.aide/policies/root-recycling.yaml`
- `.aide/policies/root-inventory.yaml`
- `.aide/policies/root-fates.yaml`
- `.aide/policies/root-exceptions.yaml`
- `.aide/policies/root-risk.yaml`
- `.aide/refactors/root-*.schema.json`
- `.aide/roots/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q40_root_recycling.py`
- `.aide/evals/golden-tasks/root_*_golden/**`
- `.aide/evals/golden-tasks/roots_no_apply_golden/**`
- docs, command catalog, latest Q41 task packet, and export-pack updates

### Rationale

Q40 turns Q37 repo intelligence, Q38 quality evidence, and Q39 refactor
controls into root-level planning evidence. Future root cleanup can now start
with deterministic root inventory, root status, risk, exception, and per-file
fate candidates instead of broad folder movement or deletion prompts.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q40. It writes `.aide/roots/` inventory, classification, plan,
exception, and risk outputs. It never moves roots, deletes files, rewrites
references, applies maps, absorbs tools, mutates branches, mutates target
repos, calls providers/models/network services, or treats `drop_candidate` as
deletion approval.

### Verification

Final Q40 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, and roots commands, Q40 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q40 is dry-run planning only; existing tool absorption starts in Q41.
- No real current move map, salvage map, path alias, tool absorption, install,
  upgrade, rollback, or apply behavior exists yet.
- Root risks and file fates are deterministic heuristics, not semantic proof.
- Target repositories must generate their own root inventories after import;
  source-generated `.aide/roots/latest-*` outputs are not portable target truth.

## Work Item: Q39

### Status

Implemented for review as deterministic no-apply refactor planning.

### Scope

- `.aide/queue/Q39-refactor-control-plane-v0/**`
- `.aide/policies/refactor.yaml`
- `.aide/policies/migration.yaml`
- `.aide/policies/refactor-safety.yaml`
- `.aide/policies/refactor-evidence.yaml`
- `.aide/policies/refactor-application.yaml`
- `.aide/refactors/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q39_refactor_control.py`
- `.aide/evals/golden-tasks/*refactor*_golden/**`
- `.aide/evals/golden-tasks/*migration*_golden/**`
- docs, command catalog, latest Q40 task packet, and export-pack updates

### Rationale

Q39 turns Q37 repo intelligence and Q38 quality evidence into a governed
planning substrate for future structural change. Refactors can now be expressed
as dry-run plans with operations, risks, validation, evidence, rollback notes,
move maps, salvage maps, path aliases, and migration-ledger records before any
future apply phase is considered.

### Notable Design Decisions

The refactor control plane is deterministic, repo-local, Python
standard-library only, and no-apply in Q39. It writes `.aide/refactors/`
readiness/example artifacts and schema records. It never moves, deletes,
rewrites references, applies migrations, mutates branches, mutates target
repos, calls providers/models/network services, or treats `drop_candidate` as
deletion approval.

### Verification

Final Q39 evidence records Harness validation, AIDE Lite validation, repo and
quality prerequisite commands, refactor commands, Q39 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q39 is dry-run planning only; concrete root recycling starts in Q40.
- No real current move map, salvage map, path alias, tool absorption, install,
  upgrade, rollback, or apply behavior exists yet.
- Target repositories must generate their own refactor readiness after import;
  source-generated `.aide/refactors/latest-*` outputs are not portable target
  truth.

## Work Item: Q38

### Status

Implemented for review as deterministic file quality measurement.

### Scope

- `.aide/queue/Q38-file-quality-ledger-v0/**`
- `.aide/policies/file-quality.yaml`
- `.aide/policies/docs-consistency.yaml`
- `.aide/policies/module-quality.yaml`
- `.aide/policies/reuse-modularity.yaml`
- `.aide/quality/**`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`
- `.aide/reports/module-quality-report.md`
- `.aide/reports/docs-consistency-report.md`
- `.aide/reports/test-coverage-map.md`
- `.aide/reports/reuse-modularity-report.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q38_file_quality.py`
- `.aide/evals/golden-tasks/*quality*_golden/**`
- docs, command catalog, latest Q39 task packet, and export-pack updates

### Rationale

Q38 turns Q37 repo intelligence into advisory quality evidence so future
WorkUnits can target small, bounded ownership, documentation, test, stale-link,
generated-boundary, module, and reuse issues instead of broad cleanup prompts.

### Notable Design Decisions

The ledger is deterministic, repo-local, Python standard-library only, and
advisory-only. It writes `.aide/reports/` quality JSON/Markdown outputs and
uses warning/candidate language. It never moves, deletes, refactors, migrates,
calls providers/models/network services, mutates target repos, or auto-fixes
source, docs, or tests.

### Verification

Final Q38 evidence records Harness validation, AIDE Lite validation, repo and
quality commands, Q38 unit tests, golden tasks, export-pack regeneration,
pack-status, core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Quality records are deterministic heuristics, not semantic quality proof.
- Warning counts are advisory and require future WorkUnits or human review.
- Orphan and reuse candidates are not deletion candidates.
- Target repositories must generate their own quality ledgers after import;
  source-generated `.aide/reports/file-quality-*` outputs are not portable
  target truth.

## Work Item: Q37

### Status

Implemented for review as deterministic repo intelligence indexing.

### Scope

- `.aide/queue/Q37-repo-intelligence-index-v0/**`
- `.aide/policies/repo-intelligence.yaml`
- `.aide/policies/file-classification.yaml`
- `.aide/policies/ownership-map.yaml`
- `.aide/policies/dependency-map.yaml`
- `.aide/policies/test-map.yaml`
- `.aide/policies/doc-link-map.yaml`
- `.aide/repo/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q37_repo_intelligence.py`
- `.aide/evals/golden-tasks/repo_*_golden/**`
- docs, command catalog, latest Q38 task packet, and export-pack updates

### Rationale

Q37 gives future WorkUnits a deterministic repo-state substrate so they do not
rediscover the file tree through long prompts or chat memory. The generated
indexes classify tracked files, owners, references, tests, docs, generated
artifacts, and conservative orphan candidates before later quality or refactor
phases act.

### Notable Design Decisions

The indexer is deterministic, repo-local, Python standard-library only, and
index-only. It reads git-tracked files when available, falls back to a bounded
filesystem walk, excludes `.git` and `.aide.local/`, computes hashes and sizes,
and writes `.aide/repo` JSON/Markdown outputs. It never moves, deletes,
refactors, migrates, calls providers/models/network services, mutates target
repos, or treats orphan candidates as deletion advice.

### Verification

Final Q37 evidence records Harness validation, AIDE Lite validation, repo
commands, Q37 unit tests, golden tasks, export-pack regeneration, pack-status,
core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Classification, dependency, test, and doc-link maps are heuristic and
  conservative.
- Unknown files and orphan candidates require Q38/Q39 follow-up before any
  quality judgment or refactor action.
- Target repositories must generate their own repo intelligence after import;
  source-generated `.aide/repo/*.json` outputs are not portable target truth.

## Work Item: Q36

### Status

Implemented for review as deterministic intent compilation and prompt
normalization.

### Scope

- `.aide/queue/Q36-intent-compiler-prompt-normalization-v0/**`
- `.aide/policies/intent.yaml`
- `.aide/policies/workunit-sizing.yaml`
- `.aide/policies/task-classes.yaml`
- `.aide/policies/risk-classes.yaml`
- `.aide/policies/prompt-normalization.yaml`
- `.aide/intake/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q36_intent_compiler.py`
- `.aide/evals/golden-tasks/intent_*_golden/**`
- `.aide/evals/golden-tasks/workunit_sizing_policy_golden/**`
- docs, command catalog, latest Q37 task packet, and export-pack updates

### Rationale

Q36 closes the raw-prompt execution gap left after Q27-Q35 governance work.
Raw prompts such as `next`, `fix everything`, `clean up the repo`, destructive
delete requests, Git promotion requests, release requests, and target install
requests now compile into reviewable intent packets and WorkUnit drafts before
any implementation work can begin.

### Notable Design Decisions

The compiler is deterministic, repo-local, Python standard-library only, and
compile-only. It reads repo policy, queue/latest-task state, and local branch
state; stores a prompt hash plus bounded excerpt; writes latest intent packet
and WorkUnit draft artifacts; and never calls providers, models, outbound
network services, GitHub APIs, Gateway forwarding, target repos, or branch
mutation commands.

### Verification

Final Q36 evidence records Harness validation, AIDE Lite validation, targeted
intent prompts, Q36 unit tests, golden tasks, export-pack regeneration,
pack-status, core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Classification confidence is heuristic and intentionally conservative.
- Q37 should add a Repo Intelligence Index so future intent packets can cite
  richer repo-local ownership and quality data.
- Q36 does not execute compiled WorkUnits, mutate targets, publish releases,
  apply GitHub/CI settings, or run provider/model/network calls.

## Work Item: Q35

### Status

Implemented as report-only GitHub protection and CI advisory tooling.

### Scope

- `.aide/queue/Q35-github-protection-ci-advisory-v0/**`
- `.aide/policies/github-protection.yaml`
- `.aide/policies/ci-gates.yaml`
- `.aide/policies/branch-protection.yaml`
- `.aide/github/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q35_github_advisory.py`
- `.aide/evals/golden-tasks/github_*_golden/**`
- `docs/reference/github-protection-ci-advisory.md`
- export-pack, command catalog, queue index, and compact docs updates

### Rationale

QCHECK-03 found Q35 missing, which left the GitHub command family unavailable
and kept Q36 planning conditional. Q35 closes that AIDE-local blocker by adding
advisory policies, generated reports, commands, tests, and export-pack support.

### Notable Design Decisions

The Q35 command family is deliberately report-only. It writes `.aide/github`
advisory artifacts but does not call GitHub APIs, create `.github/workflows`,
activate CI, mutate branches, push, create tags, publish releases, or call
providers/models/network.

### Verification

The final Q35 evidence records the full command set. Required gates include
Harness validate/doctor/self-check, AIDE Lite validate/test/selftest/eval,
GitHub advisory commands, commit check, changelog validate, Git policy,
export-pack, pack-status, core unittest suites, and secret scan.

### Remaining Issues

Active GitHub protection and CI installation remain future apply-capable work
that requires dry-run evidence, rollback, operator approval, and review gates.

## Work Item: QFIX-03

### Status

Implemented as warning and review reconciliation; accepted with notes in the
queue state.

### Scope

- `.aide/queue/**/status.yaml`
- `.aide/queue/**/task.yaml`
- `.aide/queue/index.yaml`
- `.aide/generated/manifest.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/policies/changelog.yaml`
- `.aide/policies/token-budget.yaml`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`
- `.aide/profile.yaml`
- `.aide/memory/**`
- `core/harness/**`
- `core/compat/**`
- root documentation summaries

### Implementation Notes

QFIX-03 resolved the stale generated-manifest warning, reconciled completed
review-gated queue items from task-local evidence, and converted Q25-Q31/Q34
from pending review to `passed_with_notes`. The review reconciliation explicitly
does not claim product readiness, live provider/model calls, release readiness,
target-repo mutation, live branch mutation, or generated outputs as canonical
truth.

Q34 changelog preview now treats malformed or legacy history as reportable
review findings rather than a command-level warning. The malformed commit report
and JSON counts remain in place so old history is not hidden.

Harness doctor/self-check guidance reported the reconciled queue state and
pointed to Q35 at the time of QFIX-03, rather than stale Q25/Q26/Q27 review guidance. The token ledger
now distinguishes hard budget warnings from near-budget watchlist entries and
uses an explicit eval-report budget for the 30-task golden report.

### Verification Notes

QFIX-03 reruns Harness validation, AIDE Lite validation/test/selftest/eval,
commit checks, changelog preview/validate/status, pack export/status, and core
unit test suites. Final Harness and AIDE Lite validation report PASS with no
WARN/FAIL checks. Detailed results are recorded in
`.aide/queue/QFIX-03-warning-review-reconciliation/evidence/validation.md`.

### Regressions Avoided

- No Git history rewrite.
- No provider/model/network calls.
- No release publishing, tags, GitHub Releases, or GitHub API mutation.
- No target-repo mutation.

### Follow-Up

- Q35 has since been implemented as report-only advisory work; Q36 is the next AIDE-local phase.

## Work Item: Q34

### Status

Implemented, awaiting review.

### Scope

- `.aide/policies/changelog.yaml`
- `.aide/changelog/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q34_changelog_release.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q34-changelog-release-notes-generator-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/changelog-preview.md`

### Implementation Notes

Q34 turns Q27 structured commit bodies into deterministic preview artifacts:
`CHANGELOG.preview.md`, `RELEASE_NOTES.preview.md`, matching JSON files,
`malformed-commits.md`, and `latest-changelog-report.md`. The parser reads
Conventional Commit subjects, structured Markdown sections, changelog category
bullets, AIDE trailers, legacy semi-structured commits, merge commits, and
breaking-change markers. Malformed or legacy commits warn and remain visible;
history is not rewritten.

The command surface is preview-only: `changelog preview` writes drafts,
`changelog validate` checks policy/templates/output shape, and
`changelog status` summarizes the latest preview. No tags, GitHub Releases,
release publishing, branch mutation, provider/model calls, or network calls
are introduced.

### Verification Notes

- Q34 targeted tests cover subject parsing, structured section extraction,
  trailer parsing, category bullets, legacy/malformed commits, merge commits,
  fixture Git history preview generation, JSON shape, and preview-only text.
- Q34 golden tasks cover changelog preview, release-note preview, malformed
  commit reporting, and JSON preview shape.
- Final validation is recorded under Q34 evidence.

### Regressions Avoided

- No official `CHANGELOG.md` promotion, release publishing, tag creation,
  GitHub Release creation, branch mutation, provider/model call, network call,
  or history rewrite.
- Export pack support includes changelog policy/config/templates but excludes
  source-generated preview outputs as target truth.

### Follow-Up

- Q35 should add GitHub protection and CI advisory policy without applying
  GitHub settings or publishing releases.

## Work Item: Q31

### Status

Implemented, awaiting review.

### Scope

- `.aide/policies/export-import.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q31_export_pack_governance.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q31-export-pack-sync-git-commit-workflow/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/cross-repo-pack-export-import.md`

### Implementation Notes

Q31 makes the portable AIDE Lite Pack carry the generic governance introduced
by Q27 through Q30: structured commit policy, hook/template support,
changelog preview, task resumption, WorkUnit and recovery policy, branch role
policy, promotion/sync/prune policy, project workflow profiles, and dry-run
Git helper policy. The export boundary stays target-safe: AIDE queue history,
generated context and reports, AIDE-specific branch policy, workflow detection
outputs, latest helper plans, changelog previews, local state, secrets, raw
prompts, and raw responses remain excluded.

Safe import keeps hook installation opt-in. Imported target repos receive the
hook template under `.aide/hooks/commit-msg`, but `.git/hooks/` is not written.
Target repos must run their own `git detect`, `git plan`, snapshot, index, and
pack commands after import so target state is generated locally.

### Verification Notes

- Q31 targeted tests cover manifest inclusion, source-state exclusion, safe
  fixture import, hook non-installation, commit check pass/fail behavior, and
  imported Git policy/detect/plan commands.
- AIDE Lite Q31 golden tasks cover pack inclusion/exclusion and fixture import
  governance command behavior.
- Final validation is recorded under Q31 evidence.

### Regressions Avoided

- No Eureka, Dominium, external repo, GitHub, branch, provider, model, or
  network mutation.
- No exported AIDE-specific live branch detection or helper-plan state.
- No automatic hook installation in imported target repositories.

### Follow-Up

- Q32 should sync Eureka from the canonical Q31 pack and regenerate
  Eureka-local reports.
- Q33 should sync Dominium after Q32 evidence is available.

## Work Item: Q30

### Status

Implemented, awaiting review.

### Scope

- `.aide/git/aide-branch-policy.yaml`
- `.aide/git/aide-dev-main-plan.json`
- `.aide/git/aide-dev-main-plan.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q30_aide_dev_main_policy.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q30-aide-dev-main-policy-sync/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/aide-dev-main-workflow.md`

### Implementation Notes

Q30 records the AIDE repository's own branch policy on top of the generic Q28
roles and Q29 helpers. `main` is canonical accepted truth. `dev` is the intended
shareable integration branch and is explicitly not canonical release truth.
Bounded work lands to `dev`; `dev` promotes to `main` only through review,
validation, commit, changelog, pack, and secret-scan gates.

Current local evidence shows `main` exists locally and as `origin/main`, while
`dev` is absent locally and remotely. Q30 therefore generates a future explicit
operator plan for creating and pushing `dev`, but does not run those commands.

### Verification Notes

- Q30 targeted tests cover policy parsing, main/dev role validation, no-live-
  mutation posture, missing-dev planning, existing-dev classification,
  promotion-gate anchors, and Q30 golden tasks.
- AIDE Lite Git policy, detect, status, and plan commands now include the
  AIDE-specific branch policy and generated dev/main plan artifacts.
- Final validation is recorded under Q30 evidence.

### Regressions Avoided

- No live AIDE branch creation, deletion, merge, push, prune, or promotion.
- No GitHub API calls, CI activation, release publishing, provider/model calls,
  or outbound network behavior.
- AIDE-specific live branch detection artifacts are not exported as target repo
  truth.

### Follow-Up

- Q31 should export and synchronize the generic Git/commit workflow support
  without treating AIDE's live dev/main plan as target-repo truth.
- Q35 or later should add GitHub protection and CI advisory/application layers.

## Work Item: Q29

### Status

Implemented, awaiting review.

### Scope

- `.aide/git/helper-policy.yaml`
- `.aide/git/helper-commands.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q29_git_helper.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q29-merge-land-promote-helper-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/git-helper-workflow.md`

### Implementation Notes

Q29 adds dry-run-first Git helper plans for sync, land, promote, and prune
actions. Live AIDE branch mutation remains out of scope: Q29 does not create
`dev`, merge into `main`, push remotes, delete live branches, or run GitHub
mutation. The mutating paths are implemented behind explicit `--apply` and
tested only inside temporary Git fixture repositories with fixture-local Git
user/email configuration.

The helper safety model records repo root, current branch, dirty state,
local/remote branches, upstream status, branch roles, protected roles, policy
readiness, ancestor containment, ahead/behind state where available, and
unpushed protected branches where feasible. Unknown or dirty states block
land/promote mutation. Prune eligibility requires ancestor containment and
never includes canonical, integration, release, or deploy roles.

### Verification Notes

- Q29 targeted fixture tests cover task-to-dev land, dev-to-main promote,
  contained branch prune, unmerged prune refusal, protected branch refusal,
  dirty-tree blocks, unknown-role blocks, and no remote push execution.
- Q29 golden tasks cover helper policy anchors, land/promote plan docs, prune
  guards, and live-repo no-mutation defaults.
- Final validation is recorded under Q29 evidence.

### Regressions Avoided

- No live AIDE branch creation, deletion, merge, push, prune, or promotion.
- No force-push support.
- No GitHub API calls, CI activation, release publishing, provider/model calls,
  or outbound network behavior.

### Follow-Up

- Q30 should decide and apply the AIDE-specific `dev`/`main` policy posture if
  appropriate.
- Q35 or later should add GitHub protection and CI advisory/application layers.

## Work Item: Q28

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q28_git_workflow.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q28-git-workflow-policy-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/git-workflow-policy.md`
- `docs/reference/branch-roles.md`
- `docs/reference/promotion-policy.md`

### Rationale

Q28 makes branch state understandable before branch automation exists. It reduces
future prompt and review cost by giving agents a deterministic way to identify
`main` as canonical truth, `dev` as integration truth, task/review/release/hotfix
roles, and the policy gates that later helpers must enforce.

### Notable Design Decisions

- Detection is local and report-only; it does not fetch, merge, push, prune,
  delete, create branches, or call GitHub.
- `dev` is useful as shareable integration truth but is not canonical release
  truth.
- Unknown roles and dirty trees produce conservative recommendations.
- Pruning is policy-only and requires future ancestor-containment proof.

### Tradeoffs

- Local detection cannot prove GitHub branch protection or remote freshness.
- Full merge/land/promote behavior is deferred to Q29 so policy can be reviewed
  before mutation helpers exist.

### Verification

- Q28 targeted tests and golden tasks pass.
- Final validation is recorded under Q28 evidence.

### Regressions Avoided

- No live branch creation, deletion, merge, push, prune, fetch, or GitHub API
  mutation.
- No provider/model calls, network calls, CI creation, release publishing, or
  product runtime change.

### Remaining Issues

- Q29 must implement safe helper plans and fixture-only mutation tests.
- Q35 or later must handle GitHub branch protection and CI advisory/application.

## Work Item: Q27

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/commit-messages.yaml`
- `.aide/policies/task-resumption.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/recovery.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q27_commit_recovery.py`
- `.aide/evals/golden-tasks/**`
- `.aide/hooks/commit-msg`
- `.aide/git/commit-template.md`
- `.aide/changelog/**`
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/commit-discipline.md`
- `docs/reference/workunit-idempotency.md`
- `docs/reference/changelog-preview.md`

### Rationale

Q27 makes commits and queue tasks recoverable from repository state. It reduces
future token cost by allowing agents to validate commit bodies, preview
changelog entries, detect no-op duplicate tasks, and resume partial work without
replaying long prompt history.

### Notable Design Decisions

- Existing old commits are reported as malformed instead of rewritten.
- The commit hook is opt-in and installed only by explicit command.
- Task recovery is report-first; broad fixes still need queue authorization.
- Changelog preview is deterministic and non-publishing.

### Tradeoffs

- The changelog classifier is deliberately structural, not semantic.
- Task recovery detects queue/evidence state but does not perform product work.

### Verification

- Q27 targeted tests and golden tasks pass.
- Full final validation is recorded under Q27 evidence.

### Regressions Avoided

- No `.git/hooks` writes.
- No branch mutation, remote push, provider/model call, network call, CI, release publishing, or product runtime change.

### Remaining Issues

- CI enforcement and branch workflow policy are deferred to later Q28+ phases.
- Pre-Q27 history may remain malformed under the new checker.

## Work Item: P00

### Status

Completed

### Changed Paths

- `README.md`
- `AGENTS.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `governance/vision.md`
- `governance/support-policy.md`
- `governance/naming-policy.md`
- `governance/capability-levels.md`
- `governance/release-policy.md`

### Rationale

Replace the bootstrap placeholders with durable repository law for AIDE before any product features, host adapters, or scaffolding are introduced.

### Notable Design Decisions

- Defined AIDE as one project with one shared core and many host adapters.
- Centralized support posture in support tiers `T0` through `T5`.
- Centralized integration depth in capability levels `L0` through `L4`.
- Separated directory naming law from exact version coverage rules.
- Kept the phase release-gated so implementation work follows governance, inventory, and harness setup.

### Tradeoffs

- The documents favor durable policy over exhaustive examples.
- Future inventory and matrix details are referenced but intentionally not created in this prompt.

### Verification

- Verified file existence for all required deliverables:
  - `README.md`
  - `AGENTS.md`
  - `PLANS.md`
  - `IMPLEMENT.md`
  - `DOCUMENTATION.md`
  - `governance/vision.md`
  - `governance/support-policy.md`
  - `governance/naming-policy.md`
  - `governance/capability-levels.md`
  - `governance/release-policy.md`
- Ran `rg` checks across the deliverables for required conceptual anchors:
  - `AIDE`
  - `Automated Integrated Development Environment`
  - `one shared core`
  - `many host adapters`
  - `compatibility technology`
  - `version ranges`
  - `support tiers`
  - `capability levels`
  - `T0`
  - `T5`
  - `L0`
  - `L4`
- Verified the repository worktree shape with `git status --short`.

### Regressions Avoided

- No product code, adapter code, CI, packaging, or environment systems were introduced prematurely.
- No exact host version lists were embedded into source directory doctrine.
- No unsupported parity claims were added.

### Remaining Issues

None for P00. Product implementation, inventory, scaffolding, harness, environments, evals, and packaging remain intentionally deferred to later prompts.

## Work Item: P06

### Status

Completed

### Changed Paths

- `specs/README.md`
- `specs/architecture/**`
- `shared/README.md`
- `shared/core/README.md`
- `shared/protocol/README.md`
- `shared/transforms/README.md`
- `shared/diagnostics/README.md`
- `shared/config/README.md`
- `shared/schemas/**`
- `shared/cli/README.md`
- `shared/local-service/README.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had governance, inventory, matrices, host-lane scaffolds, and host-family research. It did not yet have the contract architecture that explains how one shared core and many host adapters should actually fit together. P06 fills that gap before implementation begins.

### Notable Design Decisions

- Defined AIDE as a transport-agnostic shared core with thin host adapters.
- Standardized three execution modes: `embedded`, `cli-bridge`, and `local-service`.
- Defined stable contract objects for host identity, host context, document context, workspace context, selection context, feature requests, settings, diagnostics, capability reports, and adapter responses.
- Explicitly separated shared logic from host UI, packaging, runtime glue, and host-only policy exceptions.
- Kept schemas conservative and descriptive rather than over-engineering them into full validation systems before implementation pressure exists.

### Tradeoffs

- The architecture is intentionally structural and leaves several implementation details open, including concrete protocol serialization, service lifecycle mechanics, and feature-manifest file placement.
- The schemas stabilize core shape now, but they do not attempt exhaustive validation of every future edge case.

### Verification

- Verified existence of required `specs/architecture/` files, shared subtree directories, shared subtree `README.md` files, and schema files.
- Ran `rg` checks for required architecture anchors including:
  - `one shared core`
  - `many host adapters`
  - `embedded`
  - `cli-bridge`
  - `local-service`
  - `feature`
  - `settings`
  - `diagnostic`
  - `capability`
  - `request`
  - `response`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P06 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, or packaging manifests were added.
- The architecture does not pretend that any shared-core or adapter implementation already exists.
- The docs reuse the existing governance, support, and capability model instead of redefining them.

### Remaining Issues

- Concrete serialization format details, service lifecycle details, and per-feature manifests remain for later implementation prompts.
- No runtime validation or eval integration exists yet because this prompt was architecture-only.

## Work Item: P07

### Status

Completed

### Changed Paths

- `inventory/legal-acquisition.yaml`
- `environments/**`
- `labs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already tracked host families, capabilities, architecture, and research, but it did not yet have a durable framework for the environment-preservation side of long-horizon IDE work. P07 adds that control plane without pretending that media, snapshots, or runnable environments already exist.

### Notable Design Decisions

- Separated platform knowledge from concrete environment tracking by keeping `platforms/` distinct from `environments/`.
- Defined stable concepts for environment families, environment instances, install media, toolchains, snapshots, bootability, blockers, and archival records.
- Added a machine-readable legal and acquisition vocabulary in `inventory/legal-acquisition.yaml` rather than scattering provenance rules across prose files.
- Kept labs separate from environments so partial experiments, blocked bring-up work, and archival captures can progress without polluting stable environment catalogs.
- Reused explicit state language such as `planned`, `acquired`, `installing`, `boots`, `usable`, `blocked`, and `archival-record` to keep partial progress honest.

### Tradeoffs

- The catalogs intentionally stop at conservative structural shapes and empty records instead of inventing a real corpus.
- The framework leaves room for later environment-specific fields once actual bring-up work creates pressure for them.

### Verification

- Verified existence of required environment docs, environment subdirectories, catalog files, playbooks, lab docs, lab subdirectories, lab registers, and `inventory/legal-acquisition.yaml`.
- Ran `rg` checks for required anchors including:
  - `environment`
  - `install media`
  - `toolchain`
  - `snapshot`
  - `bootability`
  - `blocked`
  - `archival`
  - `official-download`
  - `local-only`
  - `planned`
  - `usable`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P07 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, or packaging manifests were added.
- No proprietary binaries, installers, images, or toolchains were checked into Git.
- No acquisition, ownership, or bootability facts were fabricated.

### Remaining Issues

- No actual environment instances, media records, toolchain records, or snapshots were populated in this prompt.
- Detailed bring-up results, local asset references, and blocker records remain for later prompts once real environment work begins.

## Work Item: P08

### Status

Completed

### Changed Paths

- `evals/**`
- `packaging/**`
- `matrices/test-matrix.yaml`
- `matrices/packaging-matrix.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had governance, research, architecture, environment control-plane records, and seed matrices. It did not yet have a durable framework for evaluation, verification, packaging posture, or release-shape tracking. P08 fills that gap without implying that executable tests, package builds, or shipped artifacts already exist.

### Notable Design Decisions

- Defined a layered evaluation model that separates structural verification, schema checks, documentation consistency checks, smoke categories, packaging checks, release-shape checks, and archival-record checks.
- Added machine-readable eval catalogs for eval definitions, verification routines, graders, and result states without fabricating real coverage.
- Defined a packaging model that separates artifact class, manifest family, signing posture, release channel, and release records from source layout.
- Kept source directory naming law intact while allowing future artifact names to include exact host versions where concrete release records justify them.
- Refined `matrices/test-matrix.yaml` and `matrices/packaging-matrix.yaml` into planning frameworks tied to stable family and technology ids rather than leaving them as shallow placeholders.

### Tradeoffs

- The catalogs emphasize structural shape and vocabulary now rather than prematurely introducing executable graders, manifests, or release records.
- Packaging posture is intentionally conservative and uses `unknown`, `deferred`, `planning-only`, or `archival-oriented` states where exact release mechanics remain unresolved.
- The evaluation matrix records planned posture only; it does not try to mimic test execution before implementation exists.

### Verification

- Verified existence of required `evals/` docs, subdirectories, playbooks, catalogs, and README files.
- Verified existence of required `packaging/` docs, subdirectories, catalogs, checklists, and README files.
- Verified existence of required YAML catalogs and refined matrix files.
- Ran `rg` checks for required anchors including:
  - `existence`
  - `schema`
  - `load-smoke`
  - `editor-smoke`
  - `workspace-smoke`
  - `packaging-check`
  - `release`
  - `native-extension-package`
  - `companion-package`
  - `stable`
  - `hotfix`
  - `verification`
  - `grader`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P08 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, signed artifacts, or release binaries were added.
- No matrix entry claims passing eval coverage or real packaging implementation that does not exist.
- No repository naming law was redefined; source layout remains technology-based.

### Remaining Issues

- No executable graders, smoke tests, release automation, manifest implementations, or package outputs were added in this prompt.
- Real run records, release records, and stronger coverage depend on later implementation and environment work.

## Work Item: P09

### Status

Completed

### Changed Paths

- `specs/boot-slice/**`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had host research, capability posture, shared-core contracts, environment control-plane records, and eval scaffolding, but it still lacked one explicit first implementation target. P09 defines that target as a minimal cross-host boot slice and ties it to an honest oldest-first rollout plan.

### Notable Design Decisions

- Chose a two-part boot slice: universal `boot.slice.invoke` plus conditional `boot.slice.editor-marker`.
- Kept the first slice inside `L0` through `L2` and explicitly deferred `L3` and `L4`.
- Made the boot slice report-first and deterministic so every committed lane can participate without pretending to reach identical depth.
- Required `L2` editor proof only where the documented lane surface makes that the honest first proof, especially `xcodekit` and `vsix-v2-vssdk`.
- Applied oldest-first globally by lane phase and within families by exact version ids, while allowing companion fallback when a native or archival-native lane is blocked.

### Tradeoffs

- The rollout plan avoids a fake single-file chronological order across families whose archival dates are only partially reconstructed; it uses phase classes plus within-family version order instead.
- Some lanes with theoretical `L2` potential remain report-first or optional-marker lanes in the first wave to avoid making the entire rollout hostage to the hardest environment problems.
- The spec defines feature ids and behavior invariants now, but it intentionally stops short of adding new schemas or implementation stubs.

### Verification

- Verified existence of required `specs/boot-slice/` files, `boot-slice-manifest.yaml`, and `rollout-plan.yaml`.
- Ran `rg` checks for required anchors including:
  - `boot slice`
  - `host`
  - `lane`
  - `capability`
  - `fallback`
  - `blocked`
  - `oldest-first`
  - `verification`
- Verified that all committed lane paths appear in `specs/boot-slice/rollout-plan.yaml`.
- Verified that `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, and `evals/catalogs/verification-catalog.yaml` were updated.
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P09 allowlist.

### Regressions Avoided

- No implementation code, build scripts, CI, host-specific source files, or `.codex/` or `.agents/` content were added.
- The boot slice does not promise identical cross-host UX or universal `L2` depth.
- Blocked or degraded lanes are kept explicit rather than being erased from the rollout story.

### Remaining Issues

- No executable boot-slice implementation, run records, or passing eval results were added in this prompt.
- Exact environment blockers, packaging details, and lane-specific runtime glue remain for later implementation and lab prompts.

## Work Item: P10

### Status

Completed

### Changed Paths

- `shared/**`
- `fixtures/**`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository had a defined shared-core contract and a concrete first boot-slice specification, but it still lacked any executable shared runtime. P10 turns that specification into a small deterministic implementation that later host adapters can call through an embedded path or a CLI bridge without forcing host-specific logic into the shared core.

### Notable Design Decisions

- Chose a pure Python 3 standard-library bootstrap runtime for this phase because it is sufficient for a deterministic shared-core proof and avoids unnecessary dependency or toolchain expansion.
- Implemented only the two boot-slice feature ids already defined by the spec: `boot.slice.invoke` and `boot.slice.editor-marker`.
- Kept lane-specific acceptance posture in a small static policy map under `shared/config/boot_slice.py` so the runtime can report honest fallback, optional, or required editor behavior without introducing host adapter code.
- Represented request envelopes, response envelopes, capability reports, and diagnostics as JSON-friendly dataclass-backed structures aligned to the existing shared schemas.
- Implemented a minimal `python -m shared.cli` bridge that accepts JSON from a file or stdin and emits deterministic JSON on stdout for later `cli-bridge` host work.
- Used committed JSON fixtures and standard-library `unittest` coverage as the first executable eval layer for the shared-core slice.

### Tradeoffs

- The runtime implements the boot-slice editor marker as a preview-only deterministic edit record rather than a general edit engine.
- Lane policy is static and conservative for this bootstrap phase; it reflects the current boot-slice acceptance table rather than a future dynamic registry.
- The shared core accepts the documented execution-mode values, but it does not implement a local-service daemon or any host integration lifecycle in P10.

### Verification

- Verified existence of shared-core implementation files under `shared/core/`, `shared/protocol/`, `shared/diagnostics/`, `shared/config/`, `shared/cli/`, and `shared/tests/`.
- Verified existence of deterministic request and response fixtures under `fixtures/boot-slice/`.
- Ran `py -3 -m unittest discover -s shared/tests -t .` and confirmed all tests passed.
- Ran `py -3 -m shared.cli --request fixtures\\boot-slice\\success-request.json --pretty` and confirmed the CLI smoke case passed with deterministic JSON output.
- Verified that `evals/catalogs/eval-catalog.yaml` and `evals/catalogs/verification-catalog.yaml` were updated for the shared-core slice.
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P10 allowlist.

### Regressions Avoided

- No `hosts/**` code, CI workflows, `.codex/` content, `.agents/` content, packaging automation, or external dependencies were added.
- No host-adapter success claims were made; the runtime reports shared-core capability only and keeps lane availability or fallback reasons explicit.
- No non-deterministic behavior, network calls, time-dependent behavior, or machine-local data was introduced into the fixtures or tests.

### Remaining Issues

- No host adapters call this runtime yet, so host-lane success remains deferred to later prompts.
- No local-service daemon, packaging flow, or broader feature set beyond the first boot slice was implemented.
- L3 and L4 behaviors, workspace awareness, and deeper IDE integration remain deferred by design.

## Work Item: P11

### Status

Completed

### Changed Paths

- `hosts/microsoft/**`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core and the host-agnostic CLI bridge, but no Microsoft host lane yet had a concrete first-wave proof. P11 turns the Microsoft rollout slice into explicit lane-local evidence while keeping business behavior in the shared core and staying honest about native archival or SDK blockers.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for the first runnable Microsoft proofs instead of duplicating boot-slice behavior inside host lanes.
- Implemented lane-local `run_boot_slice.py` shims only where a thin `cli-bridge` proof is the accepted minimum and can run honestly in the current repository environment.
- Chose runnable degraded `L1` proofs for `com-addin`, `vsix-v1`, `extensibility`, and `visual-studio-mac/companion`.
- Chose explicit blocked structural proofs for `vsix-v2-vssdk` and `visual-studio-mac/monodevelop-addin` because those lanes require native or archival-native evidence that cannot be reproduced honestly here.
- Kept execution-mode choices conservative: `cli-bridge` for the runnable lanes, retained `embedded` as the intended target for `vsix-v2-vssdk`, and left `local-service` deferred for the modern extensibility lane.

### Tradeoffs

- The first Microsoft wave favors report-first or companion fallback evidence over premature native project scaffolding for lanes whose true toolchains are unavailable.
- `vsix-v2-vssdk` remains the Windows native reference target, but P11 stops at a blocked-proof record rather than inventing a fake native shell-hosted test.
- Visual Studio for Mac companion proof moves the family forward, but the native MonoDevelop-derived lane remains archival and blocked until preserved macOS assets exist.

### Verification

- Verified required Microsoft lane proof files and updated lane READMEs exist under `hosts/microsoft/**`.
- Ran `py -3 -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran lane-local runnable smoke checks:
  - `py -3 hosts\\microsoft\\visual-studio\\com-addin\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio\\vsix-v1\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio\\extensibility\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio-mac\\companion\\run_boot_slice.py --verify --pretty`
- Verified blocked structural evidence for non-runnable lanes through their committed request and blocked-proof records:
  - `hosts/microsoft/visual-studio/vsix-v2-vssdk/boot_slice_request.json`
  - `hosts/microsoft/visual-studio/vsix-v2-vssdk/blocked-proof.md`
  - `hosts/microsoft/visual-studio-mac/monodevelop-addin/boot_slice_request.json`
  - `hosts/microsoft/visual-studio-mac/monodevelop-addin/blocked-proof.md`
- Verified that Microsoft matrix rows, eval catalogs, and the Microsoft run record were updated.
- Verified that changed paths stayed inside the P11 allowlist and excluded an unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Apple or CodeWarrior host code was added.
- No shared-core business logic was duplicated or broadened beyond the P10 boot slice.
- No fake native build or runtime success was claimed for historical or SDK-bound lanes that were only structurally represented.
- No `.codex/`, `.agents/`, CI, or packaging automation content was introduced.

### Remaining Issues

- `vsix-v2-vssdk` still needs a real VSSDK-capable Visual Studio environment before an honest embedded `L2` editor-marker proof can be claimed.
- `extensibility` remains on a conservative `cli-bridge` proof; the documented local-service or richer out-of-process path is deferred.
- `visual-studio-mac/monodevelop-addin` remains blocked pending preserved macOS assets and a reproducible retired-host environment.
- Apple and CodeWarrior host implementations remain deferred to later prompts.

## Work Item: P12

### Status

Completed

### Changed Paths

- `hosts/apple/**`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core, and P11 established the first Microsoft host-lane wave, but Apple still had no concrete first-wave host proof. P12 turns the Apple rollout slice into explicit lane-local evidence while keeping shared behavior in the shared core and staying honest about native XcodeKit blockers outside a macOS or Xcode environment.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for the first runnable Apple proof instead of duplicating boot-slice behavior inside Apple lanes.
- Implemented a thin `run_boot_slice.py` wrapper only for `hosts/apple/xcode/companion`, because that is the accepted runnable first proof in the current repository environment.
- Chose an explicit blocked structural proof for `hosts/apple/xcode/xcodekit` because the lane requires an embedded `L2` editor-marker proof that cannot be reproduced honestly without macOS or Xcode tooling.
- Added native-adjacent `extension-target.yaml` metadata for `xcodekit` to keep the Xcode Source Editor target shape visible without pretending it is build-verified.
- Kept execution-mode choices conservative: `cli-bridge` for the runnable companion lane and `embedded` as the intended but blocked target for `xcodekit`.

### Tradeoffs

- The Apple wave favors a runnable fallback proof plus a blocked native record instead of inventing a fake source-editor extension load outside macOS.
- `xcodekit` stays the Apple-native reference target, but P12 stops at blocked structural evidence rather than inventing a containing app, signing flow, or extension run that cannot be verified here.
- The companion lane moves older or broader Xcode workflows forward, but deeper project-aware behavior remains deferred.

### Verification

- Verified required Apple lane proof files and updated lane READMEs exist under `hosts/apple/**`.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran the runnable Apple smoke check:
  - `py -3 hosts\\apple\\xcode\\companion\\run_boot_slice.py --verify --pretty`
- Verified blocked structural evidence for the non-runnable native lane through its committed request, target metadata, and blocked-proof records:
  - `hosts/apple/xcode/xcodekit/boot_slice_request.json`
  - `hosts/apple/xcode/xcodekit/extension-target.yaml`
  - `hosts/apple/xcode/xcodekit/blocked-proof.md`
- Verified that Apple matrix rows, eval catalogs, and the Apple run record were updated.
- Verified that changed paths stayed inside the P12 allowlist and excluded the unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Microsoft or CodeWarrior host code was added.
- No shared-core business logic was duplicated or broadened beyond the P10 boot slice.
- No fake native Xcode build, package, or runtime success was claimed for the blocked `xcodekit` lane.
- No `.codex/`, `.agents/`, CI, or packaging automation content was introduced.

### Remaining Issues

- `xcodekit` still needs a real macOS or Xcode environment plus a verified containing-app or extension packaging path before an honest embedded `L2` editor-marker proof can be claimed.
- The current shared-core bootstrap exposes the CLI bridge only; a verified embedded Swift or XcodeKit interop surface remains a later blocker rather than P12 scope.
- The Apple companion lane remains at an `L1` runnable fallback proof; broader project-aware workflows and native editor parity remain deferred.
- CodeWarrior host implementations remain deferred to later prompts.

## Work Item: P13

### Status

Completed

### Changed Paths

- `hosts/metrowerks/**`
- `inventory/legacy-ide-families.yaml`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core, P11 and P12 established the Microsoft and Apple host waves, but the committed legacy host family still had only research placeholders. P13 turns the CodeWarrior lanes into explicit boot-slice proofs and uses that implementation experience to tighten the broader legacy candidate backlog without promoting new families prematurely.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for both committed CodeWarrior lanes instead of inventing legacy-specific business logic.
- Implemented a runnable archival-native `cli-bridge` proof for `hosts/metrowerks/codewarrior/ide-sdk` because the boot-slice acceptance for that lane is report-first `L1` with optional editor proof, and the shared lane map already supports that shape.
- Added `plugin-target.yaml` for `ide-sdk` so the native SDK or COM entry surface stays visible even though in-host loading remains unverified.
- Implemented a runnable fallback `cli-bridge` proof for `hosts/metrowerks/codewarrior/companion` to cover unresolved or non-native archival workflows outside the native lane.
- Stabilized `inventory/legacy-ide-families.yaml` by adding concise post-CodeWarrior next-action guidance instead of redesigning the backlog structure or promoting new host families.

### Tradeoffs

- The `ide-sdk` proof is intentionally report-first and stops at `L1`; it does not claim native IDE SDK loading, COM automation wiring, or the optional editor-marker path.
- The companion proof is runnable, but it does not replace the archival-native lane and does not imply project-aware behavior.
- Backlog stabilization stays conservative: it sharpens near-term versus difficult candidates through notes and next actions rather than inventing a new prioritization system.

### Verification

- Verified required CodeWarrior lane proof files and updated lane READMEs exist under `hosts/metrowerks/**`.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran the runnable legacy smoke checks:
  - `py -3 hosts\\metrowerks\\codewarrior\\ide-sdk\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\metrowerks\\codewarrior\\companion\\run_boot_slice.py --verify --pretty`
- Verified structural native-adjacent evidence for `ide-sdk` through `hosts/metrowerks/codewarrior/ide-sdk/plugin-target.yaml`.
- Verified that `inventory/legacy-ide-families.yaml`, legacy matrix rows, eval catalogs, and the CodeWarrior run record were updated.
- Verified that changed paths stayed inside the P13 allowlist and excluded the unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Microsoft or Apple host code was added.
- No shared-core logic was broadened or duplicated inside CodeWarrior lanes.
- No fake native CodeWarrior build, package, or in-host runtime success was claimed for the archival-native lane.
- No new committed legacy host families, `.codex/`, `.agents/`, CI, or packaging automation content were introduced.

### Remaining Issues

- `ide-sdk` still needs a reproducible historical environment before an honest in-host IDE SDK or COM automation proof can be claimed.
- The optional `boot.slice.editor-marker` proof for `ide-sdk` remains deferred until active-document capture is available from a real legacy environment.
- Later Eclipse-era CodeWarrior contract boundaries remain unresolved under the current `ide-sdk` umbrella.
- The broader legacy candidate backlog is still research-driven; P13 stabilizes it but does not promote any new family into `hosts/`.

## Work Item: P14

### Status

Completed

### Changed Paths

- `README.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `MAINTENANCE.md`
- `CHANGELOG.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `scripts/**`
- `.agents/README.md`
- `.agents/skills/**`
- `evals/reports/**`

### Rationale

The repository had completed its first planning, research, framework, and initial implementation waves, but the top-level docs still presented an earlier bootstrap picture and there was no dedicated maintenance baseline for future iterative work. P14 consolidates that state into a clearer contributor surface, a phase-based roadmap, reusable maintenance assets, repo-local maintenance skills, and a factual post-P13 audit.

### Notable Design Decisions

- Rewrote `README.md` to reflect post-P13 implementation reality rather than the earlier governance-only bootstrap state.
- Added `CONTRIBUTING.md`, `ROADMAP.md`, `MAINTENANCE.md`, and `CHANGELOG.md` as low-noise root control-plane docs rather than scattering contributor and maintenance guidance across multiple unrelated files.
- Kept maintenance automation at the control-plane level by creating task catalogs and checklists under `scripts/maintenance/` instead of adding CI or heavy executable automation.
- Added narrow repo-local skills for maintenance, docs normalization, roadmap work, and repo audits, following the existing `.agents/skills/` style.
- Added audit-style reports under `evals/reports/` so the completed bootstrap and first implementation wave has a concise factual rollup.

### Tradeoffs

- The new maintenance assets are intentionally procedural and mostly manual; they improve coherence now without pretending that automation maturity already exists.
- The roadmap stays phase-based and avoids dates, which is less specific than a schedule but more honest for the current repo state.
- The changelog is only a baseline template; it does not backfill earlier phases because that history already lives in `PLANS.md` and `IMPLEMENT.md`.

### Verification

- Verified existence of required root docs:
  - `CONTRIBUTING.md`
  - `ROADMAP.md`
  - `MAINTENANCE.md`
  - `CHANGELOG.md`
- Verified existence of required `scripts/maintenance/` files.
- Verified existence of required maintenance skill directories and `SKILL.md` files under `.agents/skills/`.
- Verified existence of `evals/reports/bootstrap-phase-audit.md`.
- Ran anchor scans for:
  - `roadmap`
  - `maintenance`
  - `blocked`
  - `deferred`
  - `candidate`
  - `committed`
  - `automation`
  - `audit`
  - `contributing`
  - `changelog`
- Ran `rg '^name:|^description:'` across the new maintenance-oriented skill files.
- Verified that `README.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P14 allowlist.

### Regressions Avoided

- No product code, boot-slice expansion, new host adapters, CI workflows, or `.codex/` content were added.
- No roadmap dates or fabricated support claims were introduced.
- Blocked, deferred, candidate, and committed distinctions remain explicit.

### Remaining Issues

- Maintenance automation remains mostly manual and checklist-driven; later scripting or CI candidates are documented but not implemented here.
- The repository still carries major technical blockers in native host environments, packaging maturity, and broader release evidence; P14 documents them rather than resolving them.

## Work Item: P15

### Status

Completed

### Changed Paths

- `.aide/**`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `.agents/README.md`
- `.agents/skills/README.md`
- `scripts/aide-queue-next`
- `scripts/aide-queue-status`
- `scripts/aide-queue-run`
- `scripts/README.md`
- `docs/reference/self-bootstrap.md`
- `AGENTS.md`
- `README.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository needed a minimal self-hosting control plane so future agent work can be resumed from filesystem state instead of relying on chat history or extension task queues. P15 creates that queue scaffold while preserving existing bootstrap-era phase records and implementation evidence.

### Notable Design Decisions

- Made `.aide/queue/` the canonical source of truth for non-trivial self-hosting work.
- Defined Q00 as a future baseline freeze and reboot audit rather than completing that audit in the bootstrap scaffold.
- Kept Q01 through Q04 as listed, pending queue items without task folders or implementation.
- Added autonomy, bypass, and review-gate policies as small YAML records rather than a full policy engine.
- Added queue scripts as read-only Python standard-library helpers with conservative line-oriented parsing.

### Tradeoffs

- The queue parser supports only the simple bootstrap `index.yaml` shape and is not a general YAML implementation.
- The runner script prints the next prompt but deliberately does not invoke Codex or any worker.
- The scaffold records the reboot focus on Contract, Harness, Compatibility, and Dominium Bridge without claiming that stack is implemented.

### Verification

- Verified required scaffold files exist.
- Ran Python syntax checks for `scripts/aide-queue-next`, `scripts/aide-queue-status`, and `scripts/aide-queue-run`.
- Ran `py -3 scripts/aide-queue-status`.
- Ran `py -3 scripts/aide-queue-next`.
- Ran `py -3 scripts/aide-queue-run`.
- Ran anchor scans for canonical queue, bypass, review-gate, ExecPlan, and Q00 language.
- Verified changed paths stayed inside the P15 allowlist.

### Regressions Avoided

- No product runtime, broker, service, host adapter, IDE extension, Commander, Mobile, app surface, provider integration, release action, tag, or package automation was added.
- No source code was moved.
- No forbidden implementation, governance, inventory, matrix, environment, lab, research, packaging, eval, fixture, shared, host, or spec paths were modified.
- Q01 through Q04 were not implemented.

### Remaining Issues

- Q00 still needs to be processed by a future worker and reviewed.
- Q01 through Q04 are queue placeholders only.
- Queue scripts are intentionally limited readers, not a full validator or autonomous runner.

## Work Item: Q00-bootstrap-audit

### Status

Needs Review

### Changed Paths

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/constitution/bootstrap-era-aide.md`
- `docs/charters/reboot-charter.md`
- `docs/reference/repo-census.md`
- `docs/roadmap/reboot-roadmap.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q00-bootstrap-audit/**`

### Rationale

Q00 freezes the current repository baseline for the in-place AIDE reboot. It records what bootstrap-era AIDE achieved, distinguishes implemented reality from future intent, and makes the Q01 through Q08 queue path visible without implementing later work.

### Notable Design Decisions

- Treated P00 through P15 as historical baseline rather than material to rewrite.
- Defined the reboot public model as AIDE Core, AIDE Hosts, and AIDE Bridges.
- Defined the internal Core split as Contract, Harness, Runtime, Compatibility, Control, and SDK.
- Recorded the first shipped stack as Contract + Harness + Compatibility + Dominium Bridge without claiming it is implemented.
- Expanded queue visibility through Q08 while creating no Q01 or later task folders.
- Kept Q00 review-gated and targeted for `needs_review` rather than self-approving it.

### Tradeoffs

- The repo census is a documentation map only; no source files were moved.
- The reboot roadmap is queue-oriented and does not add dates or release promises.
- Q00 evidence is structural and documentation-focused; it does not re-run heavy host or native tests.

### Verification

- Verified required Q00 deliverable files exist.
- Ran `py -3 scripts/aide-queue-status`; Q00 reported `needs_review`, and Q01 through Q08 were visible as planned pending items.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q01-documentation-split`.
- Ran corrected anchor scans for `AIDE Core`, `AIDE Hosts`, `AIDE Bridges`, `Contract`, `Harness`, `Compatibility`, `Dominium Bridge`, `bootstrap-era`, and `pre-product`; all were found.
- Ran `py -3 -m py_compile scripts/aide-queue-next scripts/aide-queue-status scripts/aide-queue-run`; syntax check passed and generated bytecode was removed.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; it passed with all changed paths inside the Q00 allowlist.
- Recorded validation details in `.aide/queue/Q00-bootstrap-audit/evidence/validation.md`.

### Regressions Avoided

- No bootstrap-era phase history was deleted or rewritten.
- No forbidden paths were modified.
- No Runtime, Commander, Mobile, IDE extension, app surface, provider integration, package, release, or autonomous worker implementation was added.
- Q01 through Q08 were not implemented.

### Remaining Issues

- Q00 requires review before being treated as accepted.
- Q01 through Q08 remain planned queue items.
- Runtime, CLI or Service surfaces, Commander, Mobile, IDE Hosts, packaging automation, and release work remain deferred.

## Work Item: Q01-documentation-split

### Status

Needs Review

### Changed Paths

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/constitution/**`
- `docs/charters/**`
- `docs/roadmap/**`
- `docs/design-mining/**`
- `docs/decisions/**`
- `docs/reference/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q01-documentation-split/**`

### Rationale

Q01 makes the reboot documentation surface navigable before structural skeleton, contract, harness, compatibility, or bridge work begins. It preserves bootstrap-era records and maps them into durable document families instead of moving files.

### Notable Design Decisions

- Documented the public model as AIDE Core, AIDE Hosts, and AIDE Bridges.
- Documented the internal Core split as Contract, Harness, Runtime, Compatibility, Control, and SDK.
- Kept Runtime, SDK, IDE Hosts, Commander, Mobile, provider adapters, app surfaces, and automation as deferred or planned work.
- Created ADR-like decision records for the core reboot choices.
- Treated design-mining as future reference input, not doctrine.
- Stopped Q01 at `needs_review` because queue policy and Q00's status require review-gated continuation.

### Tradeoffs

- Q01 adds concise indexes and charters rather than a large final architecture rewrite.
- Documentation migration is a map and link strategy, not a file move.
- Command and generated-artifact references are intentionally minimal because Q03 through Q05 have not run.

### Verification

- Verified required Q01 documentation directories exist.
- Verified required charter files exist.
- Verified required decision records exist.
- Verified `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md` contain Q01 documentation pointers.
- Ran `py -3 scripts/aide-queue-status`; Q00 and Q01 reported `needs_review`, and Q02 through Q08 remained pending.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q02-structural-skeleton`.
- Ran terminology scans for AIDE Core, AIDE Hosts, AIDE Bridges, Contract, Harness, Runtime, Compatibility, Control, SDK, Dominium Bridge, XStack, bootstrap-era, and pre-product.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; all changed paths stayed inside the Q01 allowlist.
- Recorded detailed validation in `.aide/queue/Q01-documentation-split/evidence/validation.md`.

### Regressions Avoided

- No source code, host lane, shared runtime, provider adapter, IDE extension, app surface, packaging, release, or heavy test work was added.
- No bootstrap-era phase history, research, eval, packaging, environment, governance, inventory, matrix, or host records were deleted or moved.
- No Q02 or later queue item was implemented.

### Remaining Issues

- Q01 requires review before being treated as accepted.
- Q00 is still `needs_review`, so Q01 records explicit follow-on authorization rather than assuming Q00 has passed.
- Q02 structural skeleton remains the next planned queue item and must be separately planned before implementation.

## Work Item: Q02-structural-skeleton

### Status

Needs Review

### Changed Paths

- `core/**`
- `hosts/README.md`
- `hosts/cli/**`
- `hosts/service/**`
- `hosts/commander/**`
- `hosts/extensions/**`
- `bridges/**`
- `docs/reference/structural-migration-map.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q02-structural-skeleton/**`

### Rationale

Q02 introduces the target structural skeleton for the in-place reboot while preserving the bootstrap-era implementation layout. It creates README-only homes for AIDE Core, AIDE Hosts, and AIDE Bridges and records how existing directories map to the future conceptual structure.

### Notable Design Decisions

- Created `core/**` as skeleton documentation only; no package files, imports, runtime logic, or migrated shared-core code were added.
- Added host-category skeletons under `hosts/cli/`, `hosts/service/`, `hosts/commander/`, and `hosts/extensions/` while preserving existing host proof lanes.
- Added `bridges/**` and Dominium Bridge placeholders without implementing bridge behavior.
- Added `docs/reference/structural-migration-map.md` to distinguish conceptual homes from current physical locations and move status.
- Kept XStack Dominium-local and did not broaden it into generic AIDE doctrine.

### Tradeoffs

- Q02 creates empty structural homes with README boundaries instead of moving current working code.
- Existing `shared/**` remains the executable bootstrap-era shared-core location until a later reviewed migration exists.
- Existing `scripts/**` and `shared/cli/**` remain in place even though they conceptually map toward future Harness and CLI host surfaces.

### Verification

- Verified required Q02 skeleton directories exist.
- Verified every required skeleton README exists.
- Verified `docs/reference/structural-migration-map.md` exists.
- Verified `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md` contain Q02 structural pointers.
- Ran `py -3 scripts/aide-queue-status`; Q00, Q01, and Q02 reported `needs_review`, and Q03 remained pending.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q03-profile-contract-v0`.
- Ran terminology scans for AIDE Core, AIDE Hosts, AIDE Bridges, Contract, Harness, Runtime, Compatibility, Control, SDK, Dominium Bridge, XStack, skeleton, and future move.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .`; all 5 tests passed.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; all changed paths stayed inside the Q02 allowlist.
- Recorded detailed validation in `.aide/queue/Q02-structural-skeleton/evidence/validation.md`.

### Regressions Avoided

- No existing source files, host proof files, tests, imports, scripts, evals, packaging records, governance records, inventory records, matrices, research, environments, or labs were moved or edited.
- No Q03 or later queue item was implemented.
- No Runtime, Service, Commander, Mobile, IDE extension implementation, provider adapter, app surface, generated artifact system, or autonomous service logic was added.

### Remaining Issues

- Q02 requires review before being treated as accepted.
- Q00 and Q01 remain `needs_review`; Q02 proceeded only because the current prompt explicitly authorized implementation.
- Q03 profile contract v0 remains the next planned queue item.

## Work Item: Q03-profile-contract-v0

### Status

Needs Review

### Changed Paths

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/**`
- `.aide/commands/**`
- `.aide/policies/ownership.yaml`
- `.aide/policies/generated-artifacts.yaml`
- `.aide/policies/compatibility.yaml`
- `.aide/policies/validation-severity.yaml`
- `.aide/tasks/**`
- `.aide/evals/**`
- `.aide/adapters/**`
- `.aide/compat/**`
- `core/contract/**`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`
- `AGENTS.md`
- `.agents/skills/aide-queue/SKILL.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q03-profile-contract-v0/**`

### Rationale

Q03 makes AIDE self-describing through a minimal declarative Profile/Contract v0. It records repo identity, lifecycle status, source-of-truth rules, component declarations, command posture, policies, task and eval declarations, adapter metadata, compatibility placeholders, and documented v0 shapes without implementing Harness behavior.

### Notable Design Decisions

- Kept Profile declarative and left executable Harness commands to Q04.
- Refined the existing P15 `.aide/profile.yaml` and `.aide/toolchain.lock` rather than treating them as absent.
- Used compact YAML catalogs under `.aide/` and Markdown shape docs under `core/contract/shapes/**`.
- Preserved existing autonomy, bypass, and review-gate policies without loosening them.
- Marked generated downstream artifacts as non-canonical outputs deferred to Q05.

### Tradeoffs

- Q03 uses documented YAML shapes rather than full JSON Schema or an executable validator because Python's standard library has no YAML or JSON Schema parser.
- Component ownership is conceptual and does not move bootstrap-era source files.
- Adapter records are metadata-only so the Profile does not overfit to any provider or host.

### Verification

- Verified required Q03 files and directories exist.
- Verified required component ids are declared.
- Verified command catalog distinguishes implemented queue scripts from planned Harness commands.
- Verified existing review gates were not loosened.
- Ran queue helper scripts.
- Ran terminology and source-of-truth scans.
- Ran lightweight YAML/Markdown sanity checks.
- Ran `git diff --check`.
- Ran an allowed-path audit.
- Recorded detailed validation in `.aide/queue/Q03-profile-contract-v0/evidence/validation.md`.

### Regressions Avoided

- No Q04 Harness commands were implemented.
- No generated downstream target artifacts were created.
- No source code was moved or refactored.
- No Runtime, Host, Commander, Mobile, IDE extension, provider adapter, app surface, package automation, release action, or autonomous service logic was added.
- No existing host proof, shared implementation, governance, inventory, matrix, research, environment, lab, eval, or packaging paths were modified.

### Remaining Issues

- Q03 requires review before being treated as accepted.
- Q00, Q01, and Q02 remain `needs_review`; Q03 proceeded only because the current prompt explicitly authorized implementation.
- Harness v0 remains Q04, generated artifacts remain Q05, compatibility baseline remains Q06, and Dominium Bridge baseline remains Q07.

## Work Item: Q04-harness-v0

### Status

Passed With Notes

### Changed Paths

- `scripts/aide`
- `core/harness/**`
- `docs/reference/harness-v0.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q04-harness-v0/**`

### Rationale

Q04 implements the smallest executable Harness v0 over the Q03 declarative Profile/Contract. The Harness gives the repo a local command surface for structural validation, doctoring, compile-plan reporting, no-op migration posture, and bakeoff metadata readiness without implementing generated artifacts, Runtime, Hosts, providers, or service logic.

### Notable Design Decisions

- Used Python standard library only.
- Kept validation structural and text-based rather than claiming full YAML or schema validation.
- Kept `scripts/aide` as a thin repo-root wrapper and placed Harness logic under `core/harness/**`.
- Made `aide compile` report a deterministic plan only; generated artifacts remain Q05.
- Made `aide migrate` a no-op baseline report; compatibility baseline remains Q06.
- Made `aide bakeoff` metadata-only with no model, provider, native host, network, or external tool calls.
- Did not mutate final `.aide/` contract catalogs because this prompt allowed only Q04 queue/status/evidence changes under `.aide/`.

### Verification

- Ran Harness command smoke checks for `--help`, `init --dry-run`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.
- Ran lightweight Harness unittest smoke checks.
- Ran queue helper scripts.
- Checked generated target artifacts remained absent.
- Ran terminology searches.
- Ran `git diff --check`.
- Ran an allowed-path audit.
- Recorded detailed results in `.aide/queue/Q04-harness-v0/evidence/validation.md` and command output in `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`.

### Regressions Avoided

- No Q05 generated artifacts were created.
- No `CLAUDE.md`, `.claude/**`, generated `.agents/skills/**` targets, provider targets, or generated downstream files were added.
- No Runtime, Service, Host, Commander, Mobile, IDE extension, provider, app, release, or autonomous worker implementation was added.
- No bootstrap-era source files, host proofs, governance, inventory, matrices, research, specs, environments, labs, evals, or packaging records were moved or edited.

### Remaining Issues

- Q04 review accepted Harness v0 with notes, so Q05 planning may proceed.
- Q05 implementation proceeded only after its own plan, generated-artifact source-of-truth rules, validation evidence requirements, and review gate were created.
- Q00 through Q03 remain `needs_review`; Q04 relied on explicit human authorization plus the foundation and full audit findings.
- `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` were refreshed by Q05 under its bounded pre-generation scope.
- Full YAML/schema validation remains deferred.

## Work Item: Q05-generated-artifacts-v0

### Status

Needs Review

### Changed Paths

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/generated/**`
- `AGENTS.md`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `core/harness/**`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/reference/harness-v0.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q05-generated-artifacts-v0/**`

### Rationale

Q05 gives the self-hosting repo a deterministic generated-artifact boundary for agent-facing guidance while preserving `.aide/` as the canonical Profile/Contract and `.aide/queue/` as the canonical long-running work queue.

### Notable Design Decisions

- Refreshed stale Q03-era Harness wording before generation because those records are source inputs.
- Kept `AGENTS.md` and the three existing AIDE skills as managed-section targets rather than full-file generated outputs.
- Generated Claude guidance only as `.aide/generated/preview/CLAUDE.md`; final root `CLAUDE.md` and final `.claude/**` remain deferred.
- Added `.aide/generated/manifest.yaml` with deterministic source and content fingerprints and no timestamps.
- Extended `aide compile` with `--dry-run`, `--preview`, and `--write`.
- Extended `aide validate` with generated marker, manifest, stale-source, and manual-edit checks while keeping validation structural and standard-library only.

### Tradeoffs

- Q05 v0 uses a small line-oriented manifest reader rather than full YAML parsing.
- Source-fingerprint drift is a warning/review-required condition in v0; marker/body mismatch is a hard error.
- Generated skill content is intentionally concise and does not create new broad skill families.

### Verification

- Ran pre-generation Harness validation, doctor, and compile checks.
- Ran `py -3 scripts/aide compile --dry-run`.
- Ran `py -3 scripts/aide compile --preview`.
- Ran `py -3 scripts/aide compile --write`.
- Ran post-generation Harness validation and command smoke checks.
- Ran lightweight Harness tests and Python syntax checks.
- Ran queue helper checks.
- Checked generated markers, manifest, and final Claude target absence.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`.

### Regressions Avoided

- No final root `CLAUDE.md` or final `.claude/**` target was created.
- No generated artifact was made canonical truth.
- No Q06 Compatibility baseline, Q07 Dominium Bridge, Runtime, Host, Commander, Mobile, IDE extension, provider adapter, browser bridge, app surface, release automation, or autonomous service implementation was added.
- No forbidden bootstrap-era implementation, host proof, governance, inventory, matrix, research, spec, environment, lab, eval, or packaging path was modified.

### Remaining Issues

- Q05 requires review before generated artifact v0 is accepted.
- Q00 through Q03 remain `needs_review`.
- Full YAML/schema validation and the Compatibility baseline remain Q06 or later.
- Final Claude targets and broader generated skill families remain deferred pending review feedback.

## Work Item: Q06-compatibility-baseline

### Status

Needs Review

### Changed Paths

- `.aide/compat/**`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/generated/manifest.yaml`
- `core/compat/**`
- `core/harness/commands.py`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q06-compatibility-baseline/**`

### Rationale

Q06 gives the self-hosting repo a first Compatibility baseline for evolution of AIDE contract, queue, Harness, generated-artifact, and compatibility metadata. The baseline is versioned and enforceable enough for future queue work, while remaining conservative and non-mutating.

### Notable Design Decisions

- Used AIDE string identifiers such as `aide.profile.v0` and `aide.compat-baseline.v0` instead of semver or dated versions.
- Added `.aide/compat/schema-versions.yaml` as the Q06 registry while preserving the older `.aide/compat/schema-version.yaml` for existing v0 readers.
- Added one no-op migration registry entry: `baseline-current-noop`.
- Defined replay as deterministic Harness summary expectations, not Runtime replay.
- Added upgrade gates that treat unknown future versions as errors and require review for schema or generated-artifact contract changes.
- Added deprecation record format with no active deprecations.
- Extended `aide validate` and `aide migrate` with structural compatibility checks only.

### Tradeoffs

- Q06 still does not parse full YAML or enforce JSON Schema.
- `aide migrate` reports compatibility posture and available no-op migrations but has no apply mode.
- Generated artifact behavior was not changed; the existing Q05 `aide compile --write` path was used only to refresh the manifest after Q06 changed source inputs.
- `.aide/profile.yaml` still contains Q05-era current-focus wording because it was not in the Q06 implementation allowlist.

### Verification

- Ran pre-change `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate`.
- Ran post-change `py -3 scripts/aide validate`, `doctor`, `migrate`, `compile`, and `bakeoff`.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Ran compatibility record existence and anchor checks.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q06-compatibility-baseline/evidence/validation.md`.

### Regressions Avoided

- No real migrations, migration apply mode, Runtime, Host, Commander, Mobile, IDE extension, provider, browser, app, release, service, or Dominium Bridge behavior was added.
- No generated target policy was changed and no final `CLAUDE.md` or `.claude/**` target was created.
- No bootstrap-era implementation, host proof, governance, inventory, matrix, research, spec, environment, lab, top-level eval, or packaging path was modified.

### Remaining Issues

- Q06 requires review before Compatibility baseline v0 is accepted.
- Q00 through Q03 and Q05 still have raw `needs_review` queue statuses; Q05 review evidence is `PASS_WITH_NOTES` and explicitly allowed Q06.
- Full YAML/schema validation, real migrations, shims, and compatibility replay beyond summary anchors remain later work.
- Dominium Bridge baseline remains Q07.

## Work Item: Q07-dominium-bridge-baseline

### Status

Needs Review

### Changed Paths

- `bridges/dominium/**`
- `core/harness/**`
- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `docs/reference/dominium-bridge.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/charters/bridges-charter.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q07-dominium-bridge-baseline/**`
- `.aide/queue/index.yaml`

### Rationale

Q07 establishes the first AIDE-side Dominium Bridge baseline so Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance.

### Notable Design Decisions

- Kept the bridge AIDE-side only; no external Dominium repository paths were touched.
- Kept XStack Dominium-local and strict rather than promoting it into generic AIDE doctrine.
- Used `pinned-managed-repo-layer` as the near-term adoption mode.
- Added a profile overlay and strict policy overlays rather than replacing `.aide/profile.yaml` or weakening base AIDE policy.
- Recorded generated target classes as metadata only; no real Dominium outputs were emitted.
- Referenced the Q06 Compatibility baseline and Q05 generated artifact ids without creating a separate bridge version system.
- Added only structural Harness bridge checks and compile-plan reporting.

### Tradeoffs

- Bridge validation remains line-oriented and structural, not full YAML/schema validation.
- Dominium-side adoption, pins, generated outputs, and proof execution remain future work.
- Q07 records stricter XStack expectations but does not implement XStack internals.
- The Q05 generated manifest remains stale because Q07 changed generated-artifact source inputs and this task did not refresh generated outputs.

### Verification

- Ran pre-change Harness validation, doctor, compile, and migrate checks.
- Ran post-change Harness validation, doctor, compile dry-run, migrate, and bakeoff checks.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Checked required Dominium Bridge files and structural anchors.
- Checked generated artifact drift and confirmed no real Dominium outputs were emitted.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q07-dominium-bridge-baseline/evidence/validation.md`.

### Regressions Avoided

- No external Dominium repository was modified.
- No real Dominium generated output was emitted.
- No Runtime, Host, Commander, Mobile, IDE extension, provider adapter, browser bridge, app surface, release automation, service, or autonomous worker implementation was added.
- No Q08 or later work was implemented.

### Remaining Issues

- Q07 requires independent review before Q08 planning or Dominium-side adoption work.
- Q05 generated manifest source fingerprint is stale because Q07 changed source inputs and did not run `aide compile --write`.
- `.aide/profile.yaml` still contains Q05/Q06-era high-level wording; cleanup remains deferred to a later reviewed task.

## Work Item: Q07 Dominium Bridge Baseline Review

### Status

Passed with notes.

### Changed Paths

- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-validation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-risks.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-recommendation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/status.yaml`
- `.aide/queue/index.yaml`
- `PLANS.md`

### Rationale

Record the independent Q07 review outcome and mark the canonical queue state so Q08 planning can proceed from a passed Dominium Bridge baseline.

### Notable Design Decisions

- Accepted Q07 as `PASS_WITH_NOTES` rather than `PASS` because generated manifest drift and stale summary/doctor guidance remain visible cleanup items.
- Marked Q07 `passed` in queue state because Q07 `status.yaml` allowed the transition and the review prompt permitted Q07 status/index updates.
- Did not refresh generated artifacts because the review task forbids generated artifact mutation.

### Verification

- Ran `py -3 scripts/aide --help`, `validate`, `doctor`, `compile --dry-run`, `migrate`, and `bakeoff`.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Checked bridge files, anchors, policy strictness, generated-output absence, dependency/scope boundaries, compile determinism, `git diff --check`, and review allowed paths.

Detailed command output is recorded in `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-validation.md`.

### Regressions Avoided

- No Dominium Bridge, Harness, Compatibility, generated artifact, Runtime, Host, provider, release, app, or Q08 implementation files were modified by the review.
- No external Dominium repository was touched.
- No real Dominium generated outputs were emitted.

### Remaining Issues

- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact task.
- `aide doctor` still prints Q07 review as the next recommended step after Q07 is passed; this should be cleaned up before automation treats doctor output as an execution signal.
- Q00-Q03, Q05, and Q06 raw queue statuses remain review-gated even though later review evidence accepted proceeding with notes.

## Work Item: Q08 Self-Hosting Automation

### Status

Needs Review

### Changed Paths

- `core/harness/**`
- `scripts/aide-queue-next`
- `scripts/aide-queue-run`
- `.aide/runs/self-check/latest.md`
- `docs/reference/self-hosting-automation.md`
- `docs/reference/self-bootstrap.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/dominium-bridge.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q08-self-hosting-automation/**`
- `.aide/queue/index.yaml`

### Rationale

Q08 adds the first safe self-hosting automation scaffold so AIDE can inspect its own queue, drift, Compatibility, and bridge state without becoming an uncontrolled autonomous runtime.

### Notable Design Decisions

- Added `aide self-check` to the existing Harness command surface rather than adding a new service or external worker runner.
- Kept self-check report-first by default, with explicit `--write-report` limited to `.aide/runs/self-check/latest.md`.
- Fixed stale doctor next-step guidance by computing the next recommendation from Q08 queue state.
- Improved `scripts/aide-queue-next` and `scripts/aide-queue-run` so they report review-gate posture instead of failing or implying automatic execution.
- Reported stale generated manifest drift and recommended a reviewed generated-artifact QFIX instead of refreshing `.aide/generated/manifest.yaml`.

### Verification

- Ran pre-change Harness validation, doctor, compile dry-run, migrate, bakeoff, queue-status, and queue-next checks.
- Ran post-change Harness validation, doctor, compile dry-run, migrate, bakeoff, self-check, and self-check report writing.
- Ran `scripts/aide --help`, `scripts/aide import`, queue helper smoke checks, Harness tests, Compatibility tests, PowerShell-expanded Python syntax checks, generated artifact absence checks, dependency/scope scans, and `git diff --check`.

Detailed command output is recorded in `.aide/queue/Q08-self-hosting-automation/evidence/validation.md`.

### Regressions Avoided

- No external agents, models, providers, browsers, network calls, or external CI were introduced.
- No generated artifacts were refreshed.
- No Runtime, Service, Commander, Host, Mobile, app, release, package, or autonomous worker implementation was added.
- No Dominium repository or real Dominium generated output was touched.

### Remaining Issues

- Q08 requires independent review.
- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact QFIX.
- `.aide/commands/catalog.yaml` does not yet list `aide self-check`; Q08 left that metadata sync deferred because `.aide/commands/**` was outside the implementation allowed paths.
- Q00-Q03, Q05, and Q06 raw queue-status nuance remains visible and unresolved.

## Work Item: Q08 Self-Hosting Automation Review

### Status

Passed With Notes

### Changed Paths

- `.aide/queue/Q08-self-hosting-automation/evidence/review.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-validation.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-risks.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-recommendation.md`
- `.aide/queue/Q08-self-hosting-automation/status.yaml`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The Q08 independent review accepted the report-first self-hosting automation scaffold as safe for post-Q08 foundation review while preserving visible cleanup notes for generated manifest drift, command catalog metadata, and older raw status nuance.

### Verification

- Ran Harness command smoke for `--help`, `validate`, `doctor`, `compile --dry-run`, `migrate`, `bakeoff`, `self-check`, and `self-check --write-report`.
- Ran queue helper smoke for `aide-queue-status`, `aide-queue-next`, and `aide-queue-run`.
- Ran Harness and Compatibility unit tests.
- Ran Python syntax checks for Harness, Compatibility, and queue helper scripts.
- Ran safety scans for external calls, automatic worker invocation, auto-merge, and generated artifact refresh behavior.
- Ran `git diff --check`.

Detailed command output is recorded in `.aide/queue/Q08-self-hosting-automation/evidence/review-validation.md`.

### Regressions Avoided

- No self-hosting automation implementation, Harness implementation, queue helper implementation, generated artifacts, contract catalogs, Runtime, Host, Commander, provider, browser, app, release, external CI, or post-Q08 implementation files were modified by the review.
- No generated artifacts were refreshed.
- No external worker or Dominium repository was touched.

### Remaining Issues

- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact QFIX.
- `.aide/commands/catalog.yaml` still does not list `aide self-check`; a bounded metadata sync should handle this before the next horizon.
- Q00-Q03, Q05, and Q06 raw queue-status nuance remains visible and should be reconciled or explicitly documented before the next horizon.

## Work Item: Q09 State Reconciliation And Token Survival Core

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q09-token-survival-core/**`
- `.aide/queue/index.yaml`
- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/policies/**`
- `.aide/prompts/**`
- `.aide/context/**`
- `.aide/memory/**`
- `.aide/scripts/**`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `core/harness/**`

### Rationale

Q09 starts the post-Q08 token-survival horizon. The immediate product constraint is that AIDE must reduce token usage and charges for equivalent-quality work, so this phase reconciles stale current-state records and adds compact repo-derived task packets, approximate token estimates, evidence-review prompts, and no-full-history guidance.

### Notable Design Decisions

- Keep Q09 repo-only and no-install; Gateway, provider calls, model routing, Runtime, Service, Commander, Mobile, MCP/A2A, and autonomous loops remain deferred.
- Preserve older raw queue status nuance instead of silently rewriting Q00-Q03, Q05, or Q06.
- Treat `.aide/runs/self-check/latest.md` as non-canonical evidence and prefer fresh command output for live state.
- Use Python standard library only for AIDE Lite token-survival tooling.
- Store generated Q09 context outputs under `.aide/context/` without inlining source contents; the formal token ledger remains deferred to Q14.
- Relocate unit tests to `core/harness/tests` because Python unittest cannot import hidden `.aide/scripts/tests` with the requested `-t .` discovery shape.

### Verification

Baseline validation passed before edits. Q09 generated `.aide/context/latest-task-packet.md` for Q10 at 2,587 chars and 647 approximate tokens. Detailed final command output is recorded in `.aide/queue/Q09-token-survival-core/evidence/validation.md`.

### Regressions Avoided

- No provider/model/network calls were added.
- No Gateway, Runtime, Service, Commander, Mobile, MCP/A2A, host implementation, app surface, or autonomous loop was added.
- No raw provider credentials, local caches, `.aide.local` data, or raw prompt logs were committed.

### Remaining Issues

- Q09 awaits independent review.
- Token counts are approximate only.
- AIDE Lite still needs Q10 hardening for drift detection and stronger validation.
- Context compiler, verifier, ledger, golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q10 AIDE Lite Hardening

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q10-aide-lite-hardening/**`
- `.aide/queue/index.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/context/repo-snapshot.json`
- `.aide/context/latest-task-packet.md`
- `.aide/commands/catalog.yaml`
- `.aide/generated/manifest.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_lite.py`

### Rationale

Q10 makes the Q09 token-survival workflow repeatable enough to become the default path for future AIDE queue prompts. AIDE Lite now has stronger validation, deterministic writes, adapter drift handling, snapshot summaries, packet budget warnings, importable helpers, and direct stdlib tests.

### Notable Design Decisions

- Keep AIDE Lite standard-library only and repo-local; no provider, model, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, or host behavior was added.
- Use generated `AGENTS.md` markers consistent with existing AIDE generated-section conventions while preserving manual content outside the managed section.
- Replace legacy Q09 token-survival markers only because they are managed output.
- Keep approximate `chars / 4` token counts; exact tokenizer and provider billing remain deferred.
- Keep context compilation shallow until Q11; Q10 snapshots record metadata and hashes only, not file contents.
- Keep direct `.aide/scripts/tests` discovery as the supported no-install test shape because Python `-t .` discovery is awkward for hidden `.aide` import names.

### Verification

Q10 validation covered Harness validate/doctor/self-check, Harness and Compatibility unit tests, AIDE Lite doctor/validate/snapshot/pack/estimate/adapt/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md`.

### Regressions Avoided

- No long-history prompt storage, raw provider credentials, `.aide.local` state, local caches, or raw prompt logs were committed.
- No Gateway, provider router, live model calls, local model setup, exact tokenizer, provider billing ledger, full verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.
- No generated artifact manifest was hand-edited; it was refreshed through `scripts/aide compile --write` after command catalog/index changes.

### Remaining Issues

- Q10 awaits independent review.
- Token estimates remain approximate only.
- Context compiler, verifier, token ledger, golden tasks, router profile, cache boundary, and Gateway remain later phases.
- Python unittest discovery with `-s .aide/scripts/tests -t .` remains a documented hidden-path limitation; direct `.aide/scripts/tests` discovery passes.

## Work Item: Q11 Context Compiler v0

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q11-context-compiler-v0/**`
- `.aide/queue/index.yaml`
- `.aide/context/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_lite.py`

### Rationale

Q11 reduces prompt size by replacing broad repo/history context with deterministic repo maps, test maps, context indexes, latest context packets, exact refs, and context-backed task packets.

### Notable Design Decisions

- Kept the Context Compiler standard-library only and deterministic.
- Used path and extension heuristics for role detection; no semantic certainty is claimed.
- Used test path/name heuristics with confidence and reason fields; no complete coverage is claimed.
- Kept generated context artifacts content-free: refs, hashes, sizes, roles, priorities, counts, and test candidates only.
- Added `path#Lstart-Lend` validation without full excerpt extraction.
- Left `.aide/generated/manifest.yaml` drift visible because Q11 does not allow generated manifest edits.

### Verification

Q11 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/adapt/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q11-context-compiler-v0/evidence/validation.md`.

### Regressions Avoided

- No raw source contents, secrets, `.env` content, local state, `.aide.local` data, caches, provider credentials, or raw prompt logs were committed.
- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, embeddings, vector search, semantic cache, full verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.

### Remaining Issues

- Q11 awaits independent review.
- Role classification and test mapping remain heuristics.
- Token counts remain approximate only.
- Q12 verifier, Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q12 Verifier v0

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q12-verifier-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/verification.yaml`
- `.aide/verification/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_verifier.py`

### Rationale

Q12 reduces premium-model review burden by moving structural checks into deterministic AIDE Lite verifier behavior. Future GPT-5.5 review can consume compact verifier output and evidence instead of re-checking packet sections, refs, scope, adapter drift, token warnings, or obvious secret risks.

### Notable Design Decisions

- Kept the verifier standard-library only and repo-local.
- Used conservative file-ref extraction from backticks and markdown links rather than trying to parse arbitrary prose.
- Kept changed-file scope path-based against the active queue task; no semantic diff analysis is claimed.
- Treated secret scanning as heuristic and allowed policy terms when they do not resemble real key values.
- Wrote compact verification reports without raw file contents.

### Verification

Q12 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/verify variants/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q12-verifier-v0/evidence/validation.md`.

### Regressions Avoided

- No raw source dumps, secrets, `.env` contents, `.aide.local` state, local caches, provider credentials, or raw prompt logs were committed.
- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, LLM-as-judge, automatic repair, golden tasks, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.

### Remaining Issues

- Q12 awaits independent review.
- Verification remains structural, path-based, and heuristic.
- Token counts remain approximate only.
- Q13 Evidence Review Workflow, Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q13 Evidence Review Workflow

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q13-evidence-review-workflow/**`
- `.aide/queue/index.yaml`
- `.aide/verification/review-packet.template.md`
- `.aide/verification/review-decision-policy.yaml`
- `.aide/policies/verification.yaml`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/context/**`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q13 reduces premium-model review burden by producing a compact review packet that references task packets, context packets, verifier reports, evidence files, changed-file summaries, validation summaries, token summaries, risks, and non-goals. GPT-5.5 review can now start from `.aide/context/latest-review-packet.md` instead of re-reading full chat history, whole repo docs, or broad roadmap context.

### Notable Design Decisions

- Kept review-pack deterministic, standard-library only, and repo-local.
- Generated review packets contain references and compact summaries, not full source files or full diffs.
- Added `verify --review-packet` so malformed review packets are checked mechanically before review.
- Added decision policy rules for `PASS`, `PASS_WITH_NOTES`, `REQUEST_CHANGES`, and `BLOCKED`.
- Left automatic GPT/model calls explicitly out of scope.

### Verification

Q13 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/pack/estimate/selftest, review-packet verification, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md`.

### Regressions Avoided

- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, LLM-as-judge automation, automatic GPT review, automatic repair, or autonomous loop was introduced.
- No raw source dumps, full diffs, secrets, `.env` content, local state, `.aide.local` data, caches, provider credentials, or raw prompt logs were committed.

### Remaining Issues

- Q13 awaits independent review.
- Review packet quality depends on evidence quality.
- Token counts remain approximate only.
- Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q14 Token Ledger and Savings Report

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q14-token-ledger-savings-report/**`
- `.aide/queue/index.yaml`
- `.aide/policies/token-ledger.yaml`
- `.aide/policies/token-budget.yaml`
- `.aide/reports/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_token_ledger.py`
- `.aide/context/**`
- `.aide/verification/latest-verification-report.md`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q14 makes AIDE's token-saving claim measurable. It records estimated metadata for compact packets, verification reports, evidence surfaces, prompt templates, generated guidance, and named naive baselines so future phases can compare compact repo-derived packets against broader prompt bundles without storing raw prompts or raw responses.

### Notable Design Decisions

- Kept token accounting deterministic, standard-library only, and repo-local.
- Used `ceil(chars / 4)` as the explicit approximation method; exact tokenizer and provider billing remain deferred.
- Stored metadata-only JSONL records with path, surface, chars, lines, approximate tokens, budget, budget status, and notes.
- Added named baselines for root-history, review, repo-context, and token-survival comparisons.
- Added budget status values and advisory regression warnings without making Q14 a billing system or quality eval system.
- Integrated ledger readiness into AIDE Lite doctor, validate, estimate, pack, context, review, verify, and selftest behavior where bounded.

### Verification

Q14 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/ledger compare/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md`.

### Regressions Avoided

- No raw prompt bodies, raw response bodies, provider credentials, `.env` contents, `.aide.local` state, local caches, provider billing records, or exact-token claims were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, LLM-as-judge automation, automatic GPT review, automatic repair, golden tasks, or autonomous loop was introduced.

### Remaining Issues

- Q14 awaits independent review.
- Token counts remain approximate only.
- The ledger does not measure provider billing, hidden reasoning tokens, cached-token discounts, or quality outcomes.
- Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q15 Golden Tasks v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q15-golden-tasks-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/evals.yaml`
- `.aide/evals/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_golden_tasks.py`
- `.aide/reports/**`
- `.aide/context/**`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q15 makes AIDE's quality-preservation claim measurable for the token-saving workflow. Q14 can show that compact artifacts are smaller; Q15 checks that the smaller artifacts still include required sections, references, evidence shape, verifier failure detection, review-packet shape, token-ledger metadata, and adapter managed-section determinism.

### Notable Design Decisions

- Kept golden tasks deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added six initial golden tasks for compact task packets, context packets, verifier bad-evidence detection, review packets, token ledger metadata, and managed adapter determinism.
- Stored eval reports as deterministic metadata and Markdown summaries under `.aide/evals/runs/`.
- Integrated `eval list`, `eval run`, and `eval report` into AIDE Lite doctor, validate, selftest, and ledger scan/report behavior.
- Treated token reduction as invalid when golden tasks fail, while explicitly not claiming arbitrary coding quality or external benchmark coverage.

### Verification

Q15 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/eval list/eval run/eval report/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory discovery behavior, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, or provider billing records were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, external benchmark integration, LLM-as-judge, automatic GPT review, automatic repair, Q16 recommendation engine, or autonomous loop was introduced.

### Remaining Issues

- Q15 awaits independent review.
- Golden tasks are deterministic local quality gates for AIDE's token-survival substrate, not arbitrary coding-task quality proof.
- Token counts remain approximate only.
- Q16 Outcome Controller, Router Profile, cache boundary, and Gateway remain later phases.

## Work Item: Q16 Outcome Controller v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q16-outcome-controller-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/controller.yaml`
- `.aide/controller/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_outcome_controller.py`
- `.aide/scripts/tests/test_review_pack.py`
- `.aide/context/**`
- `.aide/reports/**`
- `.aide/evals/runs/**`
- `.aide/prompts/**`
- `.aide/memory/**`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q16 makes AIDE's self-optimization posture advisory, measured, and review-gated. It reads local token, verifier, review-packet, golden-task, context, and adapter signals and converts them into concrete recommendations without applying them automatically.

### Notable Design Decisions

- Kept the controller deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added `.aide/policies/controller.yaml` and `.aide/controller/failure-taxonomy.yaml` to define allowed inputs, outputs, failure classes, recommendation requirements, and forbidden behaviors.
- Stored outcome records as metadata-only JSONL under `.aide/controller/outcome-ledger.jsonl`.
- Added `outcome add`, `outcome report`, and `optimize suggest` to AIDE Lite.
- Required recommendations to include evidence source, expected benefit, risk level, next action, rollback condition, and `applies_automatically: false`.
- Treated Q17 Router Profile as the next advisory phase only; no routing, Gateway, provider, or Runtime behavior was introduced.

### Verification

Q16 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/eval list/eval run/eval report/outcome report/outcome add/optimize suggest/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory discovery behavior, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q16-outcome-controller-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, provider billing records, or raw model traces were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, Router Profile behavior, or autonomous loop was introduced.

### Remaining Issues

- Q16 awaits independent review.
- Recommendations are local and heuristic; they are inputs to future queue work, not an automatic optimizer.
- Token counts remain approximate only.
- Q17 Router Profile, Q18 cache/local-state boundary, Gateway/provider/runtime/UI work, and model/provider evals remain later phases.

## Work Item: Q17 Router Profile v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q17-router-profile-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/routing.yaml`
- `.aide/models/**`
- `.aide/routing/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_router_profile.py`
- `.aide/context/**`
- `.aide/reports/**`
- `.aide/prompts/**`
- `.aide/memory/**`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q17 makes AIDE's future model/tool choice evidence-based before any live routing
exists. It reads compact task/context packets and local verifier, token,
golden-task, review, and outcome signals, then writes advisory route decisions
with a route class, hard-floor status, quality gates, evidence sources, and
fallback guidance.

### Notable Design Decisions

- Kept routing deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added `.aide/policies/routing.yaml` plus advisory `.aide/models/**` metadata for providers, capabilities, route profiles, hard floors, and fallbacks.
- Added `.aide/routing/latest-route-decision.json` and `.aide/routing/latest-route-decision.md` as metadata-only route artifacts.
- Added `route list`, `route validate`, and `route explain` to AIDE Lite.
- Preserved hard floors for architecture, security, self-modification, final promotion, governance, destructive, and high-stakes work.
- Routed deterministic work toward `no_model_tool` and unknown work conservatively toward frontier or human review.

### Verification

Q17 validation covered Harness validate/doctor/self-check, Harness and
Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify
/review-pack/ledger scan/ledger report/eval list/eval run/eval report/outcome
report/optimize suggest/route list/route validate/route explain/pack/estimate
/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory
discovery behavior, `git diff --check`, and targeted secret scanning. Detailed
command output is recorded in
`.aide/queue/Q17-router-profile-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, provider billing records, or raw model traces were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, cache boundary, or autonomous loop was introduced.

### Remaining Issues

- Q17 awaits independent review.
- Route heuristics are conservative and local; they are route advice, not execution.
- Provider capabilities are advisory metadata only; no live availability probing or current pricing exists.
- Token counts remain approximate only.
- Q18 cache/local-state boundary, Gateway/provider/runtime/UI work, and model/provider evals remain later phases.

## Work Item: Q18 Cache and Local State Boundary

### Status

Implemented and awaiting review.

### Changed Paths

- `.gitignore`
- `.aide.local.example/**`
- `.aide/policies/cache.yaml`
- `.aide/policies/local-state.yaml`
- `.aide/cache/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_cache_local_state.py`
- `.aide/queue/Q18-cache-local-state-boundary/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/cache-local-state-boundary.md`

### Rationale

Q18 prevents future Gateway, provider, runtime, and cache work from mixing committed AIDE contract records with machine-local runtime state. It creates deterministic cache-key metadata now while explicitly deferring live cache behavior.

### Notable Design Decisions

- `.aide/` remains committed contract and reviewable metadata.
- `.aide.local/` is gitignored local runtime state and must not be tracked.
- `.aide.local.example/` documents the safe layout without secrets.
- Cache reports store SHA-256 metadata, dependency hashes, policy versions, and dirty-state notes only.
- Cache hits do not bypass verifier, golden tasks, route hard floors, or review gates.
- Semantic cache for code edits and provider response cache remain disabled until future reviewed policy.

### Verification

Q18 validation covers Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/route/cache/pack/estimate/selftest, cache unit tests, `git check-ignore .aide.local/`, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q18-cache-local-state-boundary/evidence/validation.md`.

### Regressions Avoided

- No actual `.aide.local/` contents were committed.
- No raw prompts, raw responses, provider response bodies, semantic answers, traces, local cache blobs, provider credentials, `.env` contents, exact-token claims, or provider billing records were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, live cache, or autonomous loop was introduced.

### Remaining Issues

- Q18 awaits independent review.
- Cache keys are deterministic metadata only and do not prove stale content is safe to reuse.
- No live Gateway, provider response cache, semantic cache, exact tokenizer, provider billing integration, local model KV cache, or runtime cache service exists.
- Q19 Gateway Architecture and Skeleton remains the next bounded phase.

## Work Item: Q19 Gateway Architecture and Skeleton

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/gateway.yaml`
- `.aide/gateway/**`
- `core/gateway/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_gateway_commands.py`
- `.aide/queue/Q19-gateway-architecture-skeleton/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/gateway-skeleton.md`

### Rationale

Q19 creates a safe local Gateway boundary after Q09-Q18 established compact
context, verification, review packets, token accounting, golden tasks,
advisory outcomes, advisory routes, cache keys, and local-state policy. It
exposes those local signals before any provider adapter or live proxy exists.

### Notable Design Decisions

- Added `.aide/policies/gateway.yaml` with local skeleton, report-only, and
  no-provider-forwarding operating mode.
- Added `.aide/gateway/` architecture, endpoint, lifecycle, security-boundary,
  and latest-status artifacts.
- Added `core/gateway/gateway_status.py` for compact health, status, route,
  summaries, and version payloads.
- Added `core/gateway/server.py` as a localhost-only stdlib HTTP skeleton.
- Added AIDE Lite `gateway status`, `gateway endpoints`, `gateway smoke`, and
  `gateway serve`.
- Integrated Gateway readiness into AIDE Lite validation, doctor, verification,
  review-packet summaries, and selftest.

### Verification

Q19 validation covers Harness validate/doctor/self-check, Harness and
Compatibility tests, core Gateway tests, AIDE Lite
doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/
optimize/route/cache/gateway/pack/estimate/selftest, Gateway endpoint smoke,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q19-gateway-architecture-skeleton/evidence/validation.md`.

### Regressions Avoided

- No provider calls, model calls, outbound network calls, or real Gateway proxy
  forwarding were introduced.
- No OpenAI-compatible or Anthropic-compatible forwarding endpoints were
  implemented.
- No raw prompts, raw responses, provider credentials, `.env` contents,
  `.aide.local` state, local traces, or real cache blobs were committed.
- No Runtime, Service, Commander, UI, Mobile, MCP/A2A, provider adapter, or
  autonomous loop was introduced.

### Remaining Issues

- Q19 awaits independent review.
- The skeleton is not a production Gateway and has no authentication,
  authorization, live route execution, service manager, provider adapters,
  provider billing, or exact tokenizer.
- Q20 Provider Adapter v0 remains the next bounded phase and must still respect
  `.aide.local/`, no raw prompt/response storage, verifier/golden-task gates,
  and Gateway safety policy.

## Work Item: Q20 Provider Adapter v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/provider-adapters.yaml`
- `.aide/providers/**`
- `core/providers/**`
- `core/gateway/gateway_status.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_provider_adapter.py`
- `.aide/queue/Q20-provider-adapter-v0/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/provider-adapter-v0.md`

### Rationale

Q20 defines provider adapters as offline contracts before any live provider
execution exists. Provider routing can reduce token waste only when provider
families, privacy posture, credential boundaries, capability metadata, and
hard-floor rules are explicit and testable.

### Notable Design Decisions

- Added `.aide/policies/provider-adapters.yaml` with offline-contracts-only,
  metadata-validation-only, and no-provider-calls operating mode.
- Added `.aide/providers/` catalog, capability matrix, adapter contract, static
  status, and latest provider status reports.
- Added `core/providers/**` standard-library dataclasses, catalog parsing,
  validation, status rendering, and offline probe helpers.
- Added AIDE Lite `provider list`, `provider status`, `provider validate`,
  `provider contract`, and `provider probe --offline`.
- Integrated provider readiness into AIDE Lite validation, verification,
  doctor, selftest, review-packet summaries, advisory route notes, and Gateway
  status summaries.

### Verification

Q20 validation covers Harness validate/doctor/self-check, Harness,
Compatibility, Gateway, and Provider tests, AIDE Lite
doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/
optimize/route/cache/gateway/provider/pack/estimate/selftest,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q20-provider-adapter-v0/evidence/validation.md`.

### Regressions Avoided

- No live provider calls, model calls, outbound network calls, provider probes,
  credential setup, or Gateway forwarding were introduced.
- No raw prompts, raw responses, provider credentials, `.env` contents,
  `.aide.local` state, local traces, provider response caches, or real cache
  blobs were committed.
- No Runtime, Service, Commander, UI, Mobile, MCP/A2A, local model setup,
  provider billing, exact tokenizer, automatic GPT review, automatic repair, or
  autonomous loop was introduced.

### Remaining Issues

- Q20 awaits independent review.
- Capability metadata is conservative contract metadata, not measured provider
  performance, availability, pricing, latency, or quality evidence.
- Future live provider work still needs explicit reviewed phases for
  credentials, provider probes, Gateway forwarding, provider response caching,
  billing, and exact capability validation.
- Q21 Existing Tool Adapter Compiler v0 remains the next bounded phase.

## Work Item: QFIX-01 Foundation Review Reconciliation

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/QFIX-01-foundation-review-reconciliation/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q09-token-survival-core/status.yaml` and `evidence/review.md`
- `.aide/queue/Q10-aide-lite-hardening/status.yaml` and `evidence/review.md`
- `.aide/queue/Q11-context-compiler-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q12-verifier-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q13-evidence-review-workflow/status.yaml` and `evidence/review.md`
- `.aide/queue/Q14-token-ledger-savings-report/status.yaml` and `evidence/review.md`
- `.aide/queue/Q15-golden-tasks-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q16-outcome-controller-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q17-router-profile-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q18-cache-local-state-boundary/task.yaml`, `status.yaml`, and `evidence/review.md`
- `.aide/queue/Q19-gateway-architecture-skeleton/status.yaml` and `evidence/review.md`
- `.aide/queue/Q20-provider-adapter-v0/status.yaml` and `evidence/review.md`
- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- root docs

### Rationale

QCHECK found that Q09-Q20 existed and mostly worked, but future agents would
still waste context on stale source-of-truth records. QFIX-01 accepts the
token-survival foundation with notes, fixes Q18 drift, updates profile and
self-check guidance, and records QFIX-02 as the next repair before Q21.

### Reconciliation Decisions

- Q09-Q20 are accepted with notes, not marked flawless.
- Q18 task/status drift is fixed.
- `.aide/profile.yaml` now describes the post-token-foundation reconciliation
  state rather than stale Q09 focus.
- `scripts/aide self-check` no longer recommends stale Q09 once Q09-Q20 are
  accepted.
- Gateway and provider surfaces remain no-call/report-only or offline metadata.

### Verification

Baseline validation before edits covered Harness validate/doctor/self-check,
AIDE Lite doctor/validate/verify/eval/route/cache/provider checks, Harness,
Compatibility, Gateway, and Provider tests, and the known failing
`.aide/scripts/tests` discovery command. Final validation is recorded in
`.aide/queue/QFIX-01-foundation-review-reconciliation/evidence/validation.md`.

### Remaining Issues

- QFIX-01 itself still requires review.
- QFIX-02 must repair standard `.aide/scripts/tests` discovery and a routine
  runner.
- Token savings remain estimated, not billing truth.
- Golden tasks remain substrate quality gates, not arbitrary coding-task proof.
- Cross-repo pack export/import and Eureka/Dominium pilots remain future work.

## Work Item: QFIX-02 AIDE Lite Test Discovery And Runner Fix

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/**`
- `.aide/queue/index.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- `docs/reference/aide-lite.md`
- `docs/reference/aide-lite-test-runner.md`
- root docs

### Rationale

The QCHECK audit and QFIX-01 evidence showed that the AIDE Lite suite passed
when run with the direct discovery form but failed under
`py -3 -m unittest discover -s .aide/scripts/tests -t .`. That failure made
validation feel broken even though the tests were healthy. QFIX-02 makes
`py -3 .aide/scripts/aide_lite.py test` the canonical validation command and
documents the old `-t .` form as non-canonical for the hidden `.aide` path.

### Implementation Notes

- Added `test` as a stable alias over the existing internal selftest runner.
- Preserved `selftest` as a compatibility command.
- Added tests for import-without-CLI-side-effects, `test` pass behavior,
  controlled failure return code, command catalog truth, and Harness next-step
  guidance while QFIX-02 is active.
- Kept the supported raw unittest command as
  `py -3 -m unittest discover -s .aide/scripts/tests`.
- Did not add package markers under `.aide/` or move AIDE Lite into a Python
  package.

### Verification

Final validation is recorded in
`.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/validation.md`.
Key checks include Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest, supported `.aide/scripts/tests` discovery,
Harness/Compatibility/Gateway/Provider tests, `git diff --check`, and targeted
secret scans.

### Remaining Issues

- QFIX-02 itself still requires review.
- The old `-t .` discovery command remains invalid/non-canonical by design.
- Q21 Cross-Repo Pack Export / Import v0 is next after QFIX-02 review.
- Token savings remain estimated, and no arbitrary coding-task quality proof is
  introduced.
- No Gateway/provider/model runtime behavior is introduced.

## Work Item: Q21 Cross-Repo Pack Export / Import v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q21-cross-repo-pack-export-import-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/export-import.yaml`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/import/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/codex-token-mode.md`
- root docs and `docs/reference/cross-repo-pack-export-import.md`

### Rationale

Q21 makes the token-survival foundation portable before the first real
Eureka/Dominium pilots. It prevents manual broad copying from contaminating
target repos with AIDE source identity, queue history, generated context,
reports, latest status artifacts, local state, raw prompts, raw responses, or
secrets.

### Notable Design Decisions

- Added `.aide/policies/export-import.yaml` to define the portable pack
  include/exclude boundary.
- Added `.aide/import/**` target-neutral templates for profile, project state,
  decisions, open risks, and import reports.
- Added AIDE Lite `export-pack`, `import-pack`, and `pack-status` commands.
- Generated `.aide/export/aide-lite-pack-v0/` with manifest, checksums, install
  docs, import policy, export report, and portable `files/`.
- Import preserves manual `AGENTS.md` content through a managed portable
  section, creates target-specific placeholders when absent, and ensures
  `.aide.local/` remains ignored.
- Fixture validation uses temporary local repositories only; real Eureka and
  Dominium imports remain Q22/Q23.

### Verification

Q21 validation covers Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest/export-pack/pack-status/import-pack dry-run and
import, fixture target doctor/snapshot/index/pack/estimate, AIDE Lite
export/import unit tests, Harness/Compatibility/Gateway/Provider tests,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q21-cross-repo-pack-export-import-v0/evidence/validation.md`.

### Regressions Avoided

- No real Eureka or Dominium repositories were mutated.
- No source repo `.aide/profile.yaml`, `.aide/queue/**`, source memory,
  generated context, reports, controller ledgers, route/cache/Gateway/provider
  latest status artifacts, eval runs, `.aide.local/`, `.env`, secrets, raw
  prompts, or raw responses were copied into the portable pack.
- No provider calls, model calls, network calls, Gateway forwarding, Runtime,
  Service, Commander, UI, Mobile, MCP/A2A, existing-tool adapter compiler, or
  autonomous loop was introduced.

### Remaining Issues

- Q21 awaits independent review.
- Fixture import proves portability mechanics only; Q22 and Q23 must measure
  real target-repo token savings and quality preservation.
- Target-specific profile and memory placeholders still require human or
  project-specific completion after import.
- Exact tokenizer, provider billing, live provider execution, and existing-tool
  adapter compiler work remain deferred.

## Work Item: Q24 Existing Tool Adapter Compiler v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/adapters.yaml`
- `.aide/adapters/**`
- `.aide/generated/adapters/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_adapter_compiler.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- root docs and `docs/reference/existing-tool-adapter-compiler-v0.md`

### Rationale

Most AIDE users will reach AIDE first through existing coding tools rather than
through a future Gateway or Service. Q24 compiles AIDE's compact-packet,
context, validation, evidence, review-gate, local-state, and no-provider-call
rules into concise tool-specific guidance for Codex, Claude Code, Aider, Cline,
Continue, Cursor, and Windsurf.

### Implementation Notes

- Added `.aide/policies/adapters.yaml` for template-compiler-only operation,
  generated or preview outputs, managed-section rules, drift detection, and
  no-runtime/no-provider/no-network safety.
- Added `.aide/adapters/targets.yaml` and templates for Codex/AGENTS, Claude
  Code, Aider, Cline, Continue, Cursor, and Windsurf.
- Added AIDE Lite `adapter list`, `adapter render`, `adapter preview`,
  `adapter validate`, `adapter drift`, and `adapter generate` commands.
- Kept `adapt` backward-compatible as a deterministic shortcut for the safe
  `AGENTS.md` managed section.
- Generated adapter previews under `.aide/generated/adapters/**` and updated
  only the managed section in root `AGENTS.md`.
- Updated the portable AIDE Lite Pack to include adapter templates and policy
  so target repos can generate local guidance after import.

### Verification

Final validation is recorded in
`.aide/queue/Q24-existing-tool-adapter-compiler-v0/evidence/validation.md`.
Key checks include Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest, adapter list/render/preview/validate/drift,
deterministic `adapt`, export-pack refresh, AIDE Lite adapter compiler tests,
full AIDE Lite test discovery, Harness/Compatibility/Gateway/Provider tests,
`git diff --check`, `.aide.local/` ignore verification, and targeted secret
scan.

### Remaining Issues

- Q24 itself still requires review.
- Q22 and Q23 target-pilot evidence is now present in the sibling Eureka and
  Dominium repositories and awaits target-repo review. Q24 evidence was
  refreshed read-only to record those pilot results, but generated adapter
  outputs still need target-tool usage evidence.
- Non-AGENTS tool outputs are preview-only.
- Generated guidance is advisory and depends on each tool reading it.
- Exact tokenizer, provider billing, live provider execution, Gateway
  forwarding, IDE extensions, and runtime enforcement remain deferred.

## Work Item: Q24 Post-Pilot Evidence Refresh

### Status

Evidence and documentation refresh completed; Q24 remains `needs_review`.

### Notes

- Inspected `D:\Projects\Eureka\eureka` read-only and found
  `EUREKA-AIDE-PILOT-01` at `needs_review` with a 948 approximate-token task
  packet versus a 68,647 approximate-token baseline.
- Inspected `D:\Projects\Dominium\dominium` read-only and found
  `DOMINIUM-AIDE-PILOT-01` at `needs_review` with a 1,087 approximate-token
  task packet versus a 110,115 approximate-token doctrine-heavy baseline.
- Updated Q24 evidence and compact root docs to stop saying target-pilot
  evidence is absent.
- Did not change adapter compiler code, templates, targets, generated root/tool
  outputs, Gateway/provider behavior, or any Eureka/Dominium file.

## Work Item: Q25 Importer Scope And State Truth Repair

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q25-importer-scope-and-state-truth-repair/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/import/**`
- `.aide/policies/export-import.yaml`
- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- root docs and `docs/reference/cross-repo-pack-export-import.md`

### Rationale

The cross-repo readiness audit showed that AIDE had real target-pilot
token-reduction evidence, but broad handoff was blocked by pack-status failure,
stale pack provenance, an importer that planned optional broad roots by
default, and state surfaces that still pointed at QFIX/Q21-era next work.

### Implementation Notes

- Changed pack checksums to cover payload and static pack docs while excluding
  mutable `manifest.yaml`, `checksums.json`, and `export-report.md` metadata.
- Regenerated `.aide/export/aide-lite-pack-v0/` so `pack-status` passes.
- Made `import-pack` default to safe mode, report exact dry-run planned writes,
  skip optional broad `core/` and `docs/` roots by default, and keep `--mode
  full` explicit for reviewed local fixtures.
- Preserved manual `AGENTS.md` merge behavior and target-specific profile or
  memory template generation.
- Refreshed `.aide/profile.yaml`, command catalog truth, and Harness
  self-check guidance so Q25 review or Q26 handover is now recommended instead
  of stale QFIX-02/Q21 followups.
- Generated the Q26 Eureka Pilot Review And Handover task packet.

### Verification

Q25 validation covers AIDE Lite export/import tests, canonical AIDE Lite test,
export-pack regeneration, pack-status, import-pack dry-run/write into temporary
fixtures, imported fixture doctor/snapshot/index/pack, Harness
validate/doctor/self-check, Harness/Compatibility/Gateway/Provider tests,
`git diff --check`, `.aide.local/` ignore verification, and targeted secret
scan. Detailed command output is recorded in
`.aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/validation.md`.

### Remaining Issues

- Q25 itself requires review before Q26 Eureka handover.
- Fixture import proves the safer importer behavior but does not replace target
  pilot review.
- Dominium-specific golden tasks, exact tokenizer/provider billing, live
  Gateway/provider runtime, and broad adapter-output target-tool usage evidence
  remain future work.

## Work Item: Q25 Fix-Forward Pack Integrity Revalidation

### Status

Implemented and awaiting review as part of Q25.

### Notes

- Added the missing documentation-only `.aide.local.example/secrets/README.md`
  required by the Q18 local-state validation surface.
- Kept real `secrets/**` ignored while adding a narrow `.gitignore` exception
  only for `.aide.local.example/secrets/README.md`.
- Tightened `validate_pack_checksums` so `pack-status` fails if a payload file
  exists in the export pack without a checksum entry.
- Added tests for unchecksummed payload detection and for exporting the safe
  local-state secrets README.
- Regenerated `.aide/export/aide-lite-pack-v0/`; the pack now reports 123
  included files, 126 checksums, and `pack-status` passes.
- Re-ran safe import dry-run/write fixtures; safe mode planned/wrote 106 files,
  skipped optional broad roots, preserved manual `AGENTS.md`, imported the safe
  secrets README, and did not copy `core/` or `docs/`.

### Verification

Final verification used
`C:\Program Files\Hybrid\64bit\Vapoursynth\python.exe` (Python 3.12.9).
AIDE Lite validate/test, export-pack, pack-status, import fixtures,
`.aide/scripts/tests` discovery, Harness/Compatibility/Gateway/Provider tests,
Q26 task-packet generation, diff check, ignore checks, and targeted secret
scans passed. The later Q26 handover refresh regenerated the Harness
generated manifest; remaining Harness warnings are review gates rather than
Q25 pack/import blockers.

## Work Item: Q26 Eureka Pilot Review And Handover

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q26-eureka-pilot-review-and-handover/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/**`
- `.aide/queue/Q28-git-workflow-policy-v0/**`
- `.aide/queue/Q29-merge-land-promote-helper-v0/**`
- `.aide/profile.yaml`
- `core/harness/commands.py`
- `.aide/context/latest-task-packet.md`
- `.aide/generated/manifest.yaml`
- root docs

### Rationale

After Q25 repaired pack integrity, provenance, and safe import scope, AIDE still
had no explicit Q26 review packet and still showed Q27-Q29 as active blockers
from the pre-repair state. Q26 records the Eureka pilot handover checkpoint and
clears those stale active blockers without pretending Q27-Q29 are implemented.

### Implementation Notes

- Added the Q26 queue packet, evidence, status, prompt, and ExecPlan.
- Reviewed the sibling Eureka repository read-only and recorded current pilot
  evidence and validation posture.
- Marked earlier Q27, Q28, and Q29 blocked attempts as superseded redo records.
- Updated profile and self-check guidance so the next sequence is Q25 review,
  Q26 review, then Q27 Commit Discipline And WorkUnit Recovery v0 redo.
- Regenerated the latest task packet for Q27 redo.
- Refreshed the generated manifest after source-truth changes.

### Verification

Q26 validation covers AIDE Harness validate/doctor/self-check, AIDE Lite
validate/test/pack-status, read-only Eureka doctor/validate/task estimate,
Eureka diff and architecture checks, diff check, `.aide.local/` ignore checks,
and targeted secret scans. Detailed command output is recorded in
`.aide/queue/Q26-eureka-pilot-review-and-handover/evidence/validation.md`.

### Remaining Issues

- Q25 and Q26 require review before their outputs are accepted.
- Q27, Q28, and Q29 are not implemented; their old blocked attempts are only
  superseded so they can be redone from the repaired baseline.
- Eureka and Dominium target-pilot evidence remains target-repo evidence and is
  not a broad product-readiness claim.
- Exact tokenizer/provider billing, live provider/model execution, branch
  workflow helpers, and CI enforcement remain future work.

## Work Item: Q25 Pack Provenance Revalidation

### Status

Implemented as a Q25 fix-forward and awaiting Q25 review with the rest of the
repair packet.

### Changed Paths

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/**`
- `docs/reference/cross-repo-pack-export-import.md`

### Rationale

Repeated Q25 validation confirmed that checksum validation was coherent, but
`pack-status` still needed an explicit provenance guard. A stale clean
`manifest.yaml` must fail instead of being accepted merely because mutable
metadata is excluded from payload checksums.

### Implementation Notes

- Added manifest scalar parsing and pack provenance validation to AIDE Lite.
- Included provenance status in `validate` and `pack-status`.
- Treated explicit dirty-source provenance as reportable and non-failing while
  failing stale clean provenance, missing fields, and malformed dirty-state
  values.
- Regenerated the export pack so target imports receive the hardened checker.
- Recorded the new convention in Q25 evidence and the cross-repo import
  reference.

### Verification

Targeted export/import tests, full `.aide/scripts/tests` discovery, AIDE Lite
validate/test/pack-status, Harness validate/doctor/self-check, Harness,
Compatibility, Gateway, and Provider unit suites, regenerated safe-import
fixture smoke, diff check, ignore checks, and targeted secret scans passed.

## Work Item: X-OS-02 Capability Reality Ledger v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/X-OS-02-capability-reality-ledger-v0/**`
- `.aide/capabilities/**`
- `.aide/policies/capability-reality.yaml`
- `.aide/ledgers/capability-ledger.schema.json`
- `.aide/examples/task-os/capability-ledger.example.json`
- `.aide/scripts/aide_lite.py`
- `.aide/evals/golden-tasks/**`
- `.aide/reports/capability-*`
- `docs/reference/capability-reality-ledger.md`
- `docs/reference/task-os-v0.md`
- `docs/reference/task-os-report-only-commands.md`
- root planning/documentation files

### Rationale

Task OS needs a concrete report-only way to distinguish planned, specified, stubbed, implemented, tested, exposed, documented, deprecated, removed, and unknown capability claims before checkpoint or apply-capable work. The ledger prevents docs, fixtures, dry-runs, release drafts, no-call metadata, source-generated reports, and target-specific notes from being overclaimed as live behavior.

### Implementation Notes

- Added controlled capability seed records and observation/overclaim schemas.
- Extended the capability reality policy and capability ledger schema.
- Added AIDE Lite `capability status`, `scan`, `ledger`, `overclaim-report`, and `validate` commands.
- Added validation hooks and six capability golden task definitions/runners.
- Added reference documentation and index updates.

### Verification

AIDE Lite capability commands, targeted X-OS-02 tests, six capability golden tasks, full AIDE Lite validate/test/selftest/eval, raw unittest discovery, export-pack, pack-status, verifier, review-pack, route explain, Harness validate, diff check, and targeted secret scan passed or passed with the warning classifications recorded in `.aide/queue/X-OS-02-capability-reality-ledger-v0/evidence/validation.md`.

## Work Item: AIDE-BUILD-TESTJOB-SCHEMA-01 Minimal TestJob Schema

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/protocol/aide-test-job.schema.json`
- `core/protocol/test_job.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_test_job_schema.py`
- `.aide/reports/test-job/**`
- `.aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- root planning/documentation files

### Rationale

After WorkerRun was accepted as metadata-only, AIDE needed a separate protocol object for validation/test/check attempts before any Test Broker runtime or worker execution work.

### Implementation Notes

- Added an envelope-backed TestJob schema with compatibility metadata, command/environment/framework/timeout metadata, artifact/log refs, evidence refs, failure-summary placeholders, retry/flake placeholders, and explicit non-capabilities.
- Added deterministic TestJob helper functions for build, validation, schema alignment, additive projection, status reports, and validation reports.
- Added thin AIDE Lite `test-job status`, `project --source accepted-artifacts`, and `validate` dispatch.
- Added focused TestJob tests.
- Generated 9 metadata-only TestJob projections from accepted validation/check/acceptance artifacts.

### Verification

Focused TestJob tests, schema parsing, Python compile checks, `test-job status/project/validate`, predecessor validation commands, task evidence checks, boundary scans, secret scans, and diff checks are recorded in `.aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/evidence/validation.md`.

### Remaining Issues

- Full Draft 2020-12 JSON Schema validation remains deferred.
- TestJob is metadata-only; Test Broker runtime and async execution are not implemented.
- Worker execution, scheduler, leases, providers, Service, Commander, Gateway, network, GitHub mutation, branch/worktree automation, target apply, release, and promotion remain future work.

## Work Item: AIDE-BUILD-RECONCILER-REPORTS-01 Report-Only Reconciler Reports

### Status

Implemented and awaiting review.

### Changed Paths

- `core/reconciler/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_reconciler_reports.py`
- `.aide/reports/reconciler/**`
- `.aide/queue/AIDE-BUILD-RECONCILER-REPORTS-01/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

After OKF acceptance, AIDE needs a deterministic way to detect drift between queue truth, generated context, protocol reports, ReferenceID/EventRecord projections, OKF pages, evidence, and capability claims before building declarative capability admission surfaces.

### Implementation Notes

- Added `core/reconciler/reconciler_reports.py` as a report-only detector and report writer.
- Added finding taxonomy and JSON/Markdown reports under `.aide/reports/reconciler/`.
- Added thin AIDE Lite `reconciler status`, `reconciler report`, and `reconciler validate` commands.
- Added focused tests for findings, taxonomy, CLI dispatch, report-only boundaries, JSON output, and parser rejection of repair/runtime subcommands.

### Verification

Focused Reconciler tests, Python compile checks, Reconciler CLI status/report/validate, JSON parsing, predecessor validators, task inspect/evidence, broad validation, and diff checks are recorded in `.aide/queue/AIDE-BUILD-RECONCILER-REPORTS-01/evidence/validation.md`.

### Remaining Issues

- The Reconciler reports existing stale context, stale OKF build routing, acceptance gate debt, and OKF source-hash gaps as warnings only.
- Drift repair, source truth mutation, OKF refresh, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime services, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, and promotion remain deferred.

## Work Item: AIDE-CHECK-RECONCILER-REPORTS-01 Check Report-Only Reconciler Reports

### Status

Check completed and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/**`
- `.aide/reports/reconciler-check/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

The report-only Reconciler build needs an independent check gate before acceptance. The check verifies that the slice detects drift deterministically, keeps all findings warning-class/report-only, preserves predecessor artifact authority, and does not overclaim repair or runtime capabilities.

### Implementation Notes

- Added a check queue item, ExecPlan, prompt, status file, and task-local evidence.
- Added aggregate check reports under `.aide/reports/reconciler-check/`.
- Recorded `PASS_WITH_WARNINGS`, preserved the check-only and no-implementation-authority boundary, and recommended `AIDE-ACCEPT-RECONCILER-REPORTS-01`.
- Restored validation-generated report churn outside the check deliverable.

### Verification

Reconciler CLI status/report/validate, focused Reconciler tests, Python compile checks, JSON parsing, predecessor validators, task inspect/evidence checks, broad validation, Git diff checks, and commit policy checks are recorded in `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/evidence/validation.md`.

### Remaining Issues

- This check does not accept the Reconciler build.
- Stale latest-task-packet drift, acceptance gate debt, stale generated OKF routing, and OKF source-hash gaps remain warning-class and unresolved.
- Drift repair, source truth mutation, OKF refresh, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime services, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, and promotion remain deferred.

## Work Item: AIDE-ACCEPT-RECONCILER-REPORTS-01 Acceptance Review For Report-Only AIDE Reconciler

### Status

Accepted with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/**`
- `.aide/reports/reconciler-accept/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

The Reconciler build and independent check both completed with non-blocking warnings. A separate acceptance gate records that the repository now admits only the narrow `minimal_reconciler_reports` capability before moving to CapabilityManifest work.

### Implementation Notes

- Added the acceptance queue packet, status, ExecPlan, prompt, and evidence files.
- Added aggregate acceptance reports under `.aide/reports/reconciler-accept/`.
- Recorded `ACCEPTED_WITH_WARNINGS`, classified all known Reconciler warnings as non-blocking, and preserved explicit non-capabilities.
- Generated the next prompt for `AIDE-BUILD-CAPABILITY-MANIFEST-01`.

### Verification

Acceptance JSON parsing, task inspect/evidence checks, Reconciler status/validate, predecessor validators, broad validation, Git diff checks, and commit policy checks are recorded in `.aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/evidence/test-and-validation-review.md`.

### Remaining Issues

- Stale latest-task-packet drift, acceptance gate debt, stale OKF build report routing, and OKF source-hash gaps remain warning-class and unresolved.
- CapabilityManifest is selected as next work but is not implemented here.
- ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime services, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, and promotion remain deferred.

## Work Item: AIDE-BUILD-CAPABILITY-MANIFEST-01 Build Minimal CapabilityManifest

### Status

Implemented with warnings and awaiting review.

### Changed Paths

- `.aide/protocol/aide-capability-manifest.schema.json`
- `core/protocol/capability_manifest.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_capability_manifest.py`
- `.aide/reports/capability-manifest/**`
- `.aide/queue/AIDE-BUILD-CAPABILITY-MANIFEST-01/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

After Reconciler acceptance, AIDE needs a durable declaration surface that
summarizes the accepted protocol/report capabilities without turning those
declarations into conformance proof, admission, or execution authority.

### Implementation Notes

- Added an envelope-shaped CapabilityManifest schema.
- Added a deterministic helper that projects 11 accepted capabilities and
  preserves accepted-with-warnings plus metadata/report/projection/runtime and
  mutating semantics.
- Added thin AIDE Lite `capability-manifest status`, `project`, and `validate`
  commands.
- Added focused tests for schema, reports, refs, CLI dispatch, status flags,
  conformance placeholders, future non-acceptance, and overclaiming boundaries.

### Verification

Focused CapabilityManifest tests, Python compile checks, CapabilityManifest CLI
status/project/validate, JSON parsing, predecessor validators, task
inspect/evidence, broad validation, and diff checks are recorded in
`.aide/queue/AIDE-BUILD-CAPABILITY-MANIFEST-01/evidence/validation.md`.

### Remaining Issues

- CapabilityManifest declares capability state but does not prove conformance.
- ConformanceProfile, ConformanceResult, admission, adapter execution, runtime
  registry, PatchTransaction, AdapterManifest, ContextPack v2, provider/model
  calls, network/Gateway/GitHub behavior, branch/worktree automation, target
  apply, active apply, release, and production readiness remain deferred.
- Stale latest-task-packet drift and OKF source-hash drift remain warning-class
  Reconciler findings.

## Work Item: AIDE-CHECK-CAPABILITY-MANIFEST-01 Independent Check For Minimal CapabilityManifest

### Status

Checked with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/**`
- `.aide/reports/capability-manifest-check/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

The CapabilityManifest build completed with warnings. A separate check gate
verifies that the slice declares capability state only and does not imply
conformance, admission, execution, runtime authority, or production readiness.

### Implementation Notes

- Added a check queue item, ExecPlan, prompt, status file, and task-local
  evidence.
- Added aggregate check reports under `.aide/reports/capability-manifest-check/`.
- Recorded `PASS_WITH_WARNINGS`, preserved the check-only and
  no-implementation-authority boundary, and recommended
  `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`.
- Restored validation-generated report churn outside the check deliverable
  before writing check artifacts.

### Verification

CapabilityManifest CLI status/project/validate, focused CapabilityManifest
tests, Python compile checks, JSON parsing, predecessor validators, task
inspect/evidence checks, broad validation, Git diff checks, and commit policy
checks are recorded in
`.aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/evidence/validation.md`.

### Remaining Issues

- This check does not accept the CapabilityManifest build.
- CapabilityManifest declares capability state but does not prove conformance.
- ConformanceProfile, ConformanceResult, conformance admission, adapter
  admission, adapter execution, capability execution, runtime registry,
  PatchTransaction, AdapterManifest, ContextPack v2, provider/model calls,
  network/Gateway/GitHub behavior, branch/worktree automation, target apply,
  active apply, release, and production readiness remain deferred.
- Stale latest-task-packet drift and OKF source-hash drift remain warning-class
  Reconciler findings.

## Work Item: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/structure-current-state.*`
- `.aide/roots/latest-root-authority-candidates.*`
- `docs/planning/repository-structure/**`
- generated repo/root/refactor/status reports
- root planning/execution files

### Rationale

The 2026-06-17 structure note and live AIDE doctrine both point away from an
immediate file shuffle. The next safe step is a bounded current-truth audit that
uses existing repo/root/refactor report-only machinery and records root
authority candidates before any future move map or source-truth change.

### Implementation Notes

- Added the queue packet, ExecPlan, prompt, initial status, and initial scope
  evidence.
- Marked the task `check_only`, `report_only`, and
  `authorizes_implementation: false`.
- Refreshed repo intelligence, root recycling, refactor map, Task OS, Git plan,
  and Reconciler report-only surfaces.
- Wrote current-state and root authority candidate reports plus a planning note.
- Forbid file moves, deletes, reference rewrites, new top-level root creation,
  source-truth mutation, branch mutation, target-repo mutation, GitHub mutation,
  release work, provider/model calls, and network calls.

### Verification

Doctor, broad validation, task pack, Git plan, Task OS status, repo
inventory/status/validate, roots inventory/classify/plan/status/validate,
refactor status/map-status/validate-map, Reconciler status/report/validate, and
task evidence checks are recorded in the task-local evidence.

### Remaining Issues

- Root authority contracts are not written yet.
- README, OKF, generated context, and some historical task metadata still have
  stale status or next-task wording.
- No future structural moves, root creation, docs repair, OKF refresh, or root
  contract changes are authorized by this audit.

## Work Item: AIDE-STRUCTURE-01-root-authority-contracts

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/root-authority.yaml`
- `.aide/reports/root-authority-contracts.*`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

Track B needs explicit root authority before any structural migration. The
previous audit identified root candidates and overlap risks; this task records
the contract layer that future status sync, fate maps, interop policy, and
root-plan tasks can use.

### Implementation Notes

- Added a queue packet, ExecPlan, prompt, status file, and task-local evidence.
- Added a machine-readable root authority policy.
- Added a human-readable root authority governance note.
- Added a repository layout reference with a closed root model, overlap report,
  candidate target structure, migration rules, validation plan, and follow-up
  prompts.
- Added root-authority contract reports.
- Preserved no-apply boundaries for file moves, deletes, reference rewrites,
  aliases, shims, new top-level roots, generated-output source-truth promotion,
  branch mutation, target-repo mutation, provider/model calls, network calls,
  release work, and Track A protocol feature implementation.

### Verification

Doctor, broad validation, Task OS status, task inspect/evidence, diff checks,
and commit policy checks are recorded in the task-local evidence.

### Remaining Issues

- This task creates reviewable root contracts; it does not accept them beyond
  the local `needs_review` queue gate.
- Status/docs drift, OKF refresh, and stale README wording remain for
  `AIDE-STRUCTURE-02-status-doc-sync`.
- `shared`, `platforms`, `research`, `specs`, `.agents`, `.codex`, and
  add-only root candidates still need separate Track B tasks before movement or
  expansion.

## Work Item: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/repo-layout/**`
- `docs/planning/repository-structure/repo-layout-inventory.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

Track B needs concrete layout evidence before any rationalization prompt. This
task records current `.aide` and `core` pressure points, especially
`.aide/reports` path assumptions, without applying migration.

### Implementation Notes

- Added a report-only queue packet, ExecPlan, prompt, status, and evidence.
- Added layout inventory, recommendations, and migration-risk reports under
  `.aide/reports/repo-layout/`.
- Recorded duplicate naming between `.aide`, `core`, and top-level roots.
- Recorded `.aide/reports` top-level files, report directories, mixed lifecycle
  suffixes, and flat report path assumption counts.
- Did not generate a rationalization/apply prompt because design review has not
  accepted the inventory.

### Verification

Doctor, broad validation, repo/roots/refactor status commands, Task OS status,
task inspect/evidence, JSON parsing, diff checks, and commit policy checks are
recorded in the task-local evidence.

### Remaining Issues

- `.aide/reports` remains flat and mixed by design until a report index and
  no-apply reference map exist.
- `core/runtime`, `core/sdk`, and `core/control` are tiny stubs and must not
  grow without explicit queue authority.
- Tracked `.aide/tmp` files need a fate decision before naming cleanup.
- Future rationalization still requires check and acceptance gates.

## Work Item: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/self-management.yaml`
- `.aide/reports/self-management/**`
- `docs/reference/aide-self-management.md`
- `docs/planning/repository-structure/self-management-charter.md`
- `governance/root-authority.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

AIDE needs an explicit self-management doctrine before Track B turns structure,
knowledge, docs, queue, evidence, generated-output, and migration-safety
findings into future protocol objects or apply-capable work.

### Implementation Notes

- Added a policy-and-docs queue packet, ExecPlan, prompt, status, and evidence.
- Added `.aide/policies/self-management.yaml`.
- Added `docs/reference/aide-self-management.md`.
- Added self-management charter, object-backlog, and queue-sequence reports.
- Added a root-authority note linking self-management doctrine.
- Kept `AIDE_SELF_PROFILE` as proposed doctrine; `.aide/profile.yaml` was not
  mutated.

### Verification

Doctor, broad validation, Task OS status, task inspect/evidence, JSON parsing,
diff checks, and commit policy checks are recorded in task-local evidence.

### Remaining Issues

- RootAuthorityManifest, RepoLayoutInventory protocol shape,
  DocTruthReconciler, OKF drift reports, GeneratedOutputLedger,
  QueueHealthReport, StructureTransaction, and CLI commands remain future queue
  work.
- No generated outputs were refreshed or promoted.
- No filesystem mutation, queue acceptance, branch mutation, target mutation,
  runtime/provider behavior, or release work is authorized.

## Work Item: AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/self-management/check-self-management-charter.md`
- `.aide/reports/self-management/check-self-management-charter.json`
- `.aide/reports/self-management/check-self-management-charter.findings.json`
- `.aide/reports/task-os-*`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The self-management charter is foundational Track B law. It needs an
independent check before acceptance, and this check provides the first reusable
Track B governance-check pattern without formalizing a protocol schema or CLI.

### Implementation Notes

- Added a check-only queue packet, ExecPlan, prompt, status, and evidence.
- Added Markdown and JSON self-management check reports.
- Added GovernanceFinding-shaped findings JSON as a report convention only.
- Verified charter consistency, boundaries, evidence completeness, validation
  posture, dirty-state classification, and next-task routing.
- Recommended `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01` next.

### Verification

Doctor, broad validation, task inspect/evidence, JSON/YAML parsing,
GovernanceFinding JSON parsing, Markdown/JSON finding agreement, diff checks,
and commit policy checks are recorded in task-local evidence.

### Remaining Issues

- GovernanceFinding remains a report convention only; no schema, helper,
  library, or CLI command was implemented.
- Documentation truth, OKF drift, generated-output ledger, queue health,
  evidence lifecycle, schema lifecycle, tools/scripts, tests/fixtures/evals,
  and safety/secrets remain future report-only surfaces.
- The `.aide/queue/index.yaml` line-ending warning remains tracked as
  pre-existing/mixed-EOL hygiene, not a charter authority failure.

## Work Item: AIDE-ACCEPT-CAPABILITY-MANIFEST-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/**`
- `.aide/reports/capability-manifest-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Track B B1 is complete and explicitly routes back to Track A. The live queue
recommended `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`, but the acceptance task
surfaces were missing. This task materializes the missing acceptance packet,
accepts only the declaration-only CapabilityManifest capability, and routes
next work to ConformanceProfile.

### Implementation Notes

- Added the acceptance queue packet, ExecPlan, prompt, status, and evidence.
- Added acceptance JSON and Markdown reports.
- Classified all CapabilityManifest warnings as non-blocking or deferred.
- Preserved the boundary that CapabilityManifest declares capability state but
  does not prove conformance, admit adapters, execute capabilities, or authorize
  runtime behavior.
- Generated the first Track A prompt batch without executing the
  ConformanceProfile tasks.

### Verification

Acceptance JSON parsing, predecessor CapabilityManifest JSON parsing, focused
CapabilityManifest tests, CapabilityManifest CLI status/project/validate, task
inspect/evidence checks, predecessor validators, broad validation, diff checks,
and commit policy checks are recorded in task-local evidence.

### Remaining Issues

- ConformanceProfile and ConformanceResult remain future work.
- PatchTransaction, AdapterManifest, ContextPack v2, runtime, workers,
  provider/model/network/Gateway/GitHub behavior, branch/worktree automation,
  target apply, active apply, release, and production readiness remain
  deferred.
- Generated latest-task-packet drift remains warning-class debt; queue truth
  remains canonical.

## Work Item: AIDE-BUILD-MCP-SERVER-CONTRACT-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/protocol/aide-mcp-server-contract.schema.json`
- `core/interop/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_mcp_server_contract.py`
- `.aide/interop/mcp/**`
- `.aide/reports/mcp-server-contract/**`
- `.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-01/**`
- `.aide/queue/index.yaml`
- root planning/execution files

### Rationale

After static interop export preview acceptance, the next serialized queue task
requires a bounded MCP server contract projection. The slice records how a
future MCP server may project selected AIDE resources, tools, prompts, refusals,
transport expectations, authorization expectations, and conformance
expectations without making MCP a live runtime or AIDE authority.

### Implementation Notes

- Added an envelope-shaped MCP server contract schema.
- Added `core/interop/mcp_server_contract.py` to project deterministic contract,
  catalogue, JSON-RPC fixture, refusal, transport, authorization, conformance,
  and report artifacts.
- Added thin AIDE Lite `mcp-server-contract status/project/validate` dispatch.
- Added focused tests for protocol version pinning, JSON-RPC fixtures,
  catalogue validation, read-only tool boundaries, refusal mapping, transport
  and authorization non-implementation, deterministic projection, source
  immutability, unsupported command rejection, and explicit non-capabilities.
- Preserved the warning that the future `aide://interop/...` ReferenceID kind is
  advisory only; global ReferenceID authority was not broadened.

### Verification

Python compile checks, focused MCP contract tests, MCP contract
status/project/validate, predecessor validators, task inspect/evidence, broad
validation, JSON parsing, deterministic projection checks, source immutability
checks, unsupported command probes, secret-like scans, diff checks, and commit
policy checks are recorded in
`.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-01/evidence/validation.md`.

### Remaining Issues

- MCP remains contract-only and projection-only.
- Live MCP server, stdio/HTTP transport, endpoint binding, sessions,
  authentication, OAuth, credential handling, resource serving, prompt serving,
  tool execution, client roots, sampling, elicitation, adapter/worker/runtime
  execution, provider/model/network/Gateway/GitHub behavior, PatchTransaction
  apply, target mutation, branch/worktree automation, A2A, Host Contract,
  Dominium Bridge, Workbench, release, promotion, and production readiness
  remain deferred.

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/reports/dominium-readonly-seam-v0-repair/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The independent seam check found 18 bounded material defects. This repair fixes
those defects inside the existing offline read-only seam rather than advancing
to acceptance or implementing downstream runtime behavior.

### Implementation Notes

- Added exact repository identity parsing and rejection for lookalike remotes.
- Added shared integrity helpers for source snapshot, record, projection-index,
  and bundle self-digest finalization.
- Preserved bounded diagnostic/refusal registry projection while disclosing
  native counts, projected counts, omitted counts, and omitted-ID digests.
- Tightened the public schema and semantic validator for record cardinality,
  required fields, source revision binding, reference closure, semantic owners,
  read-only capability boundaries, event ordering, and native
  diagnostic/refusal registry alignment.
- Replaced compact negative fixture descriptions with replayable JSON-pointer
  operation fixtures.
- Made conformance checks expectation-specific instead of aggregate validation
  propagation.
- Made demo timing truthful and added a read-only operation observation ledger.
- Added a focused repair regression suite covering the material findings.

### Verification

Python compile, the original seam test suite, repair regression tests, live seam
demo, live seam validation, and Dominium immutability checks passed during the
repair. Final diff, broad validation, task evidence, secret scan, and commit
policy checks are recorded in the repair task evidence.

### Remaining Issues

- The seam remains offline and read-only.
- SeamBundle remains generated projection evidence, not canonical Dominium
  truth.
- Local Dominium remains clean but behind `origin/main` by 24 commits.
- Host runtime, Host SDK, Workbench, bridge runtime, service, transport,
  provider/model/network calls, worker execution, preview/apply/rollback, and
  mutation remain absent.
- Independent repair check is still required before acceptance.

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair_02.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-02/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The independent Repair 01 check left ten targeted material gaps. This second
repair fixes those gaps without changing the seam's authority boundary or
advancing to the independent check/acceptance gate.

### Implementation Notes

- Added full diagnostic/refusal registry provenance disclosure, including
  source path, digest, Git object metadata, source revision, projected IDs,
  omitted IDs, and truncation disclosure.
- Replaced the loose public seam schema record references with kind-specific
  record/spec definitions and false-boundary status constraints.
- Hardened replayable negative fixtures so expected error codes must all be
  observed and executable fixture operations are refused.
- Added assertion-level conformance evidence and preserved aggregate-only
  conformance as `NOT_PROVEN`.
- Extended the demo operation ledger with allowed operation counts, required
  operation families, family descriptions, and instrumentation methods.
- Added a runtime dependency manifest and isolated cross-process CLI
  portability proof.
- Updated the CLI validate path to validate an existing bundle instead of
  rerunning the full projection when reports already exist.

### Verification

Python compilation, base seam tests, Repair 01 regression tests, Repair 02
regression tests, live seam project/validate/diff/demo, portability proof,
Dominium immutability checks, JSON parsing, task evidence checks, broad
validation, secret-like scan, diff checks, and commit policy checks are
recorded in the Repair 02 evidence.

### Remaining Issues

- The seam remains offline and read-only.
- Local Dominium remains clean but behind `origin/main` by 24 commits.
- Independent Repair 02 check is still required before acceptance.
- Runtime, Workbench, bridge runtime, service, transport, provider/model/network
  calls, worker execution, preview/apply/rollback, and mutation remain absent.

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

### Status

Completed as a check-only task and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-02-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 02 required a final independent verification before acceptance. The
check keeps historical evidence intact and does not repair or rewrite the seam.

### Implementation Notes

- Added a task-local independent check harness and consolidated reports.
- Classified `14` material finding(s), preserving the check-only
  boundary.
- Recommended exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.

### Verification

The task evidence records the independent harness outputs, focused tests,
Dominium immutability comparison, broad validation, diff checks, secret scan,
and commit policy check.

### Remaining Issues

- Repair 02 is not accepted.
- A bounded Repair 03 is required before another acceptance attempt.
- The seam remains offline and read-only; runtime, Workbench, bridge runtime,
  service, transport, provider/model/network calls, worker execution,
  preview/apply/rollback, and mutation remain absent.

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

### Status

Completed with warnings and awaiting independent review.

### Changed Paths

- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/**`
- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair_03.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-03/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The live Repair 02 check recorded `REQUEST_CHANGES` with 15 material findings and recommended exactly this repair task. The task scaffold exists so implementation, validation, and evidence can proceed through the filesystem queue rather than from chat-only instructions.

### Implementation Notes

- Created the task packet, ExecPlan, prompt, and baseline evidence.
- Registered the task in `.aide/queue/index.yaml`.
- Hardened public schema typing, false-boundary status fields, and extension rejection for authority-changing claims.
- Tightened fixture replay semantics for pointer validation, canonical array indexes, add/remove/replace/append behavior, and executable-content rejection.
- Added evidence-bearing conformance output, a complete operation trace, guard-conformance evidence, and richer Git operation classification.
- Made portability manifest-driven, hash-checked, environment-isolated, and validated against import-closure and local-path leak checks.
- Extended typed unsupported-operation refusals across the read-only seam CLI surface and regenerated seam artifacts/reports.
- Preserved the explicit stop point: `needs_review`, with `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` as the only next recommendation.

### Verification

The task evidence records Python compilation, the base seam suite, Repair 01, Repair 02, and Repair 03 focused suites, seam `status/snapshot/project/validate/diff/demo`, unsupported-operation probes, Dominium immutability checks, historical-root preservation, broad validation, secret-like scan, and diff checks.

### Remaining Issues

- Independent Repair 03 check is still required before acceptance.
- Local Dominium remains clean but behind `origin/main` by 24 commits.
- Non-Windows platforms were not separately executed in this turn.
- The seam remains offline and read-only; runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, worker execution, preview/apply/rollback, and mutation remain absent.

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03

### Status

Completed as a bounded check-only task. The result is `REQUEST_CHANGES` at `needs_review`.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-03-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 03 completed with warnings and recommends this independent check. The check must remain adversarial and cannot use the Repair 03 disposition report as its own proof.

### Implementation Notes

- Created the check task packet, ExecPlan, prompt, and baseline evidence.
- Registered the check in `.aide/queue/index.yaml`.
- Preserved the strict check-only boundary and the two possible serialized next tasks: acceptance if no material defects remain, or Repair 04 if any material defect remains.
- Added independent task-local harnesses and reports for source-chain, schema, fixture replay, conformance, operation trace, guard probes, runtime manifest, portability, typed refusal, and Dominium immutability checks.
- Recorded 12 material assertions and selected `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` as the only next task.

### Verification

Validation ran through diff checks, commit resolution, compileall, seam unittest discovery, seam CLI commands, independent Repair 03 check harness, task inspect/evidence, broad validation, secret-like scan, and commit policy check. The independent harness intentionally returned `REQUEST_CHANGES` because material findings remain.

### Remaining Issues

- Repair 03 is not accepted.
- Repair 04 remains the selected next task and was not started.

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

### Status

Completed with warnings and awaiting independent review.

### Changed Paths

- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/**`
- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam_repair_04.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-04/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The live Repair 03 check recorded `REQUEST_CHANGES` with 12 material findings and recommended exactly this repair task. The task remains a bounded repair and does not accept the seam.

### Implementation Notes

- Created the Repair 04 task packet, ExecPlan, prompt, status, and evidence root.
- Added a `SeamRecord` schema union, bounded extension values, and validation refusal for nested authority-changing extension keys.
- Tightened fixture replay value requirements, ASCII index parsing, and executable-key rejection.
- Routed unsupported-operation conformance through actual CLI dispatch, including arbitrary unsupported verbs.
- Recorded no-write evidence around actual read-only seam operations and guard evidence through exercised guard probes.
- Made operation aggregation preserve target, classification, source, allowed state, operation family, and observation method.
- Expanded portability comparison to all 16 required outputs, including conformance evidence, operation trace, and operation guard conformance.
- Regenerated current seam artifacts and Repair 04 reports while preserving the explicit `needs_review` stop point and `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` as the only next recommendation.

### Verification

Validation records Python compilation, Repair 04 tests, targeted Repair 03/Repair 02/base seam regression suites, seam project/validate/diff/demo, standalone portability proof, Dominium immutability evidence, historical-root preservation, and task evidence. Full older Repair 02/03 suites were not completed as full-suite commands because their embedded full portability checks exceeded the interactive timeout; targeted non-portability methods plus standalone Repair 04 portability proof passed.

### Remaining Issues

- Independent Repair 04 check is still required before acceptance.
- Non-Windows platforms were not separately executed in this turn.
- The seam remains offline and read-only; runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, worker execution, preview/apply/rollback, and mutation remain absent.

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

### Status

Completed as a bounded check-only task. The result is `REQUEST_CHANGES` at `needs_review`.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-04-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 04 completed with warnings and recommends this independent check. The check remains strict but bounded to the 12 Repair 04 finding closures, sampled prior invariants, report/evidence truthfulness, and no capability expansion.

### Implementation Notes

- Created the check task packet, ExecPlan, prompt, status, and evidence root.
- Registered the check in `.aide/queue/index.yaml`.
- Added a task-local independent harness and reports for source-chain, schema, extension, fixture replay, conformance, guard, operation, portability, typed refusal, regression sampling, and Repair 04 report consistency checks.
- Recorded exactly 12 finding dispositions: 9 `CLOSED` and 3 `OPEN`.
- Recorded 4 material check failures and selected `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05` as the only next task.

### Verification

Validation records diff checks, Repair 04 commit resolution, compileall, the full independent check harness, split seam test modules after combined unittest timeout, explicit live seam `status/snapshot/project/validate/diff/demo`, task inspect/evidence, broad validation, secret-like scan, and commit policy check. The independent harness intentionally returns `REQUEST_CHANGES` because material defects remain.

### Remaining Issues

- Repair 04 is not accepted.
- Material findings remain in schema open-object surfaces, authority-changing extension semantic rejection, exercised guard evidence, and guard-report staticness.
- The first repair unittest module has one stale next-task routing assertion against the current Repair 04 route.
- Repair 05 remains the selected next task and was not started.

## Work Item: AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05

### Status

Completed with warnings and awaiting independent review.

### Changed Paths

- `.aide/protocol/aide-dominium-readonly-seam-v0.schema.json`
- `core/interop/dominium/**`
- `.aide/scripts/tests/test_aide_dominium_readonly_seam*.py`
- `.aide/fixtures/dominium-readonly-seam/**`
- `.aide/interop/dominium/**`
- `.aide/reports/dominium-readonly-seam-v0/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-05/**`
- `.aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The Repair 04 check found exactly four remaining material blockers and recommended this final bounded repair. The repair scope is frozen to those blockers and directly caused regression debt.

### Implementation Notes

- Added a recursive schema surface audit and closed the remaining public schema surface ambiguity by classifying every object as closed canonical, typed dynamic map, or explicit extension container.
- Added deterministic extension-key normalization and semantic authority-change refusal with `extension.authority_change` while preserving legacy `schema.authority_extension` evidence.
- Replaced static guard evidence with a real `GuardRequest` and `dispatch_guarded_request` path using injected executor sentinels, before/after state digests, typed refusals, and nonce-bearing proof.
- Derived operation coverage from actual guard evidence instead of shortcut family status.
- Updated stale next-task routing assertions and added a focused Repair 05 regression test module.
- Regenerated current seam artifacts, fixtures, interop outputs, and Repair 05 reports/evidence.

### Verification

Validation records schema audit, focused Repair 05 and Repair 04 tests, seam `project` and `demo`, and the full final validation matrix in task-local evidence. The task stops at `needs_review` with `PASS_WITH_WARNINGS`.

### Remaining Issues

- Independent Repair 05 check is still required before acceptance.
- Non-Windows platforms were not separately executed.
- Minimum Python 3.11 was not separately executed.
- The seam remains offline and read-only; runtime, Workbench, bridge runtime, service, transport, provider/model/network calls, worker execution, preview/apply/rollback, and mutation remain absent.

## Work Item: AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05

### Status

Completed with warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-05-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 05 completed with warnings and recommends this independent bounded check. The check scope is frozen to the four Repair 05 source findings, critical previously closed invariants, evidence truthfulness, production immutability, Dominium immutability, and next-task routing.

### Implementation Notes

- Created the Repair 05 check task packet, ExecPlan, prompt, status, and evidence root.
- Added an evidence-local independent harness without using the production schema audit helper for expected results.
- Verified schema surfaces with zero unclassified objects and zero unintended open objects.
- Verified 80 authority-changing extension variants fail with `extension.authority_change` and 20 benign variants pass.
- Exercised the actual guard dispatcher for all six forbidden guard families with sentinel executors and nonce-bearing evidence.
- Recomputed guard report counts and digests and verified nonce-sensitive report changes.
- Sampled schema discrimination, fixture strictness, arbitrary unsupported CLI refusal, no-write evidence, raw operation trace auditability, and portability output completeness.
- Recorded production tree hashes before and after check execution.

### Verification

Validation records the independent harness passing with `PASS_WITH_WARNINGS`, zero material findings, all four findings closed, production tree unchanged, Dominium clean, and the acceptance task as the only next recommendation. Final diff, compile, task evidence, broad validation, JSON, secret-like, and commit-policy checks are recorded in task evidence.

### Remaining Issues

- Acceptance has not yet been processed.
- The seam remains offline and read-only.
- The local Dominium checkout remains behind remote `origin/main`.
- Non-Windows platforms and minimum Python 3.11 were not separately executed.

## Work Item: AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01

### Status

Completed with accepted warnings and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01/**`
- `.aide/reports/dominium-readonly-seam-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The final Repair 05 independent check reported `PASS_WITH_WARNINGS`, `material_finding_count: 0`, and `missing_evidence: 0`, satisfying the zero-finding gate for acceptance.

### Implementation Notes

- Created the acceptance task packet, ExecPlan, prompt, status, and evidence root.
- Accepted only `dominium_readonly_seam_v0` as an offline deterministic read-only projection capability.
- Preserved historical failed checks and the full repair lineage.
- Recorded final schema, evidence, portability, safety, test-validation, warning, and non-capability reviews.
- Generated the next WorkUnit validation slice prompt but did not create or begin that task.

### Verification

Validation records final Repair 05 check success, current seam validation and conformance warnings, portability pass, fixture count, demo no-mutation result, Dominium clean state, task inspect/evidence, broad validation, JSON parsing, secret-like scan, diff checks, and commit-policy check.

### Remaining Issues

- The WorkUnit validation slice is not implemented.
- The seam remains offline and read-only.
- Runtime, Workbench, provider/model, worker, mutation, preview/apply, and target-repository behavior remain absent.
- Non-Windows platforms and minimum Python 3.11 were not separately executed.

## Work Item: AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01

### Status

Completed with warnings and awaiting independent review.

### Changed Paths

- `core/execution/local_process_host.py`
- `.aide/fixtures/local-process-execution-host/reference_worker.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_local_process_execution_host.py`
- `.aide/reports/local-process-execution-host/**`
- `.aide/queue/AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The accepted ExecutionHost contract was projection-only. This build adds the
smallest live reference host slice: one exact local reference worker process
launched through the accepted registered-process provider.

### Implementation Notes

- Added `core/execution/local_process_host.py` as a bounded reference
  LocalProcessExecutionHost.
- Added one committed deterministic fixture worker.
- Added AIDE Lite `local-process-execution-host status/run/validate` commands.
- Used `RegisteredProcessExecutionProvider v0` unchanged for shell-free process launch, receipt, outcome, stream summaries, timeout handling, and state probing.
- Generated descriptor, run binding, event, artifact, usage, receipt, outcome, evidence, EventRecord, projection, validation, and human-readable reports.
- Added focused fake-runner tests for exact argv/environment, zero-launch refusals, typed refusals, mutation detection, deterministic projection, and scrubbing.

### Verification

Initial validation passed for focused tests, compile checks, the live bounded
host run, and local host report validation. Final validation is recorded in
task-local evidence before commit.

### Remaining Issues

- Independent check is still required before acceptance.
- The host is a bounded reference fixture only, not a generic worker harness.
- Cancellation, durable idempotency, streaming artifact storage, resource quotas,
  worker leases, scheduler, supervisor, Service/runtime, and Workbench behavior
  remain unimplemented.

## Work Item: AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01

### Status

Completed with `REQUEST_CHANGES` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01/**`
- `.aide/reports/local-process-execution-host-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The source build passed its own tests and broad validation, but the requested
check boundary is stronger than the source proof. It requires disposable
workspace containment, escape guards, event-stream truth, artifact integrity,
lifecycle validation, and no-overclaiming before acceptance can proceed.

### Implementation Notes

- Created the check task packet, ExecPlan, prompt, status, evidence root, and
  check reports.
- Added a task-local independent source-inspection harness that reads source
  task packets and generated reports without importing production
  `core.execution.local_process_host`.
- Recorded six material findings:
  - disposable worker workspace not proven;
  - path traversal, symlink, and reparse-point escape guards not proven;
  - raw event stream and malformed/non-monotonic failure handling not proven;
  - worker artifact path containment and persisted content-addressed artifact
    truth not proven;
  - WorkerRun lifecycle transition validation not proven;
  - advertised supported operations exceed the exercised source proof.
- Stopped the serialized wave before acceptance or later trust/service/MCP work.

### Verification

Validation passed for the source local host tests, registered-process provider
tests, ExecutionHost contract tests, AIDE self-validation adapter tests,
Dominium registered validation backend tests, Eureka readonly process adapter
tests, source task inspect/evidence, local host validation, broad AIDE
validation, diff checks, and path/secret scan of check evidence.

### Remaining Issues

- `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01` is required before
  local process ExecutionHost acceptance.
- The later trust, local Service, durable WorkerRun, and read-only MCP stdio
  phases were not started.

## Work Item: AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting independent repair check.

### Changed Paths

- `core/execution/local_process_host.py`
- `.aide/fixtures/local-process-execution-host/reference_worker.py`
- `.aide/scripts/tests/test_aide_local_process_execution_host.py`
- `.aide/reports/local-process-execution-host/**`
- `.aide/reports/local-process-execution-host-repair-01/**`
- `.aide/queue/AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The independent check found that the source local process host build proved one
process launch but did not materially prove disposable workspace containment,
escape rejection, raw event truth, content-addressed artifact persistence,
WorkerRun lifecycle validation, or an accurately bounded host descriptor.

### Implementation Notes

- Staged the committed reference worker into a disposable temporary workspace
  outside the source checkout before invoking it.
- Changed the fixture output from a single JSON object to an NDJSON event
  stream and added fail-closed event parsing.
- Persisted the raw event stream and declared worker artifact under
  content-addressed report paths.
- Added path containment checks for absolute paths, traversal, symlinks, and
  visible Windows reparse points.
- Added WorkerRun lifecycle transition validation from raw events.
- Narrowed the descriptor to `probe` and `create_run`, with all other
  ExecutionHost operations explicitly unsupported.
- Kept `RegisteredProcessExecutionProvider v0` and the accepted ExecutionHost
  contract unchanged.

### Verification

Initial repair verification passed for compile checks, focused local-host tests,
and one live `aide_lite.py local-process-execution-host run`. Final validation
is recorded in task-local evidence before commit.

### Remaining Issues

- `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01` is required before
  local process ExecutionHost acceptance.
- This remains `local_process_execution_host_fixture_v0`; it is not a generic
  worker harness or Service/runtime implementation.

## Work Item: AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01

### Status

Completed with `REQUEST_CHANGES` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01/**`
- `.aide/reports/local-process-execution-host-repair-01-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The repair build materially improved the fixture host, but acceptance requires
an independent check of the exact six original findings. The check remained
strictly check-only and did not repair implementation.

### Implementation Notes

- Added a check task packet, status, prompt, ExecPlan, and evidence-local
  harness.
- Verified source chain, source result, six repair dispositions, and latest
  repair diff scope.
- Confirmed two source findings are closed: disposable workspace evidence and
  descriptor operation scope.
- Recorded seven material assertions across four open source findings:
  path containment, raw event stream, artifact integrity, and WorkerRun
  lifecycle.
- Stopped the serialized wave before acceptance, trust, Service, durable
  WorkerRun, or MCP work.

### Verification

The evidence-local harness produced `REQUEST_CHANGES` with
`material_finding_count: 7` and `missing_evidence: 0`. Final validation is
recorded in task-local evidence before commit.

### Remaining Issues

- `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02` is required before
  LocalProcessExecutionHost v0 acceptance.

## Work Item: AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01/**`
- `.aide/reports/trust-authorization-contract-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The trust contract build stopped at `needs_review` with projection-only trust
and authorization records. Acceptance requires an independent check of the
authority boundaries, negative refusal matrix, deterministic projections, and
non-capability claims.

### Implementation Notes

- Added a check-only task packet and evidence-local independent harness.
- Reviewed source build status, schema/projection alignment, stable AIDE refs,
  exact digest binding, authority-record separation, scope/delegation bounds,
  revocation/expiry/use-budget fail-closed refusal coverage, and runtime versus
  transaction approval separation.
- Confirmed all live identity, credential, policy engine, live grant, runtime
  enforcement, Service, worker, provider/model, network, mutation, release, and
  promotion flags remain false.
- Preserved projection-only warnings and routed to the acceptance task.

### Verification

The independent harness produced `PASS_WITH_WARNINGS` with 12 passing
assertions, `material_finding_count: 0`, and `missing_evidence: 0`. Focused
trust tests, trust status/validate, compileall, deterministic projection rerun,
and broad validation passed.

### Remaining Issues

- `AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01` is required before the
  trust contract is accepted.
- Live identity, credentials, live policy engine, live grants, runtime
  enforcement, Service/runtime behavior, and transaction approval remain out of
  scope.

## Work Item: AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

### Status

Completed with `ACCEPTED_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01/**`
- `.aide/reports/trust-authorization-contract-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The trust contract build and independent check both reported
`PASS_WITH_WARNINGS`, zero material findings, and complete evidence. This
acceptance consolidates the achieved capability without broadening it into live
enforcement or runtime behavior.

### Implementation Notes

- Added an acceptance task packet, evidence, reports, and an evidence-local
  acceptance review script.
- Accepted exactly `trust_and_authorization_contract_v0` as projection-only.
- Preserved non-capabilities for identity, credentials, OIDC/IAM, live policy
  engine, live grants, runtime enforcement, Service/runtime behavior, worker
  execution, transaction approval, provider/model/network calls, mutation,
  GitHub behavior, release, and promotion.
- Routed next work to `AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01`.

### Verification

The acceptance review script produced `ACCEPTED_WITH_WARNINGS` with zero
material findings and `missing_evidence: 0`. Final task inspect/evidence, trust
validation, broad validation, leak scans, diff checks, and commit-policy check
are recorded in task-local evidence.

### Remaining Issues

- Local Service foundation remains unbuilt and is the next serialized task.
- Runtime enforcement and live trust infrastructure remain future work.

## Work Item: AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `core/service/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_local_service_foundation.py`
- `.aide/reports/local-service-foundation-v0/**`
- `.aide/queue/AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

After accepting projection-only trust contracts, AIDE needs a small durable local
coordination substrate before trust enforcement or durable WorkerRun slices. The
build implements local storage primitives only, without network or runtime
authority expansion.

### Implementation Notes

- Added `core/service` with SQLite migrations, object storage, monotonic events,
  cursor acknowledgments, idempotency records, artifact metadata, and a local
  content-addressed artifact store.
- Added fixture-only `aide_lite.py local-service` commands for status,
  init-fixture, fixture, validate, and reset-fixture.
- Added focused tests for migrations, version conflicts, atomic object/event
  writes, event reads, cursors, idempotency, artifact integrity, persistence,
  corruption refusal, boundary flags, and CLI fixture initialization.
- Generated local-service reports under
  `.aide/reports/local-service-foundation-v0/`.

### Verification

Focused local service tests pass. `local-service init-fixture`, `fixture`,
`status`, and `validate` report `PASS_WITH_WARNINGS`. Final compileall,
regression tests, task inspect/evidence, broad validation, local-state boundary
checks, leak scans, diff checks, and commit-policy validation are recorded in
task-local evidence.

### Remaining Issues

- `AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01` is required before acceptance.
- Service remains local, no-network, single-machine, at-least-once only, and
  does not execute workers or enforce trust.

## Work Item: AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01/**`
- `.aide/reports/local-service-foundation-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The Local Service foundation build stopped at `needs_review` and required an
independent check before acceptance. This task verifies the proposed capability
without modifying production code or source build reports.

### Implementation Notes

- Added a check task packet, check reports, and an evidence-local harness.
- The harness independently exercised fresh temporary SQLite/object/event,
  cursor, idempotency, artifact, persistence, future-migration, corruption, and
  CLI boundary behavior.
- The check preserved no-network, no-worker, no-enforcement, no-MCP,
  no-Workbench, no-provider/model, no-preview/apply, no-mutation boundaries.

### Verification

The independent harness produced `PASS_WITH_WARNINGS`, zero material findings,
and `missing_evidence: 0`. Focused local service tests, public local-service
commands, source/check task inspect and evidence, broad validation, diff checks,
local-state boundary checks, and leak scans are recorded in task-local evidence.

### Remaining Issues

- `AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01` is required before the
  capability is accepted.
- Scheduler, worker execution, capability execution, trust enforcement, MCP,
  Workbench, exactly-once delivery, provider/model calls, preview/apply, and
  rollback remain non-capabilities.

## Work Item: AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01

### Status

Completed with `ACCEPTED_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01/**`
- `.aide/reports/local-service-foundation-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The Local Service foundation build and independent check both passed with
warnings, zero material findings, and complete evidence. This acceptance
consolidates the exact achieved capability without broadening it into runtime
scheduling, enforcement, or interoperability behavior.

### Implementation Notes

- Added an acceptance task packet, evidence, reports, and acceptance review.
- Accepted exactly `local_service_foundation_v0`.
- Preserved explicit non-capabilities for scheduler, worker execution,
  capability execution, authorization enforcement, network API, MCP, Workbench,
  distributed state, exactly-once delivery, provider/model calls,
  preview/apply/rollback, mutation, GitHub behavior, release, and promotion.
- Routed next work to `AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01`.

### Verification

The acceptance review produced `ACCEPTED_WITH_WARNINGS`, zero material findings,
and `missing_evidence: 0`. Final source/check/accept task inspect and evidence,
local-service validation, broad validation, leak scans, diff checks, and
commit-policy check are recorded in task-local evidence.

### Remaining Issues

- Local trust enforcement is the next serialized task.
- Worker execution, scheduling, MCP, Workbench, provider/model calls,
  preview/apply/rollback, and distributed state remain future work.

## Work Item: AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `core/service/local_trust_enforcement.py`
- `core/service/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_local_trust_enforcement.py`
- `.aide/reports/local-trust-enforcement-v0/**`
- `.aide/queue/AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The accepted trust contract is projection-only, and the accepted local Service
does not enforce authorization. This task adds the first deterministic local
enforcement slice by evaluating trust records, persisting the decision, and
consuming a one-use grant through local Service state.

### Implementation Notes

- Added `core/service/local_trust_enforcement.py`.
- Reused `trust_authorization.evaluate_authorization` rather than duplicating
  policy/refusal logic.
- Persisted support records, AuthorizationEvaluation, evaluation event,
  grant-consumption event, and idempotency record in a local SQLite transaction.
- Added AIDE Lite `local-trust status`, `fixture`, `validate`, and
  `reset-fixture` commands.
- Added focused tests for allowed evaluation, idempotent replay, final-use
  exhaustion, refusal matrix coverage, restart persistence, and false
  process/network/worker/provider boundaries.

### Verification

Focused local trust tests pass. `local-trust fixture`, `status`, and
`validate` report `PASS_WITH_WARNINGS`. Final compileall, trust/local-service
regressions, task inspect/evidence, broad validation, local-state boundary
checks, leak scans, diff checks, and commit-policy validation are recorded in
task-local evidence.

### Remaining Issues

- `AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01` is required before acceptance.
- External IAM, credentials, secrets, OIDC, remote policy engines, distributed
  authorization, worker execution, transaction approval, provider/model calls,
  network calls, preview/apply/rollback, and repository mutation remain
  non-capabilities.

## Work Item: AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01/**`
- `.aide/reports/local-trust-enforcement-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The local trust enforcement build proposed the first local enforcement slice
over the accepted trust contracts and accepted local Service foundation. This
check independently verifies that the slice behaves as claimed before any
acceptance task can consolidate the capability.

### Implementation Notes

- Added an independent check task packet and report set.
- Added an evidence-local harness that uses the local-trust module as the
  system under test but directly inspects the resulting SQLite state, event
  rows, idempotency records, refusal matrix, false-boundary fields, CLI output,
  determinism, and source report scrub status.
- Recorded no material findings and routed to acceptance.

### Verification

The independent harness passed with 10 material assertions, zero material
findings, and `missing_evidence: 0`. Final focused tests, broad validation,
task inspect/evidence, diff checks, leak scans, and commit-policy validation
are recorded in task-local evidence.

### Remaining Issues

- `AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01` is required before this proposed
  capability is accepted.
- External IAM, credentials, secrets, OIDC, remote policy engines, process
  launch, worker execution, transaction approval, provider/model calls, network
  calls, preview/apply/rollback, repository mutation, GitHub mutation, release,
  and promotion remain non-capabilities.

## Work Item: AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01

### Status

Completed with `ACCEPTED_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01/**`
- `.aide/reports/local-trust-enforcement-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The local trust enforcement build and independent check both passed with
warnings, zero material findings, and complete evidence. This task consolidates
the exact accepted capability without broadening it into external identity,
worker execution, transaction approval, network behavior, or mutation.

### Implementation Notes

- Added an acceptance task packet, evidence, reports, and accepted boundary.
- Accepted exactly `local_trust_enforcement_v0`.
- Preserved explicit non-capabilities for external IAM, credentials, secrets,
  OIDC, remote policy engines, process launch, worker execution, transaction
  approval, provider/model calls, network calls, preview/apply/rollback,
  repository mutation, GitHub mutation, release, and promotion.
- Routed next work to `AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.

### Verification

Acceptance evidence records `ACCEPTED_WITH_WARNINGS`, zero material findings,
and `missing_evidence: 0`. Final source build/check/accept task inspect and
evidence, local-trust validation, broad validation, scoped leak scans, diff
checks, and commit-policy validation are recorded in task-local evidence.

### Remaining Issues

- Durable local WorkerRun integration is the next serialized build gate.
- External IAM, credentials, secrets, OIDC, remote policy engines, process
  launch, worker execution beyond accepted fixture-host proof, transaction
  approval, provider/model calls, network calls, preview/apply/rollback,
  repository mutation, GitHub mutation, release, and promotion remain future
  work.

## Work Item: AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `core/service/durable_worker_run.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_durable_worker_run_slice.py`
- `.aide/reports/durable-local-worker-run-slice-v0/**`
- `.aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The accepted local Service, local trust enforcement, registered process
provider, and fixture LocalProcessExecutionHost needed one composed vertical
slice that records a WorkerRun observation durably before the system moves
toward broader worker-runtime work.

### Implementation Notes

- Added `core/service/durable_worker_run.py` as a narrow composition layer over
  existing accepted components.
- Added `durable-worker-run status`, `fixture`, `validate`, and
  `reset-fixture` AIDE Lite commands.
- Persisted WorkUnit, WorkerRun, host outcome, EvidencePacket, EventRecord,
  monotonic local Service events, idempotency, and content-addressed artifact
  metadata into temporary local Service state.
- Added focused tests using a fake runner and ran one live fixture command for
  committed reports.
- Routed next work to `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.

### Verification

Focused durable WorkerRun tests, compileall, the live durable-worker-run
fixture and validation commands, and regression checks are recorded in
task-local evidence.

### Remaining Issues

- Independent check and acceptance remain required before
  `durable_local_worker_run_slice_v0` is accepted.
- This remains fixture-backed and local only. It does not implement a general
  worker harness, autonomous AI worker, scheduler, leases, persistent daemon,
  Workbench/MCP runtime, provider/model calls, network calls,
  preview/apply/rollback, transaction approval, repository mutation, GitHub
  mutation, release, or promotion.

## Work Item: AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01

### Status

Completed with `REQUEST_CHANGES` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/**`
- `.aide/reports/durable-local-worker-run-slice-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The durable local WorkerRun build was complete, warning-bearing, and routed to
an independent check. The check needed to verify durable Service persistence,
host process accounting, idempotency, artifacts, evidence, EventRecord
truthfulness, and non-capability boundaries without repairing implementation.

### Implementation Notes

- Added a check task packet and independent task-local harness.
- Ran a fresh durable fixture as the system under test with `write_reports=False`.
- Independently inspected temporary SQLite objects, events, idempotency rows,
  artifact metadata, raw event stream integrity, false-boundary values, and
  committed report consistency.
- Preserved the failed evidence and routed to a bounded repair task.

### Verification

The independent harness recorded `REQUEST_CHANGES`, `material_finding_count: 1`,
and `missing_evidence: 0`. The fresh fixture still proved one process call,
authorization before launch, grant consumption, monotonic events, idempotent
replay without a second launch, artifact integrity, and false-boundary
preservation.

### Remaining Issues

- `event_record_result_consistency`: `.aide/reports/durable-local-worker-run-slice-v0/fixture-report.json`
  records `host_result: PASS`, but `.aide/reports/durable-local-worker-run-slice-v0/event-record.json`
  records `spec.payload.result: null`.
- Next task: `AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`.

## Work Item: AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `core/service/durable_worker_run.py`
- `.aide/scripts/tests/test_aide_durable_worker_run_slice.py`
- `.aide/reports/durable-local-worker-run-slice-v0/**`
- `.aide/reports/durable-local-worker-run-slice-v0-repair-01/**`
- `.aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The independent durable WorkerRun check found that the committed EventRecord
payload dropped the observed host result, even though the fixture report and
EventRecord status both recorded `PASS`.

### Implementation Notes

- Updated EventRecord payload generation to use the live host result when
  available and fall back to normalized fixture-report `host_result`.
- Added a focused regression assertion that `build_event_record(report)`
  preserves `PASS`.
- Regenerated durable WorkerRun reports and added repair evidence/reports.

### Verification

The regenerated fixture report records `host_result: PASS`; the regenerated
EventRecord records `spec.payload.result: PASS`. Focused tests, durable
validation, and compileall passed before final validation.

### Remaining Issues

- Independent repair check remains required before accepting
  `durable_local_worker_run_slice_v0`.
- The durable WorkerRun slice remains fixture-backed and does not implement a
  general worker harness, autonomous AI worker, scheduler, leases, persistent
  daemon, Workbench/MCP runtime, provider/model calls, network calls,
  preview/apply/rollback, transaction approval, repository mutation, GitHub
  mutation, release, or promotion.

## Work Item: AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/**`
- `.aide/reports/durable-local-worker-run-slice-v0-repair-01-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The durable WorkerRun repair claimed to close the single material finding from
the independent check. A separate check was needed to verify the closure without
repairing implementation or accepting the capability.

### Implementation Notes

- Added a check-only task packet and independent task-local harness.
- Verified the source check recorded exactly one material finding.
- Verified Repair 01 records `PASS_WITH_WARNINGS`, `material_finding_count: 0`,
  `missing_evidence: 0`, and this check as its next task.
- Verified the durable WorkerRun EventRecord payload result now matches the
  fixture report `host_result: PASS`.
- Verified source/test coverage for the normalized `host_result` case.
- Verified false-boundary and source/workspace unchanged claims remain narrow.

### Verification

The independent harness recorded `PASS_WITH_WARNINGS`,
`material_finding_count: 0`, and `missing_evidence: 0`. Focused durable tests,
durable validation, task inspect/evidence, and broad validation passed.

### Remaining Issues

- `durable_local_worker_run_slice_v0` remains unaccepted until the acceptance
  task runs.
- The slice remains fixture-backed and does not implement a general worker
  harness, autonomous AI worker, scheduler, leases, persistent daemon,
  Workbench/MCP runtime, provider/model calls, network calls,
  preview/apply/rollback, transaction approval, repository mutation, GitHub
  mutation, release, or promotion.

## Work Item: AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01

### Status

Completed with `ACCEPTED_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/**`
- `.aide/reports/durable-local-worker-run-slice-v0-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The durable WorkerRun source chain had completed the required build, check,
repair, and independent repair check sequence. The repair check verified the
single original material finding was closed, preserved failed-check evidence,
and routed to acceptance.

### Implementation Notes

- Added an acceptance-only task packet and acceptance reports.
- Accepted exactly `durable_local_worker_run_slice_v0`.
- Preserved the narrow accepted boundary: fixture-backed local durable WorkerRun
  recording through accepted local Service, trust, registered-process, and
  LocalProcessExecutionHost fixture slices.
- Routed next queue work to a bounded distribution/update protocol planning
  task because the 25 June 2026 handoff's earlier local-trust gate reference is
  stale relative to live queue truth.

### Verification

Durable WorkerRun validation, task inspect/evidence checks, broad validation,
and diff checks are recorded in the task-local evidence.

### Remaining Issues

- The accepted capability remains fixture-backed and local only.
- It does not implement a general worker harness, autonomous AI worker, remote
  ExecutionHost, scheduler, leases, persistent daemon, Workbench/MCP runtime,
  provider/model calls, network calls, preview/apply/rollback, transaction
  approval, repository mutation, GitHub mutation, release, or promotion.

## Work Item: AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01/**`
- `.aide/reports/distribution-update-protocol-v1-plan/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The durable local WorkerRun slice is accepted, and live queue truth routes next
to distribution/update planning. The plan normalizes existing Q43-Q48 install,
repair, upgrade, rollback/uninstall, release bundle, and release-draft work
instead of replacing it with a greenfield distribution design.

### Implementation Notes

- Added the plan-only task packet and reports.
- Inventoried existing no-apply/no-publish Q43-Q48 surfaces.
- Defined the distribution object dependency graph, compatibility map,
  source-of-truth map, ownership taxonomy, lifecycle state machines, migration
  rules, refusal registry, artifact/source/channel model, rollout rings,
  fixture matrix, security invariants, and public release gates.
- Selected `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01` as the exact first build
  task because downstream lock, ledger, record, plan, rollback, and receipt
  objects require a stable distribution identity.

### Verification

Install, repair, upgrade, rollback, uninstall, release-bundle, and release-draft
status/validation commands passed in their existing no-apply/no-publish modes.
Task inspect/evidence, broad validation, diff checks, and scoped leak checks are
recorded in the task-local evidence.

### Remaining Issues

- This task is planning only and does not accept public release readiness.
- Real ScreenSave, Eureka, and Dominium canary installation/update behavior was
  not executed in this task.
- All install/update/repair/rollback/uninstall apply, release publication,
  GitHub mutation, target repository mutation, Workbench/MCP runtime, and
  source-change preview/apply/rollback behavior remains unimplemented.

## Work Item: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting review.

### Changed Paths

- `.aide/protocol/aide-distribution-manifest-v1.schema.json`
- `core/protocol/distribution_manifest.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_distribution_manifest_v1.py`
- `.aide/fixtures/distribution-manifest-v1/**`
- `.aide/reports/distribution-manifest-v1/**`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The accepted distribution/update protocol v1 plan selected
`DistributionManifest v1` as the first build dependency. Downstream ProjectLock,
OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle,
and UpdateReceipt objects need stable distribution identity before apply behavior
can be safely designed.

### Implementation Notes

- Added a Draft 2020-12 schema for `DistributionManifest`.
- Added `core/protocol/distribution_manifest.py` for deterministic projection,
  canonical digest calculation, validation, fixture generation, and report
  writing.
- Added AIDE Lite `distribution-manifest status`, `project`, and `validate`
  commands.
- Generated valid and invalid fixture corpus covering source kinds, protocol
  ranges, required features, migrations, forbidden members, duplicates, digests,
  checksums, signatures, SBOM claims, and reordered input.
- Projected existing Q47 release bundle evidence into distribution identity and
  treated Q48 release-draft material as publication-review evidence only.

### Verification

Focused tests pass. `distribution-manifest status`, `project`, and `validate`
pass with warnings and `error_count: 0`. Broader validation is recorded in
task-local evidence.

### Remaining Issues

- `distribution_manifest_v1` remains proposed until independent check and
  acceptance.
- Existing Q47 release artifacts remain local preview/no-publish evidence.
- Signature verification, SBOM generation, install/update apply, release
  publication, target mutation, Workbench/MCP runtime, provider/model calls, and
  promotion remain unimplemented.

## Work Item: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01

### Status

Completed with `REQUEST_CHANGES` and awaiting review.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01/**`
- `.aide/reports/distribution-manifest-v1-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The DistributionManifest v1 build proposed a new distribution identity object
over Q47 local release evidence. A check-only gate was required before any
acceptance or downstream ProjectLock work could depend on that identity.

### Implementation Notes

- Added a check-only task packet and report set.
- Added a task-local independent harness that recomputes digests without using
  the production digest helper as authority.
- Exercised the live manifest helper as the system under test for adversarial
  schema, digest, component, artifact, checksum, protocol, and contamination
  probes.
- Preserved the check boundary; no production code, schema, fixture, or source
  report was repaired.

### Verification

The independent harness recorded `REQUEST_CHANGES`,
`material_finding_count: 9`, `missing_evidence: 0`, and routed to
`AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.

### Remaining Issues

- `schema.optional_extension_boundary_missing`
- `identity.mutable_status_changes_distribution_digest`
- `component.graph_integrity_not_validated`
- `artifact.integrity_metadata_not_validated`
- `path.preaccess_validation_order_violation`
- `checksum.value_not_verified`
- `protocol.range_semantics_incomplete`
- `contamination.forbidden_members_silently_filtered`
- `fixture.required_coverage_incomplete`

No implementation repair, DistributionManifest acceptance, ProjectLock work,
install/update/repair/rollback/uninstall apply, release publication, target
mutation, Workbench/MCP runtime, provider/model call, source-change
preview/apply/rollback, or promotion was performed.

## Work Item: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01

### Status

Completed with `PASS_WITH_WARNINGS` and awaiting independent repair check.

### Changed Paths

- `.aide/protocol/aide-distribution-manifest-v1.schema.json`
- `core/protocol/distribution_manifest.py`
- `.aide/scripts/tests/test_aide_distribution_manifest_v1.py`
- `.aide/fixtures/distribution-manifest-v1/**`
- `.aide/reports/distribution-manifest-v1/**`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The independent check found nine material defects in the proposed
DistributionManifest v1 identity. The repair closes only those defects and
preserves the review boundary before acceptance or ProjectLock work.

### Implementation Notes

- Added task-local turn context, allowed paths, finding matrix, validation
  plan, stop conditions, and campaign state before production edits.
- Added explicit `extensions` schema surfaces while keeping canonical objects
  closed.
- Removed mutable `status` from distribution identity digest input.
- Added component content-digest recomputation, artifact-ref closure,
  component-id uniqueness, dependency closure, and cycle detection.
- Added local artifact byte-count, digest, media-type, compression, checksum,
  and path-containment validation.
- Rejected malformed release artifact paths before filesystem access.
- Added checksum value comparison and basename-collision checks.
- Added exact protocol range and reader/writer compatibility validation.
- Changed local-directory inventory to record forbidden members as
  contamination rather than silently filtering.
- Expanded the committed fixture corpus for the required repair matrix.

### Verification

Focused DistributionManifest tests and `distribution-manifest validate` pass
with warnings and `error_count: 0`. Broad validation is recorded in task-local
evidence.

### Remaining Issues

- `distribution_manifest_v1` remains proposed until independent repair check
  and acceptance.
- ProjectLock v0 has not started.
- Install/update/repair/rollback/uninstall apply, release publication, target
  mutation, Workbench/MCP runtime, provider/model calls, source-change
  preview/apply/rollback, and promotion remain unimplemented.

## Work Item: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01

### Status

Completed with `REQUEST_CHANGES` and stopped the serialized distribution wave.

### Changed Paths

- `.aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/**`
- `.aide/reports/distribution-manifest-v1-repair-01-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 01 reported all nine DistributionManifest v1 check findings closed, but
the queue required independent repair verification before acceptance or
ProjectLock v0 work could begin.

### Implementation Notes

- Added a check-only queue task and report directory.
- Added a task-local independent checker that recomputes digests, probes
  extension and identity behavior, exercises component/artifact/checksum/path
  validation, and checks protocol range, contamination, fixture coverage, Q47
  mapping, and non-capability claims.
- Corrected the check harness during the task so its own allowed outputs and
  source literals were not counted as material implementation defects.
- Preserved the check boundary; no production code, schema, fixture, manifest
  report, Q43-Q48 implementation, acceptance task, ProjectLock task, target
  repository, release publication, or apply behavior was changed.

### Verification

The independent check recorded `REQUEST_CHANGES`, `material_finding_count: 4`,
`missing_evidence: 0`, and recommends exactly
`AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02`.

Validation receipts recorded passing focused DistributionManifest tests,
DistributionManifest status/project/validate, Q43-Q48 validation/status
commands, release validation, release draft validation, task inspect/evidence,
broad `aide_lite.py validate`, diff checks, and leak scans.

### Remaining Issues

- `protocol.future_major_not_implicitly_accepted`: `protocol_range.max: 2.x`
  is accepted for v1 without explicit future-major support.
- `contamination.forbidden_path_classification_complete`: forbidden target-root
  export-pack members under `files/` are not fully classified.
- `contamination.directory_forbidden_members_recorded`: nested forbidden
  directory members under `files/` are not recorded as contamination.
- `fixture.future_major_protocol_fixture_present`: the fixture corpus has no
  direct invalid future-major protocol-range fixture.

DistributionManifest acceptance, ProjectLock v0, OwnershipLedger v1,
InstallRecord v0, install/update/repair/rollback/uninstall apply, release
publication, target mutation, Workbench/MCP runtime, provider/model calls,
worker execution, and promotion remain blocked pending Repair 02.

## Work Item: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02

### Summary

Completed the bounded second repair for DistributionManifest v1 after the
Repair 01 check left four material findings open.

### Implementation Notes

- Added the Repair 02 queue task, status, ExecPlan, prompt, task-local turn
  context, finding matrix, allowed paths, validation plan, stop conditions, and
  campaign state.
- Tightened protocol-range validation so v1 rejects future-major maximums such
  as `2.x` and `2.0.0` unless a future reviewed contract explicitly supports
  them.
- Added component-level future-major compatibility rejection through optional
  `max_reader_version`, `max_writer_version`, and `protocol_range` checks.
- Added target-root classification for the accepted `files/` package prefix so
  `files/.aide.local/**`, `files/.env`, generated `.aide/context/latest-*`,
  generated `.aide/reports/**`, generated latest state, logs, caches, secrets,
  and raw prompt/response members are rejected against their installed view.
- Preserved exact allowed packaged report-reference files already present in
  the current Q47 preview pack while keeping generated report trees forbidden.
- Added structured directory inventory reporting so forbidden members are
  retained in contamination evidence instead of disappearing from the clean
  digest input.
- Added direct invalid fixtures for future-major protocol cases:
  `protocol-range-max-2x`, `protocol-range-max-2-0-0`,
  `protocol-range-min-2-0-0`, and `component-protocol-future-major`.
- Added focused tests for protocol semantics, `files/` target-root
  classification, nested directory contamination, and future-major fixture
  validation.
- Generated Repair 02 reports for protocol range, contamination
  classification, directory contamination, fixture coverage, finding
  disposition, status, and next-task routing.

### Verification

Initial compile and focused DistributionManifest tests passed after a narrow
allowlist was added for the current Q47 preview pack's exact packaged report
reference records. Full validation is recorded with the task evidence and final
task report.

### Remaining Issues

DistributionManifest v1 remains proposed until independent Repair 02 check and
acceptance. ProjectLock v0, OwnershipLedger v1, install/update apply, release
publication, target mutation, Workbench/MCP runtime, provider/model calls,
worker execution, preview/apply/rollback, and promotion were not started.

## Work Item: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02

### Summary

Completed the independent check-only review for Repair 02.

### Implementation Notes

- Added the check task packet and reports without modifying implementation,
  schema, fixture, helper, or test code.
- Used a check-local protocol range expectation to verify current v1 ranges,
  exact `1.0.0`, lower `0.9.0`, future-major maxima, malformed ranges,
  inverted ranges, min above current, component future-major constraints, and
  unknown required future-major features.
- Independently checked `files/` target-root contamination classification,
  allowed controls, and unknown-prefix behavior.
- Built a temporary directory contamination fixture and verified forbidden
  members remain recorded with source member, target member, packaging prefix,
  reason, and refusal code.
- Verified the four future-major invalid fixtures exist, are mentioned by
  tests, load from disk, and fail with `distribution.unsupported_protocol_range`.
- Rechecked Repair 01 regression surfaces, Q47/Q48 boundaries, and explicit
  non-capabilities.

### Verification

Validation receipts record passing focused DistributionManifest tests,
DistributionManifest validate, Q43-Q48 no-apply/no-publish validators, task
inspect/evidence, broad `aide_lite.py validate`, JSON parsing, path and secret
scans, diff checks, and commit-policy check.

### Remaining Issues

DistributionManifest v1 is still not accepted in this check task. The next
serialized task is `AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`; ProjectLock v0
remains blocked until acceptance is complete.

## Work Item: AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01

### Summary

Accepted exactly `distribution_manifest_v1` with warnings.

### Implementation Notes

- Added the acceptance-only queue task and acceptance reports.
- Accepted DistributionManifest v1 only as stable, deterministic, portable
  distribution identity and metadata for one local AIDE distribution.
- Recorded the accepted boundary for components, artifacts, digests, protocol
  ranges, compatibility boundaries, provenance references, placeholder SBOM and
  signature boundaries, source-contamination handling, and explicit
  non-capabilities.
- Preserved non-capabilities for ProjectLock, OwnershipLedger, InstallRecord,
  migration/update/rollback objects, install/update apply, target mutation,
  public release readiness, release publication, signatures, SBOM generation,
  network, provider/model calls, worker execution, and Workbench/MCP runtime.

### Verification

Validation receipts record DistributionManifest validation, Q43-Q48 no-apply
and no-publish validators, task inspect/evidence, broad `aide_lite.py validate`,
JSON parsing, path and secret scans, diff checks, and commit-policy check.

### Remaining Issues

ProjectLock v0 was not started in this acceptance task. The next serialized
task is `AIDE-BUILD-PROJECT-LOCK-V0-01`.
source-change preview/apply/rollback, and promotion remain blocked.

## Work Item: AIDE-BUILD-PROJECT-LOCK-V0-01

### Summary

Built the proposed `project_lock_v0` protocol slice.

### Implementation Notes

- Added a Draft 2020-12 ProjectLock schema with explicit extension maps.
- Added `core/protocol/project_lock.py` for deterministic lock projection,
  digesting, fixture generation, validation, reports, and non-capability
  boundaries.
- Added `project-lock status`, `project-lock project`, and `project-lock
  validate` AIDE Lite commands.
- Added focused ProjectLock tests and a valid/invalid fixture corpus covering
  digest binding, accepted DistributionManifest binding, component selection,
  optional component explicitness, dependency closure, channel versus digest
  authority, overlay/path/secret/source-state refusals, unknown required
  features, and extension round-trip.

### Verification

Validation receipts record focused ProjectLock tests, ProjectLock
status/project/validate, DistributionManifest regression validation, Q43-Q48
no-apply/no-publish validators, task inspect/evidence, broad
`aide_lite.py validate`, JSON parsing, path and secret scans, diff checks, and
commit-policy check.

### Remaining Issues

ProjectLock v0 remains proposed until independent check and acceptance. It does
not implement install truth, install/update apply, admission, authorization,
target mutation, release publication, network/provider calls, runtime, or
OwnershipLedger v1. The next serialized task is
`AIDE-CHECK-PROJECT-LOCK-V0-01`.

## Work Item: AIDE-CHECK-PROJECT-LOCK-V0-01

### Summary

Independently checked the proposed `project_lock_v0` build.

### Implementation Notes

- Added the check-only queue task and ProjectLock check reports.
- Recomputed ProjectLock identity with a check-local canonicalizer.
- Verified mutable status, queue routing, and selected channel are outside
  ProjectLock identity while semantic lock fields remain identity-bound.
- Verified the selected accepted DistributionManifest digest, manifest payload
  digest, selected component digest, selected artifact refs, and dependency
  closure.
- Reviewed the valid/invalid fixture corpus and explicit non-capability
  boundary.

### Verification

Validation includes source task inspect/evidence, the check-local digest and
fixture probe, focused ProjectLock tests, broad `aide_lite.py validate`, task
inspect/evidence for the check task, diff checks, and commit-policy check.

### Remaining Issues

ProjectLock v0 remains unaccepted until `AIDE-ACCEPT-PROJECT-LOCK-V0-01`.
The check does not implement or accept install truth, install/update apply,
admission, authorization, target mutation, release publication, runtime, or
OwnershipLedger v1.

## Work Item: AIDE-ACCEPT-PROJECT-LOCK-V0-01

### Summary

Accepted exactly `project_lock_v0` with warnings.

### Implementation Notes

- Added the acceptance-only queue task and acceptance reports.
- Accepted ProjectLock v0 only as a target-owned distribution selection and
  binding object.
- Recorded the accepted boundary for accepted DistributionManifest digest,
  manifest payload digest, selected component digest, selected artifact refs,
  dependency closure, informational channel, optional extension preservation,
  and required feature/extension refusal.
- Preserved non-capabilities for install truth, install/update/apply, admission,
  authorization, target mutation, release publication, runtime, OwnershipLedger,
  InstallRecord, and downstream distribution behavior.

### Verification

Validation includes source build/check task inspection, ProjectLock validation,
task inspect/evidence, broad `aide_lite.py validate`, diff checks, and
commit-policy check.

### Remaining Issues

OwnershipLedger v1 has not been started in this acceptance task. The next
serialized task is `AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`.

## Work Item: AIDE-BUILD-OWNERSHIP-LEDGER-V1-01

### Summary

Built the proposed `ownership_ledger_v1` protocol slice.

### Implementation Notes

- Added a Draft 2020-12 OwnershipLedger schema with explicit extension maps.
- Added `core/protocol/ownership_ledger.py` for deterministic ledger projection,
  digesting, taxonomy validation, fixture generation, validation, reports, and
  non-capability boundaries.
- Added `ownership-ledger status`, `ownership-ledger project`, and
  `ownership-ledger validate` AIDE Lite commands.
- Added focused tests and a valid/invalid fixture corpus covering ProjectLock
  binding, taxonomy completeness, duplicate records, unknown classes, vendor
  digest requirements, managed-section identity, unknown/never-touch no-apply
  policy, unsafe paths, source latest contamination, unknown required features,
  and required extension rejection.

### Verification

Initial validation passed focused OwnershipLedger tests, py_compile, and
`ownership-ledger validate`. Final validation receipts are recorded in task
evidence.

### Remaining Issues

OwnershipLedger v1 remains proposed until independent check and acceptance. It
does not implement install truth, install/update apply, admission,
authorization, target mutation, release publication, runtime, InstallRecord, or
UpdatePlan.

## Work Item: AIDE-CHECK-OWNERSHIP-LEDGER-V1-01

### Summary

Independently checked the proposed `ownership_ledger_v1` build and returned
`REQUEST_CHANGES`.

### Implementation Notes

- Added the check-only queue task and OwnershipLedger check reports.
- Recomputed the OwnershipLedger digest independently and confirmed the current
  compact source projection is deterministic.
- Verified the eleven ownership classes are present and no apply behavior is
  implemented.
- Found five material gaps against the requested downstream oracle:
  incomplete file-entry fields, incomplete managed-section fields, missing Q43
  migration, incomplete conflict detection, and incomplete fixture coverage.
- Stopped the serialized wave before acceptance, InstallRecord, MigrationRecord,
  UpdatePlan, and RollbackBundle.

### Verification

Validation included source task inspect/evidence, OwnershipLedger
status/project/validate, the failing `migrate-q43` CLI probe, check-local field
and collision probes, py_compile, focused OwnershipLedger tests, predecessor
DistributionManifest and ProjectLock validation, Q43-Q48 no-apply/no-publish
validators, and broad `aide_lite.py validate`.

### Remaining Issues

The next serialized task is
`AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01`. No production implementation was
repaired in this check task.

## Work Item: AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01

### Summary

Completed the bounded repair for the five OwnershipLedger v1 material findings
and stopped at the independent repair-check gate.

### Implementation Notes

- Added task-local turn context, finding matrix, allowed paths, validation plan,
  stop conditions, and campaign state before production edits.
- Expanded OwnershipLedger records with file-entry fields for owner, source,
  digest, observed target digest, portability role, preservation policy,
  operation constraints, platform/case notes, deterministic observation times,
  and supersession refs.
- Expanded managed-section records with containing file, section identity,
  marker format, marker/content digests, preimage requirements, update
  constraints, and manual-outside-only preservation policy.
- Added semantic validation for missing owners, vendor source refs, observed
  digest mismatch, distribution mutability, missing evidence, unresolved
  symlink/reparse entries, duplicate target paths, case-fold collisions,
  file-section conflicts, overlapping sections, nested ambiguity, and section
  marker/identity failures.
- Added deterministic Q43 ownership-class migration projection and
  `ownership-ledger migrate-q43`.
- Expanded the fixture corpus with direct valid class fixtures, managed-section
  preservation fixture, Q43 migration fixtures, and invalid direct cases for the
  repaired refusal behavior.
- Generated OwnershipLedger Repair 01 report matrices and next-task routing.

### Verification

Focused OwnershipLedger tests pass. `ownership-ledger status`, `project`,
`validate`, and `migrate-q43` pass with warnings; ProjectLock and
DistributionManifest regression validation pass with warnings; broad
`aide_lite.py validate` passes.

### Remaining Issues

OwnershipLedger v1 remains proposed until independent Repair 01 check and
acceptance. InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle,
distribution apply, canaries, target mutation, release publication, runtime,
provider/model calls, Workbench/MCP behavior, preview/apply/rollback, and
promotion were not started.

## Work Item: AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01

### Summary

Completed the independent Repair 01 check for OwnershipLedger v1 and stopped at
the acceptance gate.

### Implementation Notes

- Added the check-only queue task and check report directory.
- Verified the five source findings exactly match the five Repair 01
  dispositions.
- Ran a check-local harness that independently reviews committed reports,
  recomputes check-local digests, inspects schema alignment, exercises direct
  repaired SUT probes, and verifies fixture/refusal coverage.
- Confirmed file-entry contract fields, managed-section contract fields, Q43
  migration projection, conflict-model refusals, and fixture coverage are
  closed.
- Preserved explicit non-capabilities: no implementation repair, no acceptance,
  no InstallRecord/MigrationRecord/UpdatePlan/RollbackBundle, no apply behavior,
  no target mutation, no publication, no network/provider/model behavior, no
  runtime, and no promotion.

### Verification

The independent harness passed focused OwnershipLedger tests,
`ownership-ledger status/project/validate/migrate-q43`, ProjectLock and
DistributionManifest regression validation, and broad `aide_lite.py validate`.
Final task evidence records outer validation, diff checks, and commit policy.

### Remaining Issues

OwnershipLedger v1 remains proposed until the acceptance-only task completes.
The next serialized task is `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`.

## Work Item: AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01

### Summary

Accepted exactly `ownership_ledger_v1` with warnings and stopped before
downstream distribution objects.

### Implementation Notes

- Added the acceptance-only queue task and acceptance reports.
- Accepted OwnershipLedger v1 only as target ownership classification and
  preservation metadata over accepted DistributionManifest v1 and ProjectLock
  v0.
- Recorded the accepted boundary for eleven ownership classes, file-entry
  contract fields, managed-section contract fields, Q43 projection-only
  migration behavior, conflict/refusal model, fixture coverage, warnings, and
  explicit non-capabilities.
- Added `ownership-ledger-downstream-use.md` so later distribution objects know
  what they may cite and what they must not infer.
- Preserved non-capabilities for install/update/repair/rollback/uninstall
  apply, migration apply, target scan authority, target mutation, project
  canaries, release readiness, release publication, tags, uploads, GitHub
  Releases, runtime, worker execution, provider/model/network behavior,
  Workbench, Commander, preview/apply/rollback, branch/worktree automation, and
  promotion.

### Verification

Validation receipts record JSON parsing, compileall, focused OwnershipLedger
tests, OwnershipLedger status/project/validate/migrate-q43, DistributionManifest
and ProjectLock regression validation, Q43-Q48 no-apply/no-publish validators,
task inspect/evidence for source and acceptance tasks, broad
`aide_lite.py validate`, path and secret-like scans, diff checks, and
post-commit commit-policy check as the final gate for the completed commit.

### Remaining Issues

InstallRecord v0 has not been started. The next serialized task is
`AIDE-BUILD-INSTALL-RECORD-V0-01`.

## Work Item: AIDE-DISTRIBUTION-SAFETY-WAVE-01

### Summary

Materialized the Distribution Safety Wave controller and stopped before
InstallRecord implementation.

### Implementation Notes

- Added the wave-control queue task, status, ExecPlan, prompt, and task-local
  evidence.
- Added distribution-safety wave reports covering the dependency map, object
  responsibility map, no-apply/no-publish boundary, validation matrix,
  repair-routing matrix, stop-condition matrix, canary ordering rationale, wave
  summary, and next-task prompt.
- Confirmed live repo truth shows `main` and `origin/main` both at the accepted
  OwnershipLedger commit, so the wave can start from accepted local and origin
  truth.
- Preserved the wave as planning and queue materialization only. InstallRecord,
  MigrationRecord, UpdatePlan, RollbackBundle, UpdateReceipt,
  DistributionApplyEngine, self-consumer fixture, ScreenSave/Eureka/Dominium
  canaries, local canary archive, public readiness, target mutation, release
  publication, provider/model/network calls, runtime, Workbench, Commander,
  Omnigent, and branch/worktree automation were not started.

### Verification

Validation receipts record generated JSON/YAML parsing, task inspect/evidence,
broad `aide_lite.py validate`, generated-report and evidence scans for local
paths, secret-like material, and source-output misuse, diff checks, and
post-commit commit-policy check.

### Remaining Issues

The wave controller stops at `needs_review`. The next serialized task is
`AIDE-BUILD-INSTALL-RECORD-V0-01`.

## Work Item: AIDE-BUILD-INSTALL-RECORD-V0-01

### Summary

Built InstallRecord v0 as a no-apply distribution-safety protocol slice.

### Implementation Notes

- Added the InstallRecord v0 schema, helper, CLI commands, fixture corpus,
  focused tests, generated reports, queue packet, and task-local evidence.
- InstallRecord binds the accepted DistributionManifest, ProjectLock, and
  OwnershipLedger by refs and digests.
- The record models install mode/source, observed existing state, installed
  component refs, installed file-entry refs, installed managed-section refs,
  validation refs, evidence refs, warnings, explicit non-capabilities,
  deterministic creator/timestamp metadata, and extension maps.
- Semantic validation fails closed for missing predecessor refs, predecessor
  mismatches, unknown installed refs, apply authority claims, target mutation
  claims, unknown required features, absolute paths, traversal paths,
  source-output misuse, missing evidence, digest mismatch, and unknown required
  extensions.
- Unknown optional features and extensions are preserved and tolerated.

### Verification

Validation receipts record compileall, focused InstallRecord tests,
`install-record status`, `install-record project`, `install-record validate`,
predecessor regression validation, Q43-Q48 no-apply/no-publish validators,
broad `aide_lite.py validate`, task inspect/evidence, path and secret-like
scans, source-output misuse scan, diff checks, and commit-policy check.

### Remaining Issues

InstallRecord v0 remains proposed until independent check and acceptance. The
next serialized task is `AIDE-CHECK-INSTALL-RECORD-V0-01`.

## Work Item: AIDE-CHECK-INSTALL-RECORD-V0-01

### Summary

Independently checked InstallRecord v0 build output.

### Implementation Notes

- Checked commit `7a0abf5a85ff8442f65237e5824f831b4176f252`.
- Verified schema, helper, CLI, tests, generated reports, fixture matrix, and task evidence from `AIDE-BUILD-INSTALL-RECORD-V0-01`.
- Confirmed InstallRecord v0 models the required record fields and binds accepted DistributionManifest, ProjectLock, and OwnershipLedger refs/digests.
- Confirmed fail-closed coverage for missing or mismatched predecessor refs, unknown installed component/file-entry/managed-section refs, apply authority claims, target mutation claims, unknown required features/extensions, absolute paths, traversal paths, source latest output misuse, source output as target truth, and missing evidence.
- Confirmed unknown optional features/extensions are tolerated and preserved.
- Wrote `.aide/queue/AIDE-CHECK-INSTALL-RECORD-V0-01/**` and `.aide/reports/install-record-v0-check/**`.
- Did not modify InstallRecord implementation, DistributionManifest implementation, ProjectLock implementation, OwnershipLedger implementation, release archives, target repos, provider/model/network surfaces, branch/worktree automation, or apply behavior.

### Verification

Validation receipts record JSON parse, compileall, focused InstallRecord tests,
`install-record status`, `install-record project`, `install-record validate`,
predecessor regression validation, Q43-Q48 no-apply/no-publish validators,
broad `aide_lite.py validate`, build and check task inspect/evidence, path and
secret-like scans, source-output misuse scan, diff checks, and commit-policy
check.

### Remaining Issues

InstallRecord v0 remains proposed until acceptance. The next serialized task is
`AIDE-ACCEPT-INSTALL-RECORD-V0-01`.
