# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Create and process `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

## Goal

Repair the material path-scope fail-closed defects found by
`AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` and preserved by
`AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`.

## Required Repairs

Reject:

```text
C:repo/file.txt
```

as a drive-prefixed relative path where repository-relative paths are required.

Reject duplicate-normalized declared paths such as:

```text
src//file.py
src/file.py
```

## Boundary

Do not implement patch application, approval, policy evaluation, rollback
execution, admission, trust, AdapterManifest, ContextPack v2, runtime, worker
execution, provider/model/Gateway/network/GitHub behavior, branch/worktree
automation, release, promotion, or target-repository mutation.

## Exit

Stop at `needs_review` and recommend:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
