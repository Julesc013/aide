# Dominium Registered Validation Backend Acceptance

Result: `ACCEPTED_WITH_WARNINGS`

Accepted capability:

```text
dominium_registered_validation_command_boundary_invocation_v0
```

Accepted meaning:

AIDE has evidence that one narrowly registered Dominium validation command can
be invoked through one bounded local process boundary, with repository preflight,
exact argv, `shell=False`, environment constraints, timeout, typed result or
refusal capture, declared state-probe comparison, evidence, and event
projection.

Warnings preserved:

- observed domain outcome was a typed refusal;
- aggregate validation execution and success are not accepted;
- service-adapter entry is not accepted;
- mutation observation is limited to declared probe coverage;
- local Dominium checkout remained clean but behind `origin/main`.

Next task:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```
