# Broad Delete Checks

## Result

`PASS`

`broad-delete-blocked` attempts `delete_tree` and `delete_glob` as metadata only. The generated plan and expected report classify the scenario as `BLOCKED` with blocker `BLOCKED_BROAD_DELETE`.

No delete execution occurred.
