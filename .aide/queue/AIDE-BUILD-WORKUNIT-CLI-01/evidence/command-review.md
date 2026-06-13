# Command Review

Supported commands:

- `py -3 .aide/scripts/aide_lite.py workunit status`
- `py -3 .aide/scripts/aide_lite.py workunit list`
- `py -3 .aide/scripts/aide_lite.py workunit inspect --task-id <TASK_ID>`
- `py -3 .aide/scripts/aide_lite.py workunit validate`

Unsupported commands fail closed through argparse invalid-choice handling:

- `workunit create`
- `workunit claim`
- `workunit run`
- `workunit block`
- `workunit finish`
- `workunit repair`

All command outputs explicitly preserve:

- `target_mutation: false`
- `active_repo_apply_mutation: false`
- `branch_mutation: false`
- `provider_or_model_calls: none`
- `Gateway calls: none`
- `network_calls: none`
