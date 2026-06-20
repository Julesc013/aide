# Independent AgentCard Scan

Standard-library JSON inspection, independent of the production A2A helper, parsed 16 A2A JSON files.

Result:

- independent_errors: 0.
- `target_a2a_specification_release`: `1.0.0`.
- `target_a2a_protocol_version`: `1.0`.
- Official AgentCard fields are limited to name, description, supportedInterfaces, version, capabilities, defaultInputModes, defaultOutputModes, and skills.
- Top-level legacy fields are absent.
- Unsupported capability fields are absent.
- Official `skills` is empty.
- Candidate skills remain in outer AIDE metadata only.
