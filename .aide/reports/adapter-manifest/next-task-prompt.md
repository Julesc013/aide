# Next Task Prompt

```text
# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Repair the material PatchTransaction path-scope validation defects preserved by
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01 and AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01.

Required defects to address:

- path_scope_drive_prefixed_relative_accepted
- path_scope_duplicate_normalization_accepted

Do not build AdapterManifest until the PatchTransaction repair, independent
repair check, and acceptance gate authorize it.
```
