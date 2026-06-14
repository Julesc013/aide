# Command Review

Result: PASS.

Behavior report: `.aide/reports/workunit-cli-mutation-check/behavior-results.json`.

- `workunit create --dry-run`: PASS, exit 0.
- `workunit block --dry-run`: PASS, exit 0.
- `workunit evidence add --dry-run`: PASS, exit 0.
- controlled `create --apply`: PASS, exit 0.
- controlled `block --apply`: PASS, exit 0.
- controlled `evidence add --apply`: PASS, exit 0.
- unsupported `claim/run/finish/repair`: fail-closed nonzero.
- missing/conflicting mode flags: fail-closed nonzero.
