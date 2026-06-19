# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01

Create and process `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

## Goal

Repair the material path-scope fail-closed defects found by
`AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` without expanding PatchTransaction
beyond the accepted minimal schema-only boundary.

## Required Repairs

Ensure PatchTransaction scope validation rejects:

1. drive-prefixed relative paths such as:

```text
C:repo/file.txt
```

2. duplicate-normalized declared paths such as:

```text
src//file.py
src/file.py
```

The repair must preserve existing fail-closed behavior for absolute paths,
Windows absolute paths, UNC paths, traversal, empty and dot-only paths,
declared paths outside allowed scope, forbidden matches, direct
allowed/forbidden overlap, separator normalization, and prefix-boundary checks.

## Boundaries

Do not implement patch apply, approval, policy evaluation, rollback execution,
admission, trust, AdapterManifest, ContextPack v2, Test Broker runtime, worker
execution, runtime, Service, Commander, Workbench, provider/model/Gateway/
network/GitHub behavior, branch/worktree automation, release, promotion, or
target-repository mutation.

## Exit

Stop at `needs_review`. If repaired, recommend:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
