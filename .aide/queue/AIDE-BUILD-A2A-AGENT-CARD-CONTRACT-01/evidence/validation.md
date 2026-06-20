# Validation

Completed validation included:

- `py -3 -m py_compile core/interop/a2a_agent_card_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_a2a_agent_card_contract.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py`
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract project`
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract validate`
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract status`
- predecessor validators:
  - `mcp-server-contract validate`
  - `context-pack-v2 status`
  - `adapter-manifest validate`
  - `patch-transaction validate`
  - `reference-id validate`
  - `event-record validate`
  - `capability-manifest validate`
  - `conformance-profile validate`
  - `conformance-result validate`
  - `okf validate`
  - `reconciler validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- JSON parsing for 16 generated A2A schema/artifact/report JSON files
- unsupported A2A runtime-like command probes for `start`, `serve`,
  `register`, `delegate`, `send`, `connect`, and `authorize`
- high-confidence secret-like scan over changed files

Current A2A validation report:

- validation status: `PASS_WITH_WARNINGS`
- errors: `0`
- deterministic projection: `true`
- source artifacts mutated: `false`
- secret-like scan clear: `true`
- recommended next task: `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`

Task evidence reports `missing_evidence: 0`. Broad AIDE validation reports
`PASS`.
