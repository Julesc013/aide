# Tentative AIDE Product Vision And Roadmap

Status: tentative planning record

Authority: advisory only. This document does not accept a capability, authorize a
runtime, promote a provider, or change the executable queue order.

Current live gate:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

That check is the next executable gate implied by current repository evidence.
The registered-process provider remains proposed and unaccepted until an
independent repair check and later reuse proofs pass.

## Product Definition

AIDE is the universal development control plane, compatibility kernel,
governance fabric, and living project twin for complex software systems.

It turns human or machine intent into bounded work, grounded context, governed
capability invocations, previewable transactions, validated outcomes, durable
evidence, event history, and maintained project knowledge.

Its durable loop is:

```text
Intent
-> ContextPack
-> WorkUnit
-> PolicyDecision
-> CapabilityGrant
-> CapabilityInvocation
-> worker or deterministic tool
-> Proposal
-> DevelopmentTransaction
-> PreviewSession / ShadowWorkspace
-> review and approval
-> domain-authoritative apply
-> Validation
-> EvidencePacket
-> EventRecord
-> RepoGraph update
-> OKF update
-> Workbench / Commander / IDE projections
```

AIDE is not a model, a coding-agent harness, an IDE clone, a game engine, a
universal scheduler for every internal subagent, or a replacement for MCP, A2A,
ACP, CI, build systems, domain engines, or authoring tools. It makes those
systems governable, interoperable, replaceable, and auditable.

AIDE should remain useful with:

```text
no model
no cloud
no network
no modern IDE
no proprietary runtime
```

AI workers improve what AIDE can do, but they are not the foundation of AIDE's
authority.

## Architectural Law

```text
Universal semantics at boundaries.
Domain meaning inside domains.
Host presentation inside hosts.
Specialized execution in hot paths.
```

Operationally:

```text
AIDE owns durable development truth.
Execution hosts own bounded sessions.
Domains own mutation meaning.
Hosts own native presentation.
Workers remain untrusted proposers.
```

## System Shape

```text
AIDE Core
  stable semantics, identity, work, authority, capability invocation,
  transactions, evidence, events, compatibility, and knowledge records

AIDE Service
  optional durable runtime for objects, events, artifacts, grants,
  invocations, projections, subscriptions, and bounded scheduling

Execution Hosts
  local runner, Omnigent, CI, build farm, remote worker host, human runner

Worker Harnesses
  Codex, Claude Code, Pi, custom agents, scripts, humans

Capability Providers
  Dominium, Domino, AIDE tools, build and test systems, external services

Domain Bridges
  AIDE-Dominium, AIDE-Eureka, and future engine or application bridges

Host Adapters
  Workbench, Commander, Visual Studio, legacy IDE sidecars, CLI, mobile

Project Twin
  RepoGraph operational graph plus OKF readable knowledge projections
```

For the flagship stack:

```text
AIDE governs, coordinates, routes, records, and proves.
Domino performs deterministic system operations.
Dominium defines product and world law.
Workbench captures intent and presents context, preview, approval,
evidence, recovery, simulation, and authoring.
Omnigent may host bounded agent sessions as one replaceable package.
```

## Product Roles

```text
AIDE
  coordinates, governs, routes, records, proves, and explains

Domino
  performs deterministic engine and system operations

Dominium
  defines product, game, world, command, refusal, and transaction law

Dominium Workbench
  provides native context, preview, approval, authoring, recovery, and inspection

Omnigent
  may host bounded agent sessions and enforce execution constraints

Codex / Claude / Pi / future agents
  act as replaceable workers

MCP / A2A / ACP
  expose interoperability projections, not canonical truth
```

## Role Taxonomy

Use one extension envelope, but do not collapse every component into one
provider interface.

