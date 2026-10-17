# Changed files and ownership

Existing `.aide/scripts/aide_lite.py` owns the current-task projection and parser.
Only its current-command handler/parser change; three private projection helpers
are added. Original named binding and Task OS test bytes remain unchanged.
`test_task_current.py` adds behavioral oracles. `run_checks.py` is task-local
qualification transport. Documentation and queue/current records explain the
bounded change. Existing capability-ledger outputs are refreshed after their
explicit stale-source refusal. No native target, production policy or export change.
