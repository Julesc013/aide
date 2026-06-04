# Next Task Prompt Seed

Task ID: `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`

Create a planning/schema/fixture WorkUnit that defines lifecycle manifest, lifecycle transaction plan, lifecycle report, rollback-compatible record, and fixture repository shape for future install, upgrade, lifecycle repair, rollback, and uninstall proofs. Use the `AIDE-APPLY-LIFECYCLE-PLAN-01` lifecycle proof ladder as authority. Do not execute lifecycle apply, do not mutate active AIDE repo files through the scoped executor, do not mutate target repositories, do not mutate branches/worktrees, do not publish releases, do not call GitHub, providers/models, Gateway, or network services, and do not mark any lifecycle surface production-ready or release-ready. End at `needs_review` with validation, evidence, capability reality labels, and exactly one next WorkUnit.
