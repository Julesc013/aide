# AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01

Create and process `AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01`.

Repo truth outranks this prompt. Build a thin Eureka adapter over the unchanged
proposed `RegisteredProcessExecutionProvider v0`.

The requested command `scripts/validate_public_alpha_readonly.py --json` is not
present in the local pinned Eureka checkout. Use the narrowest existing
Eureka-owned deterministic read-only JSON command instead:

```text
python scripts/public_alpha_smoke.py --json
```

Record that substitution explicitly. Do not modify Eureka. Do not accept the
provider. Do not implement a generic command runner. Stop at `needs_review` and
recommend exactly:

```text
AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01
```
