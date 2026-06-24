# Next Task Prompt

```text
Create and process
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01.

Repo truth outranks this prompt.

Repair only the material findings from
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01.

Do not accept the provider.
Do not introduce new execution provider types.
Do not broaden Dominium behavior.
Do not rerun the live Dominium command unless a future task explicitly
authorizes it and records preconditions.

Required repair focus:

- binding/provider/capability mismatch must fail closed before launch;
- decoder exception must not report validation/evidence as complete success;
- state-probe failure must fail closed or clearly mark validation incomplete;
- per-invocation launcher accounting and launch metadata must not be cumulative
  or stale across provider reuse;
- cancellation must either be implemented or declared as an explicit
  non-capability.

Stop at needs_review and recommend exactly:
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```
