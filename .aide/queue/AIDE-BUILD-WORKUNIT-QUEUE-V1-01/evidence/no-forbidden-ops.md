# No Forbidden Operations

Forbidden operations preserved:

- No WorkUnit create/list/claim/block/finish/repair CLI.
- No TestJob or Test Broker.
- No scheduler, supervisor, Service, or Commander.
- No provider adapter, model/provider calls, Gateway calls, GitHub mutation, or network calls.
- No branch/worktree automation, merge, push, release, or promotion.
- No target repo apply, active repo apply, broad lifecycle apply, rollback execution, or uninstall execution.
- No destructive migration of queue tasks or accepted reports.

Validation reports preserve these flags:

- workunit_cli_implemented: false
- destructive_migration_performed: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_model_calls: false
- gateway_calls: false
- network_calls: false
