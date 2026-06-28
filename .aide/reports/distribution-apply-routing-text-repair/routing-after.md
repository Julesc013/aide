# DistributionApply Routing Text After Repair

After repair, status, plan, and verify command output includes:

```text
recommended_next_task: AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
aide_self_consumer_fixture_accepted: true
accepted_fixture_capability: aide_self_consumer_fixture_v0
self_consumer_fixture_started: true
real_target_apply_implemented: false
source_repo_apply_implemented: false
target_repository_mutation_implemented: false
release_publication_implemented: false
canary_readiness: false
public_release_readiness: false
network_calls_implemented: false
provider_model_calls_implemented: false
branch_worktree_automation_implemented: false
```

`distribution-apply plan` without `--scenario` now renders a non-mutating default plan view for `managed-file-update`.
