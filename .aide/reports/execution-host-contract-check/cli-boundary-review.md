# CLI Boundary Review

- `execution-host status`, `execution-host project --source contract-projection`, and `execution-host validate` were invoked as system-under-test commands.
- All three commands report false runtime and no-call boundary lines.
- `execution-host run` is rejected by argparse as an invalid choice.
