# Command Surface

Implemented report-only commands:

- `task status`
- `task classify`
- `task repair-plan`
- `task requeue-plan`
- `task resume-plan`
- `blocker status`
- `blocker classify`
- `wave status`
- `wave plan`
- `checkpoint status`
- `checkpoint plan`

Each command is standard-library-only, local to the AIDE source repository, and writes reports under `.aide/reports/task-os-*`.

The commands inspect queue/status/evidence/report files. They do not execute tasks, repair blockers, mutate queue state, resume target work, create branches/worktrees, merge, push, promote, publish releases, call providers/models, call network services, or mutate target repositories.