| Role | Responsibility |
| --- | --- |
| `ExecutionHost` | Runs bounded sessions and streams events. |
| `WorkerHarness` | Implements an agent or worker loop. |
| `ModelProvider` | Performs inference. |
| `CapabilityProvider` | Implements typed operations. |
| `DomainBridge` | Maps AIDE semantics into domain meaning. |
| `HostAdapter` | Captures context and presents native UI. |
| `SandboxBackend` | Provides isolation. |
| `TestBackend` | Executes deterministic validation. |
| `ArtifactStore` | Stores durable payloads. |
| `KnowledgeSource` | Supplies observations for RepoGraph and OKF. |

Omnigent belongs in the execution-host, sandbox, runtime-approval,
collaboration, event, and usage-reporting space. It should not own canonical
WorkUnits, repository policy, capability admission, checkpoint promotion,
transaction approval, AIDE evidence semantics, or domain mutation meaning.

## Two Execution Abstractions

Keep deterministic capability execution separate from bounded worker execution.

Capability execution:

```text
CapabilityInvocation
-> CapabilityBinding
-> ExecutionProvider
-> ExecutionReceipt
-> CapabilityOutcome
```

Provider examples:

```text
RegisteredProcessExecutionProvider
HostCommandExecutionProvider
HTTPExecutionProvider
MCPExecutionProvider
CIJobExecutionProvider
OfflineMailboxExecutionProvider
HumanExecutionProvider
```

Worker execution:

```text
WorkUnit
-> ExecutionHost
-> WorkerHarness
-> WorkerRun
-> events, artifacts, usage, proposals
```

Execution-host examples:

```text
LocalProcessExecutionHost
OmnigentExecutionHost
CIExecutionHost
RemoteSandboxExecutionHost
```

A registered subprocess and an Omnigent agent session are not the same thing.
They should converge through common AIDE receipts, events, artifacts, and
evidence, not through one overloaded provider interface.

## Stable Kernel Candidates

Keep the permanent kernel small and durable.

Identity and authority:

```text
Principal
Delegation
AdmissionRecord
PolicyDecision
CapabilityGrant
RevocationRecord
```

Project and context:

```text
Workspace
ResourceRef
ArtifactReference
ProjectProfile
ContextPack
RepoGraphSnapshot
KnowledgeObservation
KnowledgeClaim
KnowledgeDecision
```

Work:

```text
WorkUnit
WorkerRun
TestJob
WorkflowRun
BlockerRecord
RepairTask
Checkpoint
```

Capability execution:

```text
CapabilityDefinition
CapabilityBinding
CapabilityInvocation
ExecutionReceipt
CapabilityOutcome
ConformanceProfile
ConformanceResult
```

Change:

```text
PatchTransaction
DevelopmentTransaction
DomainMutationBundle
PreviewSession
ApplyReceipt
RollbackReceipt
```

Proof and interoperability:

```text
EvidencePacket
EventRecord
TranslationReceipt
CompilationReport
ReplayTrace
```

AIDE Core should not learn internal domain structures such as Dominium scene
nodes, Unreal Blueprints, CAD assemblies, database migrations, shader graphs, or
firmware flashes. AIDE governs how such operations are identified, authorized,
previewed, applied, verified, reversed, and explained.

## Native Domain Bridges

A domain bridge owns:

```text
capability mappings
input and output schemas
diagnostic and refusal mappings
domain transaction schemas
evidence mappings
translation receipts
conformance fixtures
```

The AIDE-Dominium bridge should convert:

```text
AIDE CapabilityInvocation
<-> Dominium command

Dominium result/refusal
<-> AIDE CapabilityOutcome

Dominium transaction
<-> AIDE DevelopmentTransaction envelope

Dominium evidence
<-> AIDE EvidencePacket references
```

Dominium should remain native internally. AIDE should project Dominium semantics
outward through adapters rather than redesigning Dominium around MCP, Omnigent,
or any current vendor protocol.

## Extension Package Direction

Tentative package envelope:

