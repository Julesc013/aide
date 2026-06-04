# Next Task Prompt

Task ID: `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`

Create a narrow queue WorkUnit that validates the lifecycle manifest, lifecycle plan, lifecycle report, rollback-compatible lifecycle record schemas, and `.aide/examples/apply/lifecycle/**` examples using local tooling only. The task may add a report-only validation command or targeted tests only if its live task packet explicitly authorizes those paths. Do not implement or execute lifecycle apply, do not materialize fixture targets, do not mutate active AIDE repo files through scoped transaction apply, do not mutate target repositories, do not mutate branches/worktrees, do not publish releases, do not call GitHub, providers/models, Gateway, or network services, and do not claim production-ready or release-ready lifecycle capability. End at `needs_review` with validation evidence and one next WorkUnit.
