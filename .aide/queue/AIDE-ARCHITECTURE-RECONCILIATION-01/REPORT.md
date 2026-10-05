# AIDE architecture and independent development report

## Later checkpoint — 2026-10-05

The original reconciliation below is retained as its dated source/evidence
snapshot. Later work qualified bounded C1 evidence dependencies, a C8 inspection
view and finite C4 custody; this does not adopt all12 candidates or the19 draft
architecture refinements. C4 passed23 native/public-CLI regressions and two live
custody operations, preserving all receipts/evidence and saving7,921,599 logical
bytes. Current affected source at eea174be passed67 fresh checks and full
validation; collection/retirement are independently accepted. A separately accepted pure export at cf234547 resolved provenance;849 checksums,
complete collection/retirement and clean-source identity verify.
The existing7132 ZIP predates custody and still needs current consumer/replay
acceptance. C4 integration and stable certification remain unfinished.

[Current delivery report](../AIDE-STABLE-LITE-RELEASE-EFFECT-01/REPORT.md),
[custody report](../AIDE-RETIRED-EVIDENCE-CUSTODY-01/REPORT.md) and the
[staged roadmap](../../../docs/roadmap/staged-expansion-roadmap.md) carry current
facts and next bounded candidates. Outer-client setup, historical dispositions,
live/matched efficiency, publication/download and wider cleanup remain separate;
FacMan product work remains paused. Preserve the original244 UR/UC and proposed
versus adopted semantics described below.


Date: 2026-10-04, Australia/Sydney. Source baseline:
`3d186d0584bb40f18402a626c9fe099260fae3d4`.

## Outcome and scope

There is useful development independent of the blocked release campaign.
The best next increments strengthen the existing control plane: accurate truth
projections, compatibility, portable checkpoints, owned resource retirement,
explainable status and small role-specific conformance suites. Shared inference,
networked ownership, learning and managed scale extend those foundations through
separately qualified profiles; they do not require another AIDE implementation.

This task reads the supplied architecture review, reconciles affected specs and
plans, and corrects concrete status contradictions. It appends proposed
refinements to 19 existing topic owners, preserving their original text and
requirement/case statements. Eighteen are imported drafts; the product-scope
appendix is also explicitly proposed. No runtime feature, schema adoption,
host configuration, model grant, support tier or release effect is introduced.

The blocked release Goal remains dormant. The current outer client is still
unrestricted. This documentation work is not the requested future constrained
development acceptance, and no command-only result closes the editor boundary.

## Current capability: source, evidence and limits

Recorded results below were inspected, not rerun as behavioral tests in this
task. Current doctor/validate and documentation checks establish their own
narrower structural properties. Review records whose terminal queue flag remains
needs_review are described as recorded reviews, not silently converted to passed.

| Area | Current evidence | Qualification limit / remaining work |
|---|---|---|
| Repo-native work and authority | [Work/attempt contract](../../../specs/control-plane/contracts/work-attempts-and-decomposition.md), [authority contract](../../../specs/control-plane/contracts/authority-and-decision-provenance.md), filesystem queue and policies | Adopted desired behavior is separate from every operation's actual grant |
| Capability and conformance | [CapabilityManifest source](../../../core/protocol/capability_manifest.py), [ConformanceProfile](../../../core/protocol/conformance_profile.py), [ConformanceResult](../../../core/protocol/conformance_result.py); recorded acceptance reviews | Declaration/schema/projection exists; it does not execute a capability or certify a host |
| Context and knowledge | [ContextPack v2](../../../core/protocol/context_pack_v2.py), source-linked context tools and OKF | Projection exists; actual rendering/token/permission and memory effectiveness remain separate |
| Truth reconciliation | [Reconciler](../../../core/reconciler/reconciler_reports.py), [knowledge truth](../../../core/reconciler/doc_knowledge_truth.py), [capability ledger contract](../../../docs/reference/capability-reality-ledger.md) | Report-only implementations exist; no automatic repair or second status authority |
| Controlled effects | [PatchTransaction](../../../core/protocol/patch_transaction.py), [bounded executor](../../../core/apply/transaction_executor.py), [AdapterManifest](../../../core/protocol/adapter_manifest.py) | Schema and bounded source do not grant general apply, install or live-adapter authority |
| Local Windows lifecycle | Portable importer/update, repair, rollback/removal and partial-recovery source; [stable-effect task](../AIDE-STABLE-LITE-RELEASE-EFFECT-01/ExecPlan.md) | Delivered candidate has recorded local consumer evidence; exact published/downloaded support remains unfinished |
| Worker and resources | [Managed owner](../../../core/execution/managed_workspace.py), [scoped adapter](../../../core/execution/scoped_host.py), [recorded public-job outcome](../AIDE-SCOPED-JOB-ENTRY-01/evidence/outcome.md) | 64 recorded regressions/export/validate and retirement qualify the bounded worker; aggregate disk admission is monitored/cooperative, not a hard quota |
| Outer client | [Route observations](../AIDE-SESSION-CONTAINMENT-01/evidence/outer-launch-boundary.md) | Ordinary command execution excluded reads/writes; direct sandbox read and native filesystem API probes did not. Actual model editing route and client controls remain unresolved |
| Source integration | [Source-sync plan](../AIDE-MAIN-BRANCH-SYNC-01/ExecPlan.md) | Main/dev were synchronized; 84 matching pairs means corresponding local/remote refs, not identical tips across all branches |
| Storage reclamation | [Bounded ownership evidence](../AIDE-SESSION-CONTAINMENT-01/evidence/storage-ownership-followup.json) | Two private archive names share one file with two links; distinct Git/package material is preserved. Logical size is not measured reclaimable allocation |
| Model binding and usage | [Efficiency task](../AIDE-LITE-EFFICIENCY-01/ExecPlan.md), opt-in binding/context/usage source | Actual authorized live invocation and matched accepted-outcome proof remain pending; source/synthetic checks are narrower |
| Runtime/broker | [Current runtime overview](../../../core/runtime/README.md), local worker/broker source and scoped queue records | Source foundations exist; no general unattended service, fleet or native/hosted effect qualification is inferred |
| Native/legacy lanes | [Support policy](../../../governance/support-policy.md), [capability levels](../../../governance/capability-levels.md), exact inventories/matrices | Each lane needs its own T0–T5 posture, state/mode and L0–L4 ceiling; shared core does not imply parity |
| Publication | Existing stable candidate and exact effect gates | No stable tag/publication/downloaded-consumer completion is claimed; ZIP still predates the new scoped adapter |

