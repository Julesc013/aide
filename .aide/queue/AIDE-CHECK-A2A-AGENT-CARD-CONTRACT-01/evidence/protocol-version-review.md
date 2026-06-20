# Protocol Version Review

Material finding `A2A-CHECK-001`: the generated contract does not explicitly record external `target_a2a_protocol_version: 1.0` or `target_a2a_specification_release: 1.0.0`. The only `protocolVersion` found is AIDE compatibility metadata value `0.1.0`, which must not stand in for the external A2A protocol version.
