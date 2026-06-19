# Next Task Prompt

```text
# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Repair the material PatchTransaction path-scope validation defects:

- path_scope_drive_prefixed_relative_accepted
- path_scope_duplicate_normalization_accepted

Preserve the historical failed check. After repair, run an independent repair
check and only then retry PatchTransaction acceptance. Do not rerun
AdapterManifest build or check until PatchTransaction acceptance succeeds.
```