## Contradictions addressed

The README called CapabilityManifest, ConformanceProfile, PatchTransaction,
AdapterManifest, ContextPack v2 and report-only Reconciler wholly planned despite
existing source and recorded reviews. It described WorkerRun as having no worker
runtime while its opening described runtime foundations. Those claims now name
the actual declaration/projection/bounded source and retain operational limits.

The Profile's focus still pointed to Q31; its runtime value said not implemented.
The focus now identifies this independent reconciliation, with bounded worker
foundations and unresolved outer/live/release qualification. Older foundation
awaiting-review fields are reconciled with the recorded QFIX-03 notes already
represented in future_intent. Q36 is compile-only implemented/needs-review, not
planned or execution authority. Target-owned pilot review status is preserved.

The existing capability scan/ledger/validation passed for 47 observations and
13 conservative seed records. That report-only projection is reused rather
than creating another status store; its coverage remains narrower than an
exhaustive current runtime/support map. Eleven unchanged implementation source
identities are bound in [source-crosswalk.json](evidence/source-crosswalk.json).

The runtime README still described Q02's placeholder as current reality. It now
preserves that history while acknowledging later bounded source. Roadmap text
distinguishes the helper CLI from the later Service and generalized Runtime.
Its foundation target is not described as an already shipped product.

Import-time custody and current edited-byte identity are now distinguished.
The original import manifest remains unchanged. The new
[amendment manifest](../../../specs/control-plane/amendment-manifest.json) binds
the 19 current Git-LF documents and their baseline; original UR/UC statements
are retained. Historical six-foundation byte-preservation claims are explicitly
scoped to the import, because product scope now has a proposed appendix.

## Architecture review dispositions

| Review topic | Disposition and existing owner |
|---|---|
| Durable work versus replaceable machinery | Clarify product/module boundaries; retain one implementation and current .aide/ ownership |
| Compatibility beyond parsing | Extend compatibility owner with readability, round trip, operation, behavior, deployment and migration distinctions |
| Worker/session/request/model/allocation | Refine execution owner; cancellation of one request cannot own a shared server's lifetime |
| Laptop through enterprise compositions | Proposed independent configuration axes; exact profile qualification, no hardware-size trust tiers |
| Hardware and resource evolution | Backend-owned topology/estimates, four independent eligibility questions, aggregate admission and explicit enforcement class |
| Durable/distributed ownership | Portable checkpoints, one writer/partition, fencing, cancellation, reconnect and uncertain effects; no new competing task store |
| Model and learning lifecycle | Separate discovery/acquisition/qualification/activation; scoped lessons and optional dataset/adaptation provenance, held-out evaluation and retirement |
| Authority and optimization | Preserve lead/descendant controls, distinguish experiment from acceptance, and measure whole accepted outcome |
| Extensions and external standards | Narrow role contracts, explicit semantic losses, version-pinned conformance and contributor reference fixtures |
| Operator experience | Explain actual state/location/authority/uncertainty/action with progressive disclosure and side-effect-free status |
| Incremental delivery | Existing module seams, CLI characterization and dependency-ranked candidates; no rewrite, swarm or speculative service stack |
| Cross-cutting proof | Sleep/restart, stale/uncertain effects, shared cancellation, recipe changes, exhaustion, cross-version reads, allowance failures and learner/evaluator separation remain planned cases |

