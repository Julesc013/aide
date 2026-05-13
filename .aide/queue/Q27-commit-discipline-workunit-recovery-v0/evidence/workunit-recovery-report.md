# WorkUnit Recovery Report

Status: blocked before implementation.

Q27 was expected to add:

- `.aide/policies/task-resumption.yaml`;
- `.aide/policies/work-units.yaml`;
- `.aide/policies/recovery.yaml`;
- AIDE Lite `task inspect`, `task status`, `task noop-check`,
  `task dependencies`, `task recover`, `task evidence`, and `task current`.

No WorkUnit or recovery policy was implemented because baseline Q25
pack/local-state validation failed before edits.

## Repo-State-First Behavior Applied

Before asking the user for help or editing implementation files, Q27 inspected:

- Git status, branch, HEAD, recent log, and ignore state;
- AIDE operating law and queue policy;
- Q25 task/status/evidence;
- current AIDE Lite validation and pack-status.

The resulting blocker is repo-local and reproducible.

## Recovery Recommendation

Repair Q25 pack/local-state drift, then reopen Q27.
