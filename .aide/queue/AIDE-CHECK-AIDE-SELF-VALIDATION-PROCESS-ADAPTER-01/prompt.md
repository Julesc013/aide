# AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Create and process `AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Repo truth outranks this prompt. Inspect the source build task, commit
`d9cb3df8dbb9274b618956d6069666f4f4274528`, its task packet, status, reports,
evidence, implementation diff, focused tests, queue policy, queue index,
`PLANS.md`, and `IMPLEMENT.md`.

This is an independent check-only task. Do not repair implementation.

Verify the self-validation adapter uses the proposed generic provider without
changing or widening provider behavior; remains AIDE-specific; uses exact
allowlisted `aide_lite.py validate` argv with `shell=False`; launches exactly
once for the valid proof; refuses invalid requests before launch; avoids
recursive self-dispatch; preserves transport/process/decoder/domain/evidence
axes; derives success from AIDE validation output; leaves workspace state
unchanged within declared probe coverage; produces deterministic receipt and
projection data; leaves no report churn, absolute local paths, or secret-like
values; preserves generic provider and Dominium parity tests; and keeps the
provider proposed and unaccepted.

If material findings remain, recommend exactly:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-REPAIR-01
```

If the adapter passes, recommend exactly:

```text
AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01
```

Do not accept `RegisteredProcessExecutionProvider v0` in this task. Stop at
`needs_review` with complete independent evidence.
