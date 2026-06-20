# Validation

Validation run before final evidence inspection:

- `git status --short --branch`: clean on `main`
- `git diff --check`: pass
- `git diff --cached --check`: pass
- `py -3 -m py_compile core/interop/mcp_server_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_mcp_server_contract.py`: pass
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py`: 41 tests passed
- `py -3 .aide/scripts/aide_lite.py mcp-server-contract status`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py mcp-server-contract project`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py mcp-server-contract validate`: `PASS_WITH_WARNINGS`
- predecessor validators: pass with warnings where expected
- MCP JSON parse sweep: 32 JSON files parsed
- independent fixture probes: `FAILED_VALIDATION`
- unsupported operation probes: fail closed
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-MCP-SERVER-CONTRACT-01`: complete
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-MCP-SERVER-CONTRACT-01`: `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-MCP-SERVER-CONTRACT-01`: complete
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-MCP-SERVER-CONTRACT-01`: `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`
- `.aide/reports/mcp-server-contract-check/check-report.json`: parses
- secret-like scan over changed and untracked files: `0` findings

`git diff --check` exited successfully while preserving the existing
`.aide/queue/index.yaml` CRLF normalization warning.
