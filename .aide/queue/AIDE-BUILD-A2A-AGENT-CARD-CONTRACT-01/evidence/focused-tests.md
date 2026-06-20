# Focused Tests

Command:

```bash
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py
```

Result:

```text
Ran 28 tests
OK
```

The tests cover valid projection, stable identity, inactive endpoint facts,
runtime/status fail-closed cases, skill catalogue safety, static preview
consistency, deterministic projection, source immutability, CLI dispatch, and
unsupported runtime-like subcommands.
