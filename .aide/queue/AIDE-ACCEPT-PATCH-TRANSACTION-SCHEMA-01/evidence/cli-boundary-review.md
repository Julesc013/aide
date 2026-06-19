# CLI Boundary Review Evidence

Supported PatchTransaction CLI commands remain:

```text
patch-transaction status
patch-transaction project
patch-transaction validate
```

Unsupported execution-command probes are required to fail closed:

```text
patch-transaction apply
patch-transaction approve
patch-transaction execute
patch-transaction rollback
```

This task does not add or alter CLI behavior.
