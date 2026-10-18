### Preserve dependency work across a changed session

**Objective.** Continue the same cooperative dependency requests when a declared
worker session is replaced or its explicit configuration expires. Extend the
existing Requests ledger and CLI; preserve native work and every original
observation. This contributes to P3 continuation and P4 request ownership.

**Evidence.** At ceac70a6, initialize refuses changed configuration and expired
configuration refuses new observations. Status remains readable. There is no
reconciled replacement path; creating another database would strand pending work.
Publication remains independently pending at f708e8c6. Its old dev/main effect
guards must be refreshed later; no authentication probing or release mutation.

**Design.** Add an explicit operator CLI preview/apply operation, not an MCP
participant tool. Preview binds the exact logical dependency state, current
configuration, proposed configuration, reconciliation references, full controls
sequence and native activity in one consistent read transaction. Stream the sorted
logical rows into a bounded digest; do not put ledger contents into the plan.
Apply rechecks under the existing transaction, requires pause-dispatch and no
active native attempt or unresolved effect intent, and leaves controls paused. A prior heartbeat or model
statement never proves host quiescence or transfers a workspace.

Keep schema, state root, participant identities, repository, owner, workspace and
resource bounds unchanged. Permit a later finite expiry and host/session changes
with exactly one generation increment for each replaced binding. A renewed expiry must be future-valid and never shortened. No downgrade,
arbitrary generation jump, participant removal/addition or schema migration.
Unchanged bindings keep their generation. Reconciliation requires an attributed
decision and evidence references; these are claims, never independently verified
native effects. The operation neither opens evidence refs nor executes commands.

Atomically preserve old/new configuration, exact plan and decision in the existing
event history with configuration replacement. Bound replacement history to 16
operations. Preserve dependency rows, prior events, native tasks/attempts/effects
and controls. Refuse stale plans, stale configuration and conflicting retries.
After uncertain acknowledgement, use the known proposed configuration pin to inspect/replay the exact plan and
recover its retained receipt. An exact already-applied plan returns that receipt
without another event; conflicting or superseded plans refuse. Reconciliation
bypasses only ordinary expiry/resume observation checks, never its own paused
snapshot/effect checks. A retry must not repeat an effect or create another ledger.
Old cached actors/writers and fresh processes with old pins must refuse mutation.
Historical observations retain their original binding identities.

**Scope.** Exact task allowlist. Original request/state/MCP/cancellation tests stay
byte-identical. Source-runtime extension only; no live reconfiguration, dispatch,
host enrollment or native takeover. Existing exporter may refresh provenance, but
every development payload and frozen release asset must remain unchanged unless a
demonstrated affected owner requires a separately reviewed scope amendment.

**Sequence.**
1. Review exact admission; under current shared controls create one local task
   branch from ceac70a6 in this checkout, preserve both release branches, and
   checkpoint only the admitted packet through managed commit creation.
2. Prepare source, focused tests and reference. Freeze exact source and first job.
3. At most three existing managed jobs with unchanged limits: request/MCP/state/
   cancellation regressions plus rebind refusal/recovery tests; a fresh CLI/MCP
   session-replacement workflow; final existing ownership/export/full validation
   and fixed promotion preview. Every allocation and retry requires exact review.
4. Independent closure and exact dev/main integration; verify remote refs and
   retire only this short-lived local task branch. Preserve pending publication.

**Acceptance.** An accepted request survives replacement of its recipient's
declared host/session and expiry extension, then returns a result and is adopted
through fresh processes. Another request, prior cancellation and native tables
remain unchanged. Old credentials/binding pins refuse; matching current pins
continue only after a separate existing resume control. Include expiry, pause,
active attempt, unresolved effect intent, changed snapshot/control sequence, wrong generation/identity/bounds, duplicate
input, two-connection replacement races, pause/resume/pause invalidation, event failure
rollback and interrupted response. Operator-only describes CLI placement, not
authentication. Test stale cached writers after explicit resume; replacement
sessions continue only unfinished stages, preserving original actor bindings.
Native quiescence, external authentication and automatic wake-up remain unclaimed.

**Recovery and stop.** Use disposable owned job fixtures and existing finite
admission/collection/retirement only. Preserve failures; stop on an unexplained
changed subject, failed required check or review finding. No new server, storage
root, paid inference, recurring polling or unqualified downstream adoption.

**Admission and source prepared.** Independent admission accepted the exact map
53409138 and local effect ee349f3b. Managed checkpoint32a9d56a is retained.
Fifteen focused methods and the original73 methods are prepared; no native tests
have run. A separate actual fresh-process workflow remains job2.

**Source job passed.** At b8158911, all88 methods passed without skips.
Job9066a297c95d463ea73d3169b2ed675d is quiescent, collected/digest-verified and
retired; scratch and reservation are gone. The reviewer\'s nonblocking wording
note is clarified: initialization refuses schema/config changes; explicit
reconciliation is separate. Product code and tests are unchanged for job2.
Prepared two actual fresh-process workflows plus frozen old-reader v1/v2
continuity and exact870 pack/eight release checks. No live ledger effect.

**Workflow job passed.** At984b47b6, fresh CLI/MCP replacement and the original
cancellation workflow passed. Frozen prior readers preserve v1/v2 renewal semantics,
reject old configuration/cached writers and accept explicitly current pins.
All870 pack files/eight release assets are unchanged. Jobdcd40a22562d4806b7da946dec485b50
was collected/digest-verified and retired. Prepare the final existing owned export
(provenance only), full validation and fixed preview with 7MiB pack +1MiB preview
canonical reservation; no additional allocation or archive rebuild.

**Final qualification passed.** Job4e1fc979a31a48659a12f61ae28e4aff passed
six ownership checks, existing exporter/doctor/full validate/pack-status and
four-commit exact preview. Only manifest source_commit changed; all867 payload
members/eight frozen assets remain identical. All3 allocations are retired and
collected. Terminal exact review/integration is next; no further native job.
