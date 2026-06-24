# AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Create and process `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.

Repo truth outranks this prompt. Inspect the repair task, source failed check,
implementation diff, focused tests, repair reports, task evidence, queue policy,
queue index, `PLANS.md`, and `IMPLEMENT.md`.

This is an independent check-only task. Do not repair implementation.

Verify closure of all five source findings:

- binding mismatches launch zero processes;
- launch accounting and launch metadata are per invocation;
- decoder failures do not report complete validation/evidence axes;
- state-probe failures fail closed and preserve no typed domain result;
- cancellation is implemented or explicitly declared unsupported.

Also verify genericity, Dominium parity, no capability widening, scrubbed
reports, focused tests, broad validation, task evidence, and diff checks.

If the repair passes, recommend exactly:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

If material findings remain, recommend exactly:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02
```
