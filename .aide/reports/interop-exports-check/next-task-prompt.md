# AIDE-ACCEPT-INTEROP-EXPORTS-01

Create and process `AIDE-ACCEPT-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

This is an acceptance/consolidation task for the static interop export previews.

Do not execute this acceptance until:

- `AIDE-BUILD-INTEROP-EXPORTS-01` exists and is complete at `needs_review`;
- its result is `PASS` or `PASS_WITH_WARNINGS`;
- `AIDE-CHECK-INTEROP-EXPORTS-01` exists and is complete at `needs_review`;
- its result is `PASS` or `PASS_WITH_WARNINGS`;
- both tasks report complete evidence with `missing_evidence: 0`;
- no unresolved interop export repair or superseding task exists.

Acceptance scope must remain limited to static, deterministic, report-only
interop export previews.

Acceptance must not imply:

- live MCP server;
- live A2A endpoint;
- provider, model, Gateway, GitHub, or network calls;
- worker execution or dispatch;
- Host Contract or Host SDK;
- Dominium Bridge conformance;
- Workbench, Commander, Service, scheduler, leases, supervisor, or runtime;
- PatchTransaction apply, approval, rollback, admission, or trust;
- branch or worktree automation;
- release, promotion, publication, or target-repository mutation.

Allowed changes should be limited to acceptance task packet/evidence,
`.aide/reports/interop-exports-accept/**`, `.aide/queue/index.yaml`, `PLANS.md`,
and `IMPLEMENT.md`.

Stop at `needs_review`.

If accepted, recommend:

```text
AIDE-BUILD-MCP-SERVER-CONTRACT-01
```
