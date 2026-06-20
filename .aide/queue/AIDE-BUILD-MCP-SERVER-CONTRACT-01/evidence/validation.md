# Validation

Validation completed:

```text
git status --short --branch
PASS

git diff --check
PASS

git diff --cached --check
PASS

py -3 -m py_compile core/interop/mcp_server_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_mcp_server_contract.py
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py
PASS, 41 tests

py -3 .aide/scripts/aide_lite.py mcp-server-contract status
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py mcp-server-contract project
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py mcp-server-contract validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py context-pack-v2 status
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py adapter-manifest validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py patch-transaction validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py reference-id validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py event-record validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py capability-manifest validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py conformance-profile validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py conformance-result validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py okf validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py reconciler validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-MCP-SERVER-CONTRACT-01
PASS, classification complete

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-MCP-SERVER-CONTRACT-01
PASS, missing_evidence: 0

py -3 .aide/scripts/aide_lite.py validate
PASS
```

Additional probes:

```text
JSON parsing for .aide/interop/mcp/**/*.json and .aide/reports/mcp-server-contract/*.json
PASS, 32 files

Unique resource URI check
PASS

Unique tool-name check
PASS

Resource URI containment/traversal review
PASS

JSON Schema-object review for tool inputs
PASS

Lifecycle and fixture JSON-RPC review
PASS

Capability/catalogue consistency review
PASS

Refusal fixture review
PASS

Transport/runtime status contradiction review
PASS

No-live-endpoint scan
PASS

No-mutation-tool scan
PASS

Unsupported start/serve/connect/call/listen/install command probes
PASS

Repeated-projection byte comparison
PASS

Interop Export source-byte comparison before/after projection
PASS
```

No unrelated generated churn remains after validation.
