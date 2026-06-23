# AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01

Create and process `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01`.

This is a check-only task. Do not repair implementation.

Independently verify that the active registered Dominium validation backend now
uses:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

Verify that active reports distinguish process launch, transport/JSON parsing,
registered command boundary, service-adapter boundary, aggregate-validation
execution, aggregate-validation success, typed refusal, and probe-scoped
mutation observation. Verify the live Dominium command was not rerun for the
relabel and Dominium remained unchanged.

If all material checks pass, recommend exactly:

```text
AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```
