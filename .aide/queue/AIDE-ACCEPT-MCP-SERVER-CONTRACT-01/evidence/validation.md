# Validation

Validation commands run:

- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 -m py_compile core/interop/mcp_server_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_mcp_server_contract.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py`: PASS, 65 tests.
- `py -3 .aide/scripts/aide_lite.py mcp-server-contract status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py mcp-server-contract validate`: PASS_WITH_WARNINGS.
- Predecessor validators: PASS_WITH_WARNINGS where expected.
- JSON parsing for MCP JSON artifacts and reports: PASS.
- Unsupported MCP command probes: PASS fail-closed.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Final task inspect/evidence and commit policy are recorded after materialization.
