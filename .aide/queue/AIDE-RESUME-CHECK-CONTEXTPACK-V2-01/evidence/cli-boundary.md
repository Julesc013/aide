# CLI Boundary

Commands:

```bash
py -3 .aide/scripts/aide_lite.py context-pack-v2 status
py -3 .aide/scripts/aide_lite.py context-pack-v2 apply
py -3 .aide/scripts/aide_lite.py context-pack-v2 approve
py -3 .aide/scripts/aide_lite.py context-pack-v2 execute
py -3 .aide/scripts/aide_lite.py context-pack-v2 rollback
```

Results:

- `status`: `PASS_WITH_WARNINGS`
- unsupported `apply`: fails closed
- unsupported `approve`: fails closed
- unsupported `execute`: fails closed
- unsupported `rollback`: fails closed

Focused tests exercised `project` and `validate` in temporary workspaces.
