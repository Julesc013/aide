# Next Task Prompt

Proceed with:

```text
AIDE-CHECK-WORKUNIT-CLI-MUTATION-01
```

Review only. Do not repair inline.

Check that the `minimal_workunit_queue_metadata_mutation_cli` slice implements only bounded queue metadata mutation for `workunit create`, `workunit block`, and `workunit evidence add`, with explicit `--dry-run|--apply`, safe path handling, temp-root apply tests, truthful reports, no accepted queue mutation during dry-run validation, no overclaiming, no secrets, and no claim/run/finish/repair/runtime/lease/scheduler/service/provider/branch/target-apply behavior.
