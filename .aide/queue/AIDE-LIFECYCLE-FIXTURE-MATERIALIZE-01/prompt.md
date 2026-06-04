# Prompt

Materialize static lifecycle fixture inputs and expected-state files under explicitly authorized fixture/example paths using the lifecycle schemas and local lifecycle-schema validator created by `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`.

Do not implement or execute lifecycle apply. Do not run scoped transaction apply against fixture targets. Do not mutate external target repositories. Preserve all install, upgrade, repair, rollback, uninstall, branch/worktree, merge, push, promotion, release, GitHub, provider/model, Gateway, network, and broad active-repo apply prohibitions.

End at `needs_review` with evidence and exactly one next WorkUnit.
