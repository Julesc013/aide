# AIDE-CHECK-MCP-SERVER-CONTRACT-01
# Independent Check of Minimal Contract-Only MCP Projection

Use `.aide/queue/index.yaml` as canonical queue truth.

Check `AIDE-BUILD-MCP-SERVER-CONTRACT-01` without modifying the MCP contract implementation.
Verify schema/helper alignment, protocol/version pinning, JSON-RPC fixtures, catalogue consistency, refusal fixtures, transport and authorization boundaries, deterministic projection, source immutability, and explicit non-capabilities.

If no material issue exists, recommend `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.
If a material defect exists, recommend one bounded repair task.
