# Exact Invocation

The live process invocation used the registered argv template:

```text
<python> scripts/public_alpha_smoke.py --json
```

Recorded process evidence:

- `process_call_count`: `1`
- `launcher_call_count`: `1`
- `shell`: `false`
- `return_code`: `0`
- `stdout` parsed as Eureka public-alpha smoke JSON.

Invalid capability, identity, revision, dirty checkout, and digest mismatch cases
are covered by fake-runner tests and launch zero processes.
