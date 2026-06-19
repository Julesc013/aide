# AIDE-CHECK-INTEROP-EXPORTS-01

Create and process `AIDE-CHECK-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

This is an independent check-only task for
`AIDE-BUILD-INTEROP-EXPORTS-01`.

Verify:

- the build task exists and is complete at `needs_review`;
- its result is `PASS` or `PASS_WITH_WARNINGS`;
- task evidence reports `missing_evidence: 0`;
- static preview artifacts exist under `.aide/interop/exports/`;
- preview artifact hashes match `.aide/interop/exports/manifest.json`;
- JSON preview artifacts and JSON reports parse;
- previews preserve queue authority and explicit non-capabilities;
- no live MCP server, A2A endpoint, Host Contract, Dominium Bridge conformance,
  Workbench, worker execution, provider/model/network call, PatchTransaction
  apply, branch/worktree automation, GitHub mutation, release, promotion, or
  target-repository mutation was introduced.

Allowed changes:

- `.aide/queue/AIDE-CHECK-INTEROP-EXPORTS-01/**`
- `.aide/reports/interop-exports-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Do not modify implementation, schema, helper, tests, static preview artifacts,
accepted predecessors, generated OKF pages, runtime, provider, host, VCS,
GitHub, release, or target-repository files.

Stop at `needs_review`.

If no material finding exists, recommend:

```text
AIDE-ACCEPT-INTEROP-EXPORTS-01
```