```yaml
apiVersion: aide.dev/extensions/v1alpha1
kind: ExtensionPackage

metadata:
  name: omnigent-runtime
  publisher: omnigent-ai
  version: pinned-version
  digest: sha256:...

spec:
  components:
    - kind: ExecutionHost
    - kind: SandboxBackend
    - kind: PolicyCompiler
    - kind: EventTranslator
    - kind: EvidenceCompiler
    - kind: ConformanceSuite
```

Installation is not admission:

```text
discover
-> inspect
-> validate
-> conformance test
-> admit exact digest
-> grant scoped use
-> observe
-> revoke
-> update or roll back
```

Possible execution forms include declarative packages, WASM/WASI components,
out-of-process JSON-RPC processes, OCI containers, remote HTTP or gRPC services,
MCP bindings, A2A bindings, ACP bindings, CLI/file bridges, and host-native
extensions. These are package forms, not trust grants.

## Translation Receipts

AIDE should treat protocol conversion as an explicit, evidenced operation. A
bridge from AIDE to MCP, A2A, ACP, Omnigent, an IDE protocol, a build system, or
a domain schema should produce a `TranslationReceipt`.

Example shape:

```yaml
source:
  protocol: aide.execution-host/v1
  digest: sha256:...

target:
  protocol: omnigent.session/v1
  digest: sha256:...

nativeFeatures:
  - sandbox
  - session-events

emulatedFeatures:
  - checkpoint-resume

unsupportedOptionalFeatures:
  - atomic-multi-repo-apply

missingRequiredFeatures: []
fidelity: normalized
result: accepted_with_loss
```

Rules:

```text
preserve normalized AIDE state
preserve raw foreign payload
record protocol and version
record native, emulated, downgraded, and unsupported semantics
fail closed when required meaning cannot be preserved
```

MCP, A2A, and ACP remain projections or bindings. They do not become internal
authority. AIDE's policy, grant, evidence, admission, and transaction layers sit
above them.

## Knowledge Fabric

Separate observation from truth:

```text
KnowledgeObservation
  Something was observed.

KnowledgeClaim
  An interpreted assertion with provenance, scope, confidence, and validity.

KnowledgeDecision
  Accepted, rejected, superseded, contradicted, or deferred.

KnowledgeProjection
  OKF page, graph node, report, ContextPack section, or UI view.
```

Pipeline:

```text
source
-> observation
-> claim
-> validation or review
-> decision
-> RepoGraph fact
-> OKF projection
-> ContextPack selection
```

RepoGraph should be the machine-queryable operational graph. OKF should be the
portable human and agent-readable explanation layer. `ProjectCapsule` should be
a portable export/import artifact, not a competing source of truth.

## Project Twin

RepoGraph should capture machine-queryable operational knowledge:

```text
files and revisions
folders and logical modules
functions, classes, and symbols
imports, references, and calls
build targets and generated artifacts
tests and coverage
documentation
assets, scenes, and graphs
owners
capabilities
WorkUnits
transactions
failures and evidence
runtime observations
```

OKF should capture portable human and agent-readable explanation:

```text
systems
concepts
decisions
risks
capabilities
current state
known contradictions
evidence links
```

Rule:

```text
RepoGraph models.
OKF explains.
Protocol executes.
Evidence proves.
```

RepoGraph should begin with facts AIDE already has, then add producers
incrementally:

```text
existing file and quality ledgers
Git history
Tree-sitter
SCIP/LSP/compiler indexes
build-system graphs
test coverage
runtime telemetry
domain bridge facts
```

## Preview-First Mutation

The decisive product primitive is:

```text
PreviewSession + ShadowWorkspace
```

It should eventually support file overlays, structured-document overlays, scene
snapshots, graph snapshots, asset staging, build sandboxes, simulation forks,
replay branches, deployment previews, and performance experiments.

Mutation loop:

```text
proposal
-> shadow state
-> policy and capability checks
-> execute candidate
-> validate
-> calculate impact
-> native preview
-> evidence
-> approve, revise, compare, or discard
```

Runtime approval and authoritative transaction approval must remain separate. A
worker or execution host must never approve its own authoritative mutation.

