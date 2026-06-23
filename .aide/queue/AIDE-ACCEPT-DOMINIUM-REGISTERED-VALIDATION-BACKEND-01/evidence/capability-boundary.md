# Capability Boundary

Accepted:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

Accepted observed facts:

- `process_started: true`
- `launcher_call_count: 1`
- `structured_output_parsed: true`
- `registered_command_boundary_reached: proven`
- `domain_outcome: typed_refusal`
- `aggregate_validation_executed: false`
- `aggregate_validation_succeeded: false`
- `service_adapter_boundary_reached: unproven`
- `mutation_observation: none_detected_within_probe_coverage`

Not accepted:

- aggregate validation success;
- aggregate validation execution;
- service-adapter entry;
- all internal Dominium service boundaries;
- read-only guarantees outside declared probe coverage;
- general Dominium command execution;
- generic process-provider behavior.
