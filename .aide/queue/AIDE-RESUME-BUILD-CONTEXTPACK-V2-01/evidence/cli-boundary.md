# CLI Boundary

Added thin AIDE Lite dispatch:

```bash
py -3 .aide/scripts/aide_lite.py context-pack-v2 status
py -3 .aide/scripts/aide_lite.py context-pack-v2 project
py -3 .aide/scripts/aide_lite.py context-pack-v2 validate
```

Observed results:

- `status`: `PASS_WITH_WARNINGS`
- `project`: `PASS_WITH_WARNINGS`
- `validate`: `PASS_WITH_WARNINGS`

The commands generate reports and validate the projection only. They do not
apply patches, create branches/worktrees, call providers or networks, or mutate
target repositories.
