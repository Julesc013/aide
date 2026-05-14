# Uninstall Dry-Run Report

Command: `py -3 .aide/scripts/aide_lite.py uninstall dry-run`

- Result: PASS.
- Dry-run path: `.aide/uninstall/latest-uninstall-dry-run.json`.
- Operations: 1790.
- Future removal candidates: 233.
- Planned preservations: 885.
- Unknown-ownership records: 672.
- Blockers: 0.
- `no_apply`: true.
- `target_mutation`: false.
- `delete`: false.
- Blanket `.aide` deletion: false.

Future removal candidates are advisory only and keep `apply_allowed: false` and
`delete_allowed: false`. Target memory, queue, evidence, golden tasks, generated
target state, manual content, existing tools, local state, secrets, and unknown
ownership are preserved or routed to manual review.
