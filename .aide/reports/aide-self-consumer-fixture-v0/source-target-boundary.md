# Source/Target Boundary

The AIDE source repository is fixture author and source-pack input only.

The installed target in this fixture is synthetic:

```text
aide://fixture-target/aide-self-consumer-v0
```

The fixture records:

- `source_repo_is_target: false`
- `source_repo_identity_excluded: true`
- `source_generated_state_is_target_truth: false`
- `source_repo_apply_occurred: false`
- `real_target_repo_modified: false`

The `source-repo-confusion-refusal` scenario blocks any attempt to treat the source repository as the installed self-consumer target.
