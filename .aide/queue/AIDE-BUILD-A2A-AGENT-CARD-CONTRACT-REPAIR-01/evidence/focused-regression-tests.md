# Focused Regression Tests

Command:

```bash
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_a2a_agent_card_contract.py
```

Result: PASS.

Focused A2A test count: 66.

Covered repair regressions include:

- explicit external A2A specification release and protocol version pins;
- rejection of `latest` and `0.1.0` as external pins;
- required `supportedInterfaces`;
- no legacy top-level `url`;
- no null `provider.url`;
- no top-level `supportsAuthenticatedExtendedCard`;
- no unsupported `capabilities.stateTransitionHistory`;
- no AIDE governance fields inside official AgentSkill objects;
- official `skills` remains empty while no endpoint exists;
- candidate skills preserved as non-callable AIDE metadata;
- no live endpoint, registration, delegation, network, provider, worker, mutation, or trust behavior;
- unsupported runtime commands fail closed.

The unittest output includes argparse error text for unsupported-command probes. Those probes intentionally invoke invalid A2A runtime verbs and passed because the CLI rejected them with non-zero exit codes.
