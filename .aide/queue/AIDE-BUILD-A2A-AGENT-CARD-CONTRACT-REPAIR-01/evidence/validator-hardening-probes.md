# Validator Hardening Probes

Focused tests and direct validator probes inject missing/malformed version pins, missing/invalid interfaces, legacy fields, provider defects, unsupported capabilities, AIDE fields in official skills, official unimplemented skill overclaim, security/signature overclaims, and runtime true flags; all fail closed.

Direct temporary mutation probes run against an in-memory copy of the repaired record:

- `target_a2a_specification_release: latest` rejected.
- `target_a2a_protocol_version: 0.1.0` rejected.
- missing `supportedInterfaces` rejected.
- legacy top-level `url` rejected.
- null `provider.url` rejected.
- legacy top-level `supportsAuthenticatedExtendedCard` rejected.
- unsupported `capabilities.stateTransitionHistory` rejected.
- official advertised skill rejected while no endpoint exists.
- AIDE governance field inside official AgentSkill rejected.

Probe result: 9 probes, 0 failures.
