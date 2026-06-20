# AIDE-CHECK-MCP-SERVER-CONTRACT-01

Create and process `AIDE-CHECK-MCP-SERVER-CONTRACT-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

Independently check the minimal contract-only MCP projection created by
`AIDE-BUILD-MCP-SERVER-CONTRACT-01`.

Verify:

- source-chain integrity and missing evidence;
- schema/helper/CLI alignment;
- target MCP protocol version `2025-11-25` and JSON-RPC `2.0`;
- lifecycle, resource, tool, prompt, refusal, transport, and authorization
  fixtures;
- catalogue consistency and fail-closed validation;
- no live server, endpoint, transport, auth, resource serving, prompt serving,
  tool execution, worker dispatch, provider/model/network call, branch/worktree
  mutation, GitHub mutation, PatchTransaction apply, target mutation, release,
  or promotion behavior;
- deterministic projection and source immutability.

If no material issue exists, recommend
`AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.

If a material repairable defect exists, recommend one bounded MCP contract
repair task.

Do not execute the acceptance task in the check turn.
