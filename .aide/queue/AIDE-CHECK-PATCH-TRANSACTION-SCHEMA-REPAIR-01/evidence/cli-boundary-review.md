# CLI Boundary Review

Supported command results before report writing:

- `py -3 .aide/scripts/aide_lite.py patch-transaction status`:
  `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py patch-transaction project`:
  `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py patch-transaction validate`:
  `PASS_WITH_WARNINGS`.

Unsupported operations failed closed with exit code `2`:

- `patch-transaction apply`;
- `patch-transaction approve`;
- `patch-transaction execute`;
- `patch-transaction rollback`.

No apply, approval, target mutation, branch/worktree creation, provider/model,
network, Gateway, GitHub, release, or promotion behavior was observed.
