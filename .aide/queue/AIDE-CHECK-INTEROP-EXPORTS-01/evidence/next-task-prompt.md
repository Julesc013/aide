# AIDE-ACCEPT-INTEROP-EXPORTS-01

Create and process `AIDE-ACCEPT-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

This is an acceptance/consolidation task for static interop export previews.

Review `AIDE-BUILD-INTEROP-EXPORTS-01` and
`AIDE-CHECK-INTEROP-EXPORTS-01`. Accept only static, deterministic,
report-only interop export previews if both tasks remain complete with
`missing_evidence: 0` and no material finding exists.

Do not implement live MCP, live A2A, Host Contract, Dominium Bridge
conformance, Workbench, runtime, worker execution, provider/model/network calls,
PatchTransaction apply, branch/worktree automation, GitHub mutation, release,
promotion, or target-repository mutation.

If accepted, recommend:

```text
AIDE-BUILD-MCP-SERVER-CONTRACT-01
```
