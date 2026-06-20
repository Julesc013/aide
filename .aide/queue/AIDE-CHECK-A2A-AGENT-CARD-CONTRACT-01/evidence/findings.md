# Findings

Result: `FAILED_VALIDATION`

- `A2A-CHECK-001`: External A2A protocol version is not pinned - The contract records AIDE compatibility/schema protocolVersion 0.1.0 but no target_a2a_protocol_version 1.0 or target_a2a_specification_release 1.0.0 field was found.
- `A2A-CHECK-002`: Projected Agent Card omits supportedInterfaces - agent-card.preview.json does not contain supportedInterfaces while being emitted as an Agent Card projection.
- `A2A-CHECK-003`: Legacy top-level url placeholder is emitted as null - agent-card.preview.json contains top-level url: null; A2A v1.0 moved endpoint URL into supportedInterfaces[0].url.
- `A2A-CHECK-004`: Provider object has null required URL - provider is present with organization AIDE and url null; A2A AgentProvider requires both organization and url when provider is present.
- `A2A-CHECK-005`: Extended-card capability uses legacy top-level field - supportsAuthenticatedExtendedCard is emitted at the top level; A2A v1.0 places extendedAgentCard under capabilities.
- `A2A-CHECK-006`: Unsupported stateTransitionHistory capability is emitted as A2A capability - capabilities.stateTransitionHistory appears in the projected Agent Card even though the pinned v1.0 capability model contains streaming, pushNotifications, extensions, and extendedAgentCard.
- `A2A-CHECK-007`: AIDE governance fields are embedded inside AgentSkill objects - Each skill contains aide_operation_mapping, implemented, requires_future_capability_grant, requires_future_policy_decision, and side_effect_class inside the AgentSkill object.
- `A2A-CHECK-008`: Unimplemented skills are advertised in an externally shaped skills array - The official-looking skills array lists four skills but all are implemented:false and no endpoint, task delegation, or worker execution exists; conforming clients may ignore implemented:false.
