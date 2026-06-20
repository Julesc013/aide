# Changed Files

The repair changed only authorized MCP helper/test, affected generated MCP
contract projection files, and task/report/planning surfaces.

Implementation and tests:

- `core/interop/mcp_server_contract.py`
- `.aide/scripts/tests/test_aide_mcp_server_contract.py`

Generated MCP contract artifacts:

- `.aide/interop/mcp/fixtures/*list-request.json`
- `.aide/interop/mcp/fixtures/*list-result.json`
- `.aide/interop/mcp/fixtures/resource-not-found-refusal.json`
- `.aide/reports/mcp-server-contract/fixture-index.json`
- `.aide/reports/mcp-server-contract/fixture-index.md`

Task/report surfaces:

- `.aide/queue/AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01/**`
- `.aide/reports/mcp-server-contract-repair/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
