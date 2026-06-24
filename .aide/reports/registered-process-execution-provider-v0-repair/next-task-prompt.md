# AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Create and process `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.

Repo truth outranks this prompt. Inspect
`AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`, its source
check, implementation diff, focused tests, repair reports, task evidence, queue
policy, queue index, `PLANS.md`, and `IMPLEMENT.md`.

This is an independent check-only task. Do not repair implementation.

Verify that the repair closes all five material findings:

- mismatched capability/provider/spec bindings launch zero processes;
- receipt launch accounting and metadata are per invocation;
- decoder exceptions and undecoded outcomes do not report complete validation or evidence axes;
- state-probe failure fails closed and preserves no typed domain result;
- cancellation is either implemented or explicitly declared unsupported.

Also verify genericity, Dominium parity, no capability widening, no live Dominium
rerun, no target repository mutation, complete evidence, focused tests, broad
validation, scrubbed reports, and diff checks.

If the repair passes, recommend exactly:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

If material findings remain, recommend exactly:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02
```
