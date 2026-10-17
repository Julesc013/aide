# Local dependency request/reply: bounded admission candidate

Parent: AIDE-CONVERGENCE-AND-DELIVERY-01. Child: AIDE-LOCAL-DEPENDENCY-01.
Base: 9605d8e333a1da8f113a2a1b44f88427511fbba2. Prepared 2026-10-17.

## Useful result and existing owners

Implement the first P4.requests increment: a cooperating requester records a
dependency, the designated receiver acknowledges the exact revision, accepts it
against its native work reference, returns a result, and the requester records
its own adoption. Restart and duplicate delivery preserve one logical request.
This is the local recording/interface part of the real FacMan-to-Setup workflow;
actual host delivery and real downstream adoption remain required follow-ons.

Source inspection found `continuous_worker/state.py` owns transactional runtime
state, intents and observations; `workunit_cli.py` owns native AIDE queue creation
and inspection. The integration broker requires an independently reviewed code
candidate and exact dev authority. Do not repurpose or weaken that broker gate.

Extend the existing coordinator state owner with dependency records and a narrow
CLI/API. These records link sender/native receiver work; they do not own task
requirements, acceptance, scheduling, workspace mutation or Git integration.
Reuse State transactions, canonical serialization and event history. Keep the
new lifecycle implementation in one sibling module, not a second service/queue.

## Exact first capability boundary

- Explicit opt-in local initialization pins a small configuration: existing
  state-root identity, named participant bindings, expiry and finite record/body
  limits. Reuse the approved execution control root for fixtures only. No live
  control-root initialization is admitted by this child.
- A binding identifies repository, responsible owner, workspace, host/session
  and ownership generation. This first profile is cooperative: declarations and
  caller identity are not OS authentication, filesystem isolation or evidence of
  a live host. The configuration is immutable in place; changed binding requires
  reconciliation, not a lease timeout or automatic replacement writer.
- Requests carry stable identity, sender work/source reference, recipient,
  objective, acceptance, source/context references and requested completion
  obligations. Same ID/same body reuses; different body conflicts. Amendments
  require a separate attributed successor; this increment refuses in-place edits.
- Recorded, delivered, accepted, returned and adopted are distinct. Every step
  binds the original request digest and current participant binding. Acceptance
  links the receiver's native work; it does not grant execution authority. A
  result contains exact subject/evidence references and explicit completion
  claims; reporting it does not independently verify those claims. Adoption is
  a separate attributed sender observation with its own verification references.
- Refuse stale/mismatched binding/revision, wrong role, out-of-order operations,
  conflicting duplicate observations, unknown required fields/schema, expiry,
  oversized input and exhausted record allowance. Atomic writes leave either
  the original record or the complete new state; queries never deliver or retry.
- CLI status exposes mode=cooperative, the next owner/action, and separates
  reported completion from independently verified effects. It starts no model,
  subprocess, scheduler, watcher, network endpoint or notification loop.

## Allowed implementation paths

- `core/runtime/continuous_worker/requests.py` (new cohesive lifecycle module)
- `core/runtime/continuous_worker/state.py` (only necessary optional-record support)
- `core/runtime/continuous_worker/__main__.py` (local request commands)
- `.aide/scripts/tests/test_dependency_requests.py` (new)
- `.aide/scripts/tests/test_continuous_worker_state.py` (only affected regression)
- `docs/reference/local-dependency-requests.md` (new usage/boundary reference)
- `.aide/queue/AIDE-LOCAL-DEPENDENCY-01/**`
- `.aide/queue/index.yaml`
- parent `ExecPlan.md`, `status.yaml`, and this admission
- `.aide/intake/latest-*`, `.aide/context/latest-task-packet.md`
- existing compiler-owned `.aide/generated/**`, `.aide/reports/capability-*`
- `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`

No other source refactor, canonical WorkUnit schema replacement, broker change,
live registration/contact, target edit, workspace creation/relocation/cleanup,
provider effect, global install, archive/export/release change or protection
change. Existing continuous-worker admissions and runtime pins remain binding;
new source does not silently reactivate an old live configuration.

## Plan, authority and Git

Parent intake conservatively requires split/live-test planning; it does not
authorize raw prompt execution. This child implements only the deterministic
local interface. The existing campaign delegation supplies bounded source and
local branch authority after independent admission. Create/switch to local-only
`task/aide-local-dependency-01` in the sole checkout from the exact base above,
preserving the published DiskEd branch. Classify only the four intake files and
this admission as owned pre-branch edits; fresh helper/ref/job/dispatch checks
must hold. No remote or integration effect follows from this admission alone.

1. Record task/ExecPlan and implement the smallest complete local lifecycle.
2. Check syntax and exact inputs; independently review source and a finite
   managed test effect before execution. Do not claim static checks prove behavior.
3. Exercise both API and actual CLI in disposable state: happy request/reply,
   duplicate and conflicting messages, reopened/fresh-process continuation,
   transactional failure, stale binding, wrong role/revision, bounds and expiry.
   Preserve native task/admission/effect tables and original state regressions.
4. Collect/retire the test job; retain failures and unknowns. Review outcome,
   document commands and precise limitations, commit and prepare exact dev/main
   synchronization. Prepare the actual host-delivery brief after local evidence.

Maximum two new deterministic jobs, each separately source/effect reviewed, under
the existing D runner and unchanged config digest
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90.
Use 1 GiB Job / 180 seconds / 32 MiB scratch / 8 MiB retained limits and existing
reserves. Tests are offline stdlib, no acquisition or model calls. Zero live peer
deliveries and zero live state initializations are admitted. A terminal failed
test may justify one repaired second attempt; no automatic third allocation.

Recovery: preserve initial records and exact failed attempts. Unsupported schema
or changed config fails before any mutation. Never interpret a missing reply as
permission to launch another writer. The existing blocked DiskEd child remains
unchanged. Acceptance here proves the local recording path only; the overall
daily-use goal still needs actual worker delivery and downstream adoption.
