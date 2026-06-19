# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Create and process `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Independently recheck
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Verify that:

- the failed check evidence remains preserved;
- drive-prefixed relative paths such as `C:repo/file.txt` fail closed;
- duplicate-normalized declarations such as `src//file.py` plus `src/file.py`
  fail closed;
- pre-existing path-scope fail-closed behavior remains intact;
- focused tests pass;
- PatchTransaction `status`, `project`, and `validate` remain
  `PASS_WITH_WARNINGS`;
- no approval, apply, target mutation, rollback, admission, trust, runtime,
  provider/model/network/Gateway/GitHub, branch/worktree, release, promotion, or
  target-repository mutation behavior was added.

If the repair passes, recommend:

```text
AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01
```

If a material defect remains, recommend:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-02
```
