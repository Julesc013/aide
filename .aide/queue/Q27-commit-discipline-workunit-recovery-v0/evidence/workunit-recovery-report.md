# WorkUnit Recovery Report

Status: superseded pre-repair blocker record.

Q27 was expected to add:

- `.aide/policies/task-resumption.yaml`;
- `.aide/policies/work-units.yaml`;
- `.aide/policies/recovery.yaml`;
- AIDE Lite `task inspect`, `task status`, `task noop-check`,
  `task dependencies`, `task recover`, `task evidence`, and `task current`.

No WorkUnit or recovery policy was implemented in this attempt. The original
blocker was baseline Q25 pack/local-state validation failure before edits.

## Repo-State-First Behavior Applied

Before asking the user for help or editing implementation files, Q27 inspected:

- Git status, branch, HEAD, recent log, and ignore state;
- AIDE operating law and queue policy;
- Q25 task/status/evidence;
- current AIDE Lite validation and pack-status.

The resulting blocker is repo-local and reproducible.

## Recovery Recommendation

Q25 pack/local-state drift has since been repaired. Redo Q27 after Q25 and Q26
review so commit discipline and WorkUnit recovery are implemented from the
repaired baseline.
