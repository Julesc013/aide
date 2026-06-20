# Legacy Field Review

Material findings: top-level `url: null` is present, top-level `supportsAuthenticatedExtendedCard: false` is present, and `capabilities.stateTransitionHistory` is emitted as if it were an A2A capability. A2A v1.0 moved endpoint declaration into `supportedInterfaces[]` and extended-card support into `capabilities.extendedAgentCard`.
