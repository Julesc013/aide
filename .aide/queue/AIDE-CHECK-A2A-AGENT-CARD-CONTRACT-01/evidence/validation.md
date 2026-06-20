# Validation

Final validation completed for the check-only task.

## Results

- `git diff --check`: PASS with CRLF normalization notices for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`.
- `git diff --cached --check`: PASS before staging; rerun after staging is required before commit.
- `py -3 -m py_compile core/interop/a2a_agent_card_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_a2a_agent_card_contract.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py`: PASS, 28 tests.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract validate`: PASS_WITH_WARNINGS.
- Predecessor validators for MCP server contract, ContextPack v2, AdapterManifest, PatchTransaction, ReferenceID, EventRecord, CapabilityManifest, ConformanceProfile, ConformanceResult, OKF, and Reconciler: PASS or PASS_WITH_WARNINGS as expected for accepted warning posture.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`: PASS, build evidence complete.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`: PASS, check evidence complete.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

## Independent Checks

- Parsed 16 generated A2A JSON files under `.aide/interop/a2a/`, `.aide/reports/a2a-agent-card-contract/`, and `.aide/reports/a2a-agent-card-contract-check/`.
- Reproduced 8 material A2A standards-alignment findings without importing `core/interop/a2a_agent_card_contract.py`.
- Confirmed unsupported runtime commands fail closed for 13 probed operations.
- Secret-like scan over changed files reported 0 high-confidence findings.
- Diff checks against `.aide/interop/a2a/**`, `.aide/reports/a2a-agent-card-contract/**`, accepted Interop Export A2A preview, and MCP acceptance reports produced no unexpected changes.

## Result

`FAILED_VALIDATION`.

The A2A build remains contract-only and projection-only, but it is not acceptance-ready until the material Agent Card standards defects are repaired.
