# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Create and process `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

This is a check-only task. Verify the preserved source chain:

- `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` remains `FAILED_VALIDATION`;
- the original check identifies drive-prefixed relative paths and
  duplicate-normalized path entries as material findings;
- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01` exists with result
  `PASS_WITH_WARNINGS`;
- commit `fca99236c2f933660de29b657dc181f1174dd719` is at live `HEAD` or an
  ancestor;
- repair evidence reports `missing_evidence: 0`;
- no later repair-check or superseding PatchTransaction repair exists.

Independently verify:

- `C:repo/file.txt`, `C:repo\file.txt`, `C:/repo/file.txt`,
  `C:\repo\file.txt`, `c:relative.txt`, `z:folder/file.py`, and `Z:file.py`
  fail closed;
- duplicate-normalized entries fail in `allowed_paths`, `forbidden_paths`, and
  `declared_changed_paths`;
- diagnostics preserve both original values, the shared canonical path, and the
  path collection;
- existing absolute-path, traversal, forbidden-match, outside-allowed,
  prefix-boundary, lifecycle, no-apply, no-target-mutation, no-approval, and
  no-trust protections remain intact;
- projection is deterministic and source inputs remain unchanged;
- unsupported apply/approve/execute/rollback commands fail closed;
- downstream blocked tasks remain preserved historical records.

Write repair-check reports under `.aide/reports/patch-transaction-repair-check/`
and task evidence under this task's `evidence/` directory. Do not edit
PatchTransaction implementation, schema, tests, build reports, failed-check
reports, repair reports, accepted predecessor protocols, blocked downstream task
records, AdapterManifest, ContextPack, OKF, runtime, provider, host, VCS, or
target-repository files.

Expected result if sound: `PASS_WITH_WARNINGS`.

If the repair passes, recommend exactly:

```text
AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01
```

Do not reuse or rewrite the already-blocked
`AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01` task.
