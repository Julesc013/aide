# Source Chain Review

Source-chain checks passed:

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01`: `PASS_WITH_WARNINGS`,
  `missing_evidence: 0`.
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01`: `FAILED_VALIDATION`,
  `missing_evidence: 0`.
- `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`: `PASS_WITH_WARNINGS`,
  `missing_evidence: 0`.
- Build commit, failed-check commit, and repair commit are ancestors of live
  HEAD.
- Repair recommends `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`.
- No later MCP repair check, second repair, acceptance, or superseding task was
  registered before this check.
