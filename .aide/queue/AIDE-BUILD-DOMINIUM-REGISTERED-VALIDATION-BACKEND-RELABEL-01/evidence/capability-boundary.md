# Capability Boundary

Accepted by this build task as a proposal only:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

Meaning:

```text
AIDE can invoke the registered Dominium validation command boundary through one
bounded process invocation, receive and preserve a typed Dominium result or
refusal, observe no mutation within declared state-probe coverage, and emit
evidence.
```

Not accepted:

- aggregate validation succeeded
- aggregate validation executed
- `ValidationServiceAdapter` was entered
- every internal Dominium service boundary was reached
- universal read-only behavior outside declared probe coverage
- general Dominium command execution
- generic registered-process provider
- runtime, worker, preview, apply, or rollback capability
