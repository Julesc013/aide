# CLI Review

Added thin dispatch only:

```powershell
py -3 .aide/scripts/aide_lite.py capability-manifest status
py -3 .aide/scripts/aide_lite.py capability-manifest project
py -3 .aide/scripts/aide_lite.py capability-manifest validate
```

Not registered:

- `run`
- `execute`
- `admit`
- `conformance`
- `adapter-run`
- `repair`
- `mutate`

Focused tests confirm forbidden runtime/admission subcommands fail closed through
argparse.
