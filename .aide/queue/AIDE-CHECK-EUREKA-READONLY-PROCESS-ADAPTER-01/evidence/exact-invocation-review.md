# Exact Invocation Review

The committed source receipt records:

- `launcher_call_count`: `1`
- `process_call_count`: `1`
- `shell`: `false`
- `return_code`: `0`
- `argv_template`: `<python> scripts/public_alpha_smoke.py --json`

Focused fake-runner tests also verify exact argv, working directory,
environment constraints, timeout behavior, and zero-launch invalid preconditions.
