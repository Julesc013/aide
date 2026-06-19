# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01
# Independent Recheck of PatchTransaction Path-Scope Repair

Create and process `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Independently review:

- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`

Scope:

- check only
- no repair
- no schema/helper/test changes
- no approval
- no patch apply
- no target mutation
- no policy engine
- no rollback execution
- no admission or trust
- no AdapterManifest
- no ContextPack v2
- no runtime or external calls

Verify independently:

1. preserve the historical failed check evidence
2. verify the repair task and evidence are complete
3. verify drive-prefixed relative paths such as `C:repo/file.txt` fail closed
4. verify `C:repo\file.txt`, `C:/repo/file.txt`, `C:\repo\file.txt`, and `z:relative.txt` fail closed
5. verify duplicate-normalized declarations such as `src//file.py` plus `src/file.py` fail closed
6. verify duplicate-normalized entries in `allowed_paths` and `forbidden_paths` fail closed
7. verify duplicate diagnostics name both original values and the shared canonical path
8. verify absolute, Windows absolute, UNC, traversal, empty, dot-only, outside-allowed, forbidden-match, overlap, and prefix-boundary cases remain fail-closed
9. verify ordinary separator normalization remains supported for a single declared path
10. verify valid distinct normalized paths remain accepted
11. verify focused tests include the repaired cases and pass
12. verify PatchTransaction status/project/validate remains `PASS_WITH_WARNINGS`
13. verify the deterministic PatchTransaction projection remains stable
14. verify reports parse and agree on no apply, no approval, no target mutation, no admission, and no trust
15. verify no forbidden operations occurred
16. verify broad AIDE validation and task evidence checks pass

Expected result:

```text
PASS
or
PASS_WITH_WARNINGS
```

Recommended next task if the recheck passes:

```text
AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01
```

If the path-scope repair remains incorrect:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-02
```
