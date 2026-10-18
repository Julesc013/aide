### Dependency work survives an explicit session replacement

The existing source CLI previews and applies an exact cooperative configuration
reconciliation. Pending request identity, accepted native work, original actor
bindings, cancellations and other requests survive. Expiry renewal and changed
host/session are explicit; native ownership does not transfer.

**Behavior.** The operator reviews a consistent bounded snapshot and exact proposal.
Apply requires pause-dispatch, no active native attempt and no unresolved effect
intent. Ownership, schema, participant identities and resource bounds stay fixed.
Changed host/session requires exactly one generation increment. Old configuration
pins and cached writers refuse after replacement, including after explicit resume.
A lost response can recover the same committed receipt without repeating effects.
Changed state/control history invalidates an unapplied plan. Controls stay paused.

**Qualification.**
- Source b8158911: 73 unchanged methods plus 15 new methods passed; no skips.
- Source 984b47b6: two actual fresh-process CLI/MCP workflows passed. The replacement
  session continued accepted work through return/adoption; another cancellation
  stayed intact. Frozen prior readers preserved v1/v2 renewal and rejected stale
  pins/cached writers after resume.
- Source 09925a0f: six ownership checks, existing exporter, doctor, full validation,
  pack status and fixed four-commit preview passed. All six preview outputs
  regenerate exactly. Only the development manifest source_commit changed;
  all867 payload/static members and eight frozen release assets stayed identical.
- All three allocated jobs passed, were collected/digest-verified and retired.
  Scratch is absent and reservations released. No live ledger or provider was used.

**Scope and limits.** This is a source-runtime, trusted cooperative CLI profile,
not an installed desktop session or native process takeover. No MCP administration
tool was added. The plan streams at most32MiB of logical snapshot data and allows
16 reconciliations; larger histories need a separately reviewed continuation path.
Referenced native decisions are attributed evidence, not independently verified
effects. Whole-outcome controller/review usage remains unknown.

**Validation warning.** Full validation retains one existing review-reference
warning with no failures. The referenced file exists; this report does not
reinterpret that validator finding. This child has its own complete review packet.

**Integration.** Exact terminal acceptance governs closure-source.json and
integration-effect.json. Actual dev/main delivery is recorded in the local
evidence/integration-result.log; this report does not predeclare a push.
Both release task branches remain preserved. Publication still needs authentication
and refreshed guards; public Lite assets are unchanged.
