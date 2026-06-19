# CLI Boundary

Added thin AIDE Lite dispatch:

```bash
py -3 .aide/scripts/aide_lite.py adapter-manifest status
py -3 .aide/scripts/aide_lite.py adapter-manifest project
py -3 .aide/scripts/aide_lite.py adapter-manifest validate
```

The commands report declaration-only status and do not implement apply,
approval, execution, admission, trust, worker launch, network, provider, GitHub,
branch/worktree, or target-repository mutation behavior.
