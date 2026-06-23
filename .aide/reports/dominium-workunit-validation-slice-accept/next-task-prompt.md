# AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Create and process `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

Goal:

Prove exactly one invocation of the Dominium-owned
`dominium.validation.run` command through its registered CLI or command
boundary.

Use a pinned, clean Dominium checkout or temporary copy at an explicitly
recorded revision.

Invoke only:

```text
apps/workbench/module/validation/cli.py
```

with an exact argv equivalent to:

```text
<python> apps/workbench/module/validation/cli.py --repo-root <pinned-dominium-root> --target all --profile FAST --surface aide --mode dry_run
```

Use `subprocess` with `shell=False`, exact allowlisted executable and script
path, a bounded timeout, sanitized environment, separate stdout/stderr capture,
typed AIDE result or refusal mapping, revision and implementation digest
evidence, before/after clean-state evidence, EvidencePacket, EventRecord, and a
deterministic projection.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```
