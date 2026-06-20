# Validator Hardening Review

The repair evidence records nine temporary defect-injection probes, all rejected:

- invalid external specification pin;
- invalid external protocol pin;
- missing `supportedInterfaces`;
- legacy top-level `url`;
- null `provider.url`;
- legacy top-level `supportsAuthenticatedExtendedCard`;
- unsupported `capabilities.stateTransitionHistory`;
- official advertised skill while no endpoint exists;
- AIDE governance field inside official AgentSkill.

Focused regression tests also passed with 66 tests.
