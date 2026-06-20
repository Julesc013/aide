# Validation

Commands run:

- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 -m py_compile core/interop/a2a_agent_card_contract.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_a2a_agent_card_contract.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py`: PASS, 66 tests.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py a2a-agent-card-contract validate`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, exit code 0.

The unittest output includes argparse errors for unsupported runtime verbs; those are expected fail-closed probes and the test process exits successfully.
