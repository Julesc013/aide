# AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Create and process `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

Repo truth outranks this prompt. Build a narrow registered validation backend
that proves exactly one bounded local read-only invocation of Dominium's
`dominium.validation.run` command through:

```text
apps/workbench/module/validation/cli.py
-> run_validation_command()
-> ValidationServiceAdapter
```

The exact live argv must be equivalent to:

```text
<python>
apps/workbench/module/validation/cli.py
--repo-root <pinned-dominium-root>
--target all
--profile FAST
--surface aide
--mode dry_run
```

Use `subprocess` with `shell=False`, an exact allowlisted Python executable and
script path, a bounded timeout, separate stdout/stderr capture, and sanitized
environment including `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`,
`PYTHONUTF8=1`, and `PYTHONHASHSEED=0`.

Do not pass `--write-reports` or `--json-out`. Dominium must remain unchanged.

Unsupported capabilities and invalid AIDE requests must refuse before process
creation. Success must originate from Dominium stdout JSON, not a constructed
static success result. Focused tests must use an injected fake runner instead
of repeatedly invoking the live checkout.

Proposed capability label:

```text
live_dominium_validation_command_readonly_v0
```

This label remains unaccepted until independent check and acceptance complete.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```
