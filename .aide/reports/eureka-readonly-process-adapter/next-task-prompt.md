# AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01

Create and process `AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01`.

Independently check `AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01`.

Verify the selected Eureka command is an existing Eureka-owned read-only JSON command,
the result originates from Eureka output, exactly one allowlisted process launches with
`shell=False`, invalid preconditions launch zero processes, the Eureka checkout remains
unchanged within declared probe coverage, committed evidence is scrubbed, provider core
remains unchanged, and the provider remains proposed and unaccepted.

If material findings remain, recommend exactly:

AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-REPAIR-01

If the check passes, recommend exactly:

AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
