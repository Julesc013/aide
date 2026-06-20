# Validation

Result: PASS_WITH_WARNINGS.

Commands run:

- `git diff --check`
  - Exit code: 0.
  - Notes: Git reported CRLF normalization notices for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors.
- `git diff --cached --check`
  - Exit code: 0.
- `py -3 -m py_compile core/interop/a2a_agent_card_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_a2a_agent_card_contract.py`
  - Exit code: 0.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py`
  - Exit code: 0.
  - Result: 66 tests passed.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract status`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract project`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01`
  - Status: needs_review.
  - Classification: complete.
  - missing_evidence: 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01`
  - Evidence files: 29.
  - missing_evidence: 0.

Independent repair-shape checks:

- Parsed 16 generated A2A JSON artifacts.
- Verified official AgentCard field allowlist.
- Verified `supportedInterfaces` exists and the legacy top-level URL/provider/extended-card fields are absent.
- Verified official `skills` is empty.
- Verified four candidate skills remain in AIDE metadata only.
- Verified high-confidence secret-like scan over changed files found 0 findings.
- Verified unsupported runtime commands fail closed.
- Verified repeated projection bytes are identical across 28 generated A2A projection/report files.

Next serialized task: `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01`.