## Roadmap From Current State

Milestone 0: repair gate closure.

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

Current inspected state:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
  commit: 7f043d09ae0c5bbb73d68ad293e6dafaaaa8ddd6
  result: PASS_WITH_WARNINGS
  provider_accepted: false
  recommended_next_task: AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```

No later repair-check result was found in the current repository inspection for
this docs task.

If the repair check passes, route to:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

If material findings remain, route to:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02
```

Milestone 1: prove provider reuse.

```text
AIDE self-validation adapter
-> independent check
Eureka read-only adapter
-> independent check
registered-process provider acceptance
```

Acceptance should require the same provider code, one shared receipt model, one
shared conformance suite, thin domain adapters, no executor changes for new
adapters, zero domain branches in execution core, and zero committed local paths.

Milestone 2: define execution-host semantics.

```text
ExecutionHostContract v0
ExecutionHostRunBinding
ExecutionHostEvent
ExecutionHostArtifact
ExecutionHostApproval
ExecutionHostUsage
LocalProcessExecutionHost reference implementation
```

Required operations:

```text
probe
create_run
attach
send_input
stream_events
resolve_runtime_approval
interrupt
collect_artifacts
finish
reconcile
```

The local implementation comes before Omnigent certification so the contract is
not accidentally designed around one external host.

Milestone 3: complete minimum trust and translation primitives.

```text
Principal
Delegation
AdmissionRecord
PolicyDecision
CapabilityGrant
RevocationRecord
TranslationReceipt
```

Milestone 4: optional durable service.

```text
SQLite object store
append-only event log
content-addressed artifact store
idempotency keys
resumable subscriptions
health
pause/resume/cancel surfaces
materialized projections
```

No general scheduler is needed at this point.

The service should first support one machine and one active run reliably.

Milestone 5: Omnigent integration package.

```text
Omnigent AdapterManifest
immutable session binding
policy compiler
event translator
evidence compiler
usage and cost translator
sandbox receipt
conformance suite
```

Omnigent may enforce stricter constraints than AIDE grants, but it may not widen
them.

Milestone 6: read-only context and shadow execution.

```text
live read-only AIDE MCP
ShadowWorkspace v0
disposable workspace integration
```

Expose read-only status, WorkUnit inspection, ContextPack inspection, OKF search,
RepoGraph excerpts, evidence inspection, and patch inspection. Do not expose
queue mutation or apply.

Milestone 7: first external-worker compatibility proof.

```text
AIDE WorkUnit
-> admitted ExecutionHost package
-> immutable session binding
-> disposable shadow workspace
-> one worker harness
-> ContextPack through read-only resources
-> one admitted read-only Dominium capability
-> EventRecords
-> TestJobs
-> EvidencePacket
-> no-apply PatchTransaction
-> canonical checkout verified unchanged
```

Milestone 8: read-only Workbench.

Show WorkUnits, WorkerRuns, execution-host sessions, costs, budgets, tool events,
capability invocations, evidence, OKF, RepoGraph, patch previews, and conformance
state. Do not enable authoritative mutation yet.

Milestone 9: first complete governed document mutation.

```text
DevelopmentTransaction
PreviewSession
ShadowWorkspace
document preview
approval
document apply
post-apply validation
rollback
EvidencePacket
EventRecord
OKF/RepoGraph refresh
```

This is the first full usable development-system loop:

```text
intent
-> proposal
-> preview
-> approval
-> apply
-> proof
-> rollback
```

Milestone 10: flagship Dominium workflow.

```text
Dominium scene preview
scene apply
undo/evidence
Domino graph editing
asset pipeline
build comparison
simulation branches
performance experiments
```

The flagship experience should be native Workbench authoring, not chatbot-first
interaction:

```text
select
-> state intent
-> inspect context
-> review plan
-> preview
-> edit operations
-> approve
-> apply
-> prove
-> undo or continue
```

## Parallel Track B2

