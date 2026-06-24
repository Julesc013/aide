# AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Create and process `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.

Repo truth outranks this prompt. Inspect the source repair task
`AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`, the source
failed check `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`, commit
`7f043d09ae0c5bbb73d68ad293e6dafaaaa8ddd6`, implementation, focused tests,
queue policy, queue index, `PLANS.md`, and `IMPLEMENT.md`.

This is an independent check-only task. Do not repair implementation and do not
accept the provider.

Verify:

- binding mismatch launches zero processes;
- launch accounting and launch metadata are per invocation;
- decoder failure marks validation/evidence incomplete and preserves no typed
  domain result;
- state-probe failure fails closed and preserves no typed domain result;
- process cancellation is implemented or explicitly unsupported;
- generic provider/protocol code remains free of Dominium, queue, report, and
  domain-specific branches;
- exact argv and `shell=False` behavior remain preserved;
- invalid specs and failed preconditions launch zero processes;
- one valid invocation launches at most once;
- timeout, stream limits, decoder errors, and state-probe failures are
  represented honestly;
- transport, process, decoder, domain, validation, and evidence outcomes remain
  distinct;
- state probes report declared coverage and do not claim universal no-mutation;
- committed summaries are scrubbed of local absolute paths and secret-like
  values;
- receipt and outcome projections are deterministic enough for v0 evidence;
- Dominium parity is preserved without rerunning the live Dominium command;
- focused provider tests, Dominium parity tests, broad validation, and diff
  checks pass;
- explicit non-capabilities remain intact.

Required result:

```text
PASS, PASS_WITH_WARNINGS, REQUEST_CHANGES, FAILED_VALIDATION, or BLOCKED
```

If material findings exist, recommend exactly:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02
```

If the provider repair passes, recommend exactly:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```

Do not accept the provider in this task. Stop at `needs_review` with complete
independent evidence.
