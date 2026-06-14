# AIDE-CHECK-WORKUNIT-CLI-MUTATION-01 Prompt

Check, do not build.

Verify the `minimal_workunit_queue_metadata_mutation_cli` slice from commit `0957e9a4d2e8fae85cf271723f168fcda96fb0a6`.

Confirm that `workunit create`, `workunit block`, and `workunit evidence add` are queue metadata operations only, with explicit `--dry-run|--apply`, safe task id and evidence path handling, no runtime/lease/scheduler behavior, no claim/run/finish/repair behavior, no target apply, no active apply, no branch/worktree mutation, no provider/model/Gateway/network/GitHub calls, no overclaiming, and no secrets.

End at `needs_review`.
