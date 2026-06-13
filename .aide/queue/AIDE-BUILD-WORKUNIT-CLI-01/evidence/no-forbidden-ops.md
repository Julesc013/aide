# No Forbidden Operations

Forbidden operations preserved:

- no WorkUnit mutation CLI
- no runtime scheduler or supervisor
- no WorkerRun, TestJob, or Test Broker
- no Service or Commander
- no provider adapters
- no branch/worktree automation
- no target repo apply
- no active repo apply
- no rollback or uninstall execution
- no release or promotion
- no merge or push
- no GitHub mutation
- no network, Gateway, or model/provider calls
- no dependency installation
- no destructive migration of queue tasks or accepted reports

Validation facts:

- Unsupported mutation commands fail closed with argparse invalid-choice errors.
- WorkUnit CLI reports state `workunit_create_implemented`, `workunit_claim_implemented`, `workunit_run_implemented`, `workunit_block_implemented`, `workunit_finish_implemented`, and `workunit_repair_implemented` as `false`.
- `target_mutation`, `active_repo_apply_mutation`, `branch_mutation`, `provider_or_model_calls`, `Gateway calls`, and `network_calls` remained false/none in command output.
- Targeted overclaim scan over added lines and new files found no unsupported capability claims.
- Boundary-aware secret scan over added lines and new files found no secret markers.
