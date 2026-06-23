# Live Invocation Evidence

The single permitted live backend run was:

```text
py -3 .aide/scripts/aide_lite.py dominium-registered-validation run
```

Observed:

- Dominium CLI process count: `1`
- `shell`: `false`
- argv template: `<python> apps/workbench/module/validation/cli.py --repo-root <pinned-dominium-root> --target all --profile FAST --surface aide --mode dry_run`
- `--write-reports`: absent
- `--json-out`: absent
- stdout JSON parsed: `true`
- Dominium command status: `refused`
- AIDE result origin: `dominium_stdout_json`
- checkout state unchanged: `true`
- fixture callable used as executor: `false`

Dominium returned a typed refusal:

```text
aggregate validation suite service is not bound in the Workbench validation slice
```

That is recorded as `PASS_WITH_WARNINGS` for the build proof because the task
required a typed Dominium result or refusal from the real command boundary, not
successful aggregate validation.

The initial live CLI wrapper exited nonzero after the one process because the
AIDE-side report validator ran before markdown companion files existed. The
reports were refreshed from the captured invocation record and validated without
rerunning the Dominium process.
