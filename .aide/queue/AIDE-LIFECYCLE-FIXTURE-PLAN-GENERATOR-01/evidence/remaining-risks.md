# Remaining Risks

- Generated plans are static artifacts, not output from a reusable CLI command.
- Generated plans require independent review before future dry-run execution or planner widening.
- Lifecycle-schema validator remains schema/example scoped.
- Scoped transaction executor v0 is accepted-with-notes but not production-ready.
- Multi-file lifecycle orchestration remains unimplemented.
- Rollback execution remains prohibited.
- Uninstall/delete safety remains future work.
- Active repo apply, target repo apply, release publication, provider/model calls, Gateway calls, network calls, GitHub mutation, branch/worktree mutation, and broad active-repo apply remain prohibited.
- Global Task OS `task next-plan` selector still lags task-local next-batch routing.
