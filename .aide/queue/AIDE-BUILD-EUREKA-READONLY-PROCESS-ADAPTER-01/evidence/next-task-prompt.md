# AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01

Create and process `AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01`.

Independently check `AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01`.

Verify the selected Eureka command is an existing Eureka-owned read-only JSON
command, the result originates from Eureka output, exactly one allowlisted
process launches with `shell=false`, invalid preconditions launch zero
processes, the Eureka checkout remains unchanged within declared probe coverage,
committed evidence is scrubbed, provider core remains unchanged, and the
provider remains proposed and unaccepted.

If material findings remain, recommend exactly:

```text
AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-REPAIR-01
```

If the check passes, recommend exactly:

```text
AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```

Do not accept the provider in this check task.
