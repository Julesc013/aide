# AIDE-TASK-OS-STATUS-REPAIR-01 Prompt

Repair stale Task OS current/latest-task reporting after `AIDE-APPLY-02` was accepted with notes.

Use live repo truth and the `AIDE-QUEUE-CLOSURE-02` selection. Keep writes inside the allowed paths in `task.yaml`. Do not implement apply lifecycle behavior, do not mutate target repositories, do not mutate branches/worktrees, do not push, do not merge, do not publish releases, do not call GitHub, providers, Gateway, or network services, and do not perform broad active-repo apply.

Required outcome: Task OS generated reports no longer classify stale raw `AIDE-APPLY-02` shorthand as the current/latest missing task; reports distinguish absent `.aide/queue/current.toml`, latest indexed task, latest task packet, selected next WorkUnit, historical tasks, and superseded tasks; README and latest task packet no longer point to stale next-work truth; status ends at `needs_review`.
