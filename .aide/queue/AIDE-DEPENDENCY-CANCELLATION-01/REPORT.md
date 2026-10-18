### Independent cooperative cancellation

**Result.** Explicit v2 request configuration supports sender cancellation and
recipient acknowledgement through the existing ledger, CLI and MCP tool.
Cancellation binds the exact request, participant and observed stage; retries
preserve records, conflicts refuse, and normal advancement stops. V1 behavior
is unchanged; old readers reject v2. No live ledger was initialized or migrated.

**Evidence.** All 73 source regression methods passed, including the unchanged
60 original methods. An additional actual fresh-process CLI/MCP workflow cancelled
one accepted request, retained an uncertain acknowledgement and completed adoption
of a second request. Native tasks, attempts, effects and controls stayed unchanged.
The exact old reader accepted v1 and refused v2 without ledger mutation.

**Package and preview.** Six ownership checks passed. The existing exporter,
doctor, full validation and pack status passed; only the manifest source commit
changed. All 867 payload/static members and eight frozen release assets retained
their bytes. The five-commit preview through a672797f regenerates all six outputs
exactly; the later closure commit receives its own strict check. The runtime
cancellation feature is source-only and is not added to published Lite archives.

**Retained corrections.** Initial full validation exposed two stale pack-provenance
assertions; the original failed output remains in provenance-failure.json. Independent
review caught a missing export reservation before execution; the initial template,
map and REQUEST_CHANGES remain. The corrected reservation reused the existing
8 MiB total. These corrections consumed no additional job; all three actual jobs
passed, their collections were verified, and workers, scratch and reservations retired.

**Existing warning.** Full validation retains the unrelated missing review-packet
reference `.aide/prompts/evidence-review.md`. This child has explicit independent
reviews. No warning is counted as a pass or used to widen authority.

**Integration.** Exact terminal review and integration-effect.json govern guarded,
nonforce dev/main synchronization. The local integration receipt records observed
effects; remote Git refs establish published branch state. Retain the pending
publication branch at f708e8c6 and qualification branch at dfae9356. Retire only
this local task branch after both updates and postchecks pass.

**Limits.** An acknowledgement is an attributed claim, not enforced termination,
quiescence or independent verification. Uncertain effects require native recovery.
No host wake-up, shared-service cancellation, live downstream work or model call
was performed. Whole-outcome model usage remains unknown. Lite publication still
requires interactive authentication; refresh its ref guards after this integration.
