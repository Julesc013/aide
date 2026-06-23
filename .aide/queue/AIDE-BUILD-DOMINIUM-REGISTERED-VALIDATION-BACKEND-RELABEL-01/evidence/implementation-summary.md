# Implementation Summary

The active registered-validation backend now proposes:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

The code records the prior label as superseded data, not as the active label.

The active report generator now classifies boundary facts independently:

- process and transport facts come from the process launch and parsed stdout.
- registered command boundary is proven only when Dominium stdout names
  `dominium.validation.run`.
- service-adapter boundary is `unproven` unless Dominium output emits that
  exact boundary.
- aggregate-validation execution and success remain false for the observed
  typed refusal.
- mutation observation is scoped to declared Git and implementation-digest
  probes.

The active reports were regenerated from saved invocation artifacts. The live
Dominium CLI was not rerun.