Detailed content lives in the 19 original topic files, not in a replacement
specification or a new parallel architecture. Proposed refinements remain
subject to separate semantic adoption and source-bound implementation admission.

## What can be developed independently

The [staged plan](../../../docs/roadmap/staged-expansion-roadmap.md) provides
12 bounded candidates with existing owners, prerequisites and acceptance:

1. **C1 truth projections:** connect existing capability/reconciler views to
   current source and qualification dependencies; prevent a schema, test fixture
   or recorded review from becoming a whole-host claim.
2. **C8 explainable operations:** extend existing status/doctor/task views with
   effective configuration provenance and one precise resume condition. Keep
   ordinary inspection free of downloads, paid requests and mutation.
3. **C2 compatibility codecs:** preserve safe unknown data and refuse unknown
   required security semantics using older/newer fixture pairs.
4. **C3 portable checkpoints:** preserve objectives, exact facts/artifacts,
   effects, questions and remaining obligations across interruption or backend
   removal, without copying private session history or allocating a new checkout.
5. **C4 resource/retirement explanation:** build on managed receipts and metadata
   to distinguish real ownership, links and recoverable bytes. Discovery is
   independent; deletion still requires exact proven disposal authority.
6. **C9 contributor conformance:** one small role reference, packaging guide and
   failure suite over existing declaration/conformance owners; no marketplace or
   every language SDK before a real consumer.
7. **C11 recipe invalidation:** bind model/template/runtime/hardware/tools and
   check dependencies, preserving unrelated valid source evidence.
8. **C5 request lifecycle:** specify and fixture-test logical-worker/shared-model
   cancellation before attempting actual shared inference.
9. **C6 asset metadata:** model/dataset/adaptation lineage and transition records
   without downloads, training, activation or new inference calls.
10. **C7 lesson correction:** scoped applicability, retirement, index invalidation
    and protected evaluation ownership; weights are optional future artifacts.
11. **C10 characterization:** measure one existing CLI use case and its contract
    before an admitted extraction. Size alone does not justify a rewrite.
12. **C12 attribution:** extend current usage reconciliation/reservations only
    where actual coverage is missing; count cumulative/shared costs once and
    retain failures/unknowns. Actual efficiency claims still require measurements.

The recommended first combination is C1/C8, followed by C2/C3/C4. The remaining
candidates can run when their independent consumers and prerequisites are ready.
This task defines those candidates; it does not admit their implementation en
masse or prescribe additional model invocations.

## What remains dependent on operational input

Ordinary client qualification needs the actual outer application, model editing
routes and effective task source/output scope. Retain the existing shell proof,
identify trusted management versus model-accessible filesystem routes, and run
one permitted edit/check/collect/retire workflow after supported setup changes.
Do not repeat the unchanged client question, probes or worker rewrite here.

Real model/worker replacement needs separately authorized complete bindings and
same-outcome evidence. Networked execution needs admitted nodes, authenticated
ownership generations, cancellation, duplicate/uncertain effect, reconnect and
partition proof. Controlled training needs data authority, held-out evaluation,
activation and rollback. Managed scale needs tenant isolation, restoration and
measured capacity. Native/legacy work needs its exact environment/lane admission.

These are separate profile dependencies. Fleet, training, every IDE and enterprise
scale do not become mandatory features of the first local Windows Lite release.
Historical owner decisions, live/matched qualification and exact stable effect/
downloaded-asset checks remain the release task's recorded separate gates.

## Verification and practical limits

Baseline doctor, validate and context pack completed successfully; full bounded
outputs and hashes are in evidence/baseline-checks.json and adjacent logs. Final
structural/provenance/link/claim checks and generated-view validation are recorded
in [validation.md](evidence/validation.md). Existing worker tests are unchanged
recorded evidence; they are not rerun merely because prose changes.

The architecture attachment was read in full initially (32,307 observed bytes).
Its client-managed file later became unavailable while capturing provenance.
The exact raw attachment SHA remains unknown and is explicitly null; no digest
or replacement source copy was invented. Current edited spec identities are
verified independently. This limitation must be resolved before any later
adoption that requires exact raw-source custody.

This is an affected-document and declaration reconciliation, not an exhaustive
audit of every source line, old archive or historical record. It does not prove
perfect software, production isolation, future hardware compatibility, live
efficiency or released support. Controller/reviewer inference and any unknown
usage are not represented as zero; this task is not an efficiency benchmark.
No broad disk scan, new worktree, source archive, machine policy change or target
product development is performed. See [remaining risks](evidence/remaining-risks.md).

## Independent acceptance

Frozen documentation source `afd9dfdc80387b19411dd148d74120731f5a0ba2` and its
dev-only effect received [independent ACCEPT_WITH_NOTES](evidence/independent-review-afd9dfdc.md).
All notes are explicitly nonblocking for that source/effect: preserve unknown
raw-source custody, separate proposal admission and every operational gate.
Record-only successors require focused exact rereview before the declared dev
effect; main and stable qualification are outside this documentation integration.
