# Warning Disposition

All warnings are non-blocking for this acceptance.

| Warning | Disposition |
| --- | --- |
| OKF is deterministic knowledge projection only | Non-blocking; this is the accepted capability boundary. |
| OKF pages do not replace protocol, evidence, reference, event, or queue truth | Non-blocking; this preserves authority. |
| Full YAML parser integration is deferred | Non-blocking; stdlib structural frontmatter validation is accepted only for this bounded slice. |
| `.aide/context/latest-task-packet.md` is stale | Non-blocking; live `.aide/queue/` truth was used. |
| Broken links and orphan pages are warning-class | Non-blocking while counts are 0 and no authority overclaim exists. |
| Reconciler is not implemented | Non-blocking; Reconciler Reports is selected as the next queue task. |
| CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 are not implemented | Non-blocking; these are later queue items. |
| Runtime/service/provider/target/release/GitHub behavior remains deferred | Non-blocking; not part of the accepted capability. |

No warning requires OKF hardening or repair before acceptance.
