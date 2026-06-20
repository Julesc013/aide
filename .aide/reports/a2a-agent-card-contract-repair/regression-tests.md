# Regression Tests

Focused A2A regression suite expanded to 66 tests covering version pins, required fields, interfaces, legacy fields, provider, capabilities, skill separation, security/signature boundaries, runtime facts, determinism, and unsupported command rejection.

Final command:

```bash
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py
```

Result: PASS, 66 tests.
