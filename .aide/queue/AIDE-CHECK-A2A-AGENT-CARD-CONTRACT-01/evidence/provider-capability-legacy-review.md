# Provider Review

Material finding `A2A-CHECK-004`: `provider` is present, but `provider.url` is `null`. For the pinned AgentProvider shape, present provider objects require non-empty `organization` and `url`. The check did not fabricate a URL.

# Capability Review

`streaming` and `pushNotifications` are false and no endpoints exist. However, `stateTransitionHistory` is emitted in the A2A capabilities object and `extendedAgentCard` is not used. This is standards-alignment debt requiring repair.

# Legacy Field Review

Material findings: top-level `url: null` is present, top-level `supportsAuthenticatedExtendedCard: false` is present, and `capabilities.stateTransitionHistory` is emitted as if it were an A2A capability. A2A v1.0 moved endpoint declaration into `supportedInterfaces[]` and extended-card support into `capabilities.extendedAgentCard`.
