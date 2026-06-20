# Validation

Validation commands run for this task are recorded in `.aide/reports/a2a-agent-card-contract-accept/test-validation-review.md`.

Initial preflight validation:

- `git status --short --branch`: clean on `main`
- `py -3 .aide/scripts/aide_lite.py task status`: PASS/report-only
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01`: missing evidence 0
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01`: evidence listed, no missing entries
- `py -3 .aide/scripts/aide_lite.py validate`: PASS

Final validation after acceptance materialization:

- `py -3 -c "import json; json.load(open('.aide/reports/a2a-agent-card-contract-accept/acceptance-report.json', encoding='utf-8')); print('json ok')"`: PASS
- `git diff --check`: PASS
- `py -3 -m py_compile core/interop/a2a_agent_card_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_a2a_agent_card_contract.py`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py`: PASS, 66 tests
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract project`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`: `classification: complete`, `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`: evidence listed, no missing entries
- `py -3 .aide/scripts/aide_lite.py validate`: PASS
- Independent structural check over `agent-card.json`, `skill-catalog.json`, the repair-check report, the contract record, and the acceptance report: PASS

The unit suite also confirmed unsupported A2A runtime verbs remain rejected by the CLI parser. A first local independent script required exact equality between the repair runtime facts and acceptance runtime facts; it was corrected to require repair-fact preservation as a subset because acceptance adds the stricter explicit `task_submission_performed: false` non-capability.
