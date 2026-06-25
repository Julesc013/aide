# Remaining Risks

- The service is single-machine and local only.
- Event delivery is at-least-once, not exactly-once.
- No scheduler, worker execution, trust enforcement, MCP, Workbench, or network
  API exists.
- Runtime `.aide.local/service` state remains future operational state and is
  not committed by this task.

No material build findings remain.