Run project-intelligence work as a read-only serialized lane when it does not
conflict with the product path:

```text
RepositoryFact contract
existing file/quality fact ingestion
RepoGraph snapshot v0
impact reports
affected-test selection
ContextPack integration
OKF integration
Reconciler integration
symbol/build/history producers later
Workbench graph visualization
```

Do not begin with a graph database or universal compiler. Start from AIDE's
existing deterministic facts.

## Product Lane Constraint

AIDE architecture must continue to accelerate real Dominium product progress. Do
not build a sophisticated development fabric around a stalled game.

Every new universal primitive should:

```text
solve a current concrete problem
produce an executable vertical slice
improve a human or player workflow
have measured acceptance criteria
preserve a rollback path
```

Maintain a bounded product lane for the playable client loop, save/load
continuity, local and dedicated server operation, launcher/install/update and
recovery, one complete world/content package, one complete modding path,
accessibility/localization, performance budgets, release packaging, diagnostics,
and support.

## What Should Wait

Do not build yet:

```text
package marketplace
distributed fleet scheduler
full Commander
Mobile application
all IDE adapters
live A2A delegation
broad MCP mutation tools
multi-repository atomic transactions
automatic promotion
self-modifying policy
large-scale provider catalog
```

These are valid later capabilities, but they do not close the first usable
product loop.

## Operating Priorities

Optimize for completed loops, not for the number of schemas or queue items.

```text
1. Correctness and fail-closed execution
2. Reuse across three reference domains
3. One durable local runtime
4. One real external-agent run
5. Read-only native UX
6. Preview and rollback
7. One complete domain hero workflow
8. RepoGraph-driven intelligence
9. Packages, SDKs, legacy hosts, and fleet operation
```

## Do Not Build Yet

```text
Do not fork Omnigent.
Do not merge Omnigent's database into AIDE truth.
Do not make Omnigent mandatory.
Do not make Dominium depend on Omnigent.
Do not equate external sessions with canonical WorkUnits.
Do not expose canonical workspaces as writable to workers.
Do not build one giant provider interface.
Do not build one giant universal transaction schema.
Do not silently lose translation semantics.
Do not allow package installation to imply admission.
Do not let runtime approval imply transaction approval.
Do not build a marketplace before conformance, signing, revocation, and rollback.
Do not resume bespoke Dominium backend expansion before generic reuse is proven.
```

## Definition Of Success

AIDE reaches this product shape when:

1. One WorkUnit can run through a local process, Omnigent, CI, or a human without
   changing semantic identity.
2. One Dominium capability is usable through Workbench, CLI, MCP, ACP, and a
   legacy bridge without changing capability meaning.
3. Every external translation records semantic fidelity and loss.
4. Every mutation is previewable, scoped, authorized, validated, reversible, and
   evidenced.
5. Every extension is conformance-tested before admission.
6. One agent task can resume on another harness through portable AIDE state.
7. AIDE remains useful with no cloud, no model, no Git, and no live service.
8. RepoGraph and OKF continuously improve context, impact analysis, tests, and
   documentation.
9. Routing improves from measured correctness, cost, latency, privacy, and
   rollback outcomes.
10. Omnigent can be removed or replaced without changing canonical project truth.
11. Dominium remains playable and product-progressing throughout platform
    development.
12. The system materially accelerates development of the actual game and engine.

## Explicit Non-Capabilities Of This Document

This document does not implement, accept, authorize, or evidence:

```text
registered-process provider acceptance
ExecutionHostContract
LocalProcessExecutionHost
Omnigent package admission
live MCP, A2A, or ACP behavior
worker execution
provider or model calls
network calls
Service/runtime behavior
Workbench implementation
PreviewSession implementation
DevelopmentTransaction implementation
PatchTransaction apply
rollback execution
target repository mutation
Dominium mutation
Dominium aggregate validation success
branch or worktree mutation
GitHub mutation
release or promotion
marketplace behavior
```
