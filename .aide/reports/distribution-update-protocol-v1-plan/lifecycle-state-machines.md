# Lifecycle State Machines

## Install

```text
observe -> plan -> dry_run -> review -> approve_exact_plan -> apply_fixture_only_future -> verify -> record -> repair_or_rollback
```

## Update

```text
observe_current -> observe_candidate_distribution -> compare -> plan -> dry_run -> approve_exact_plan_digest -> create_rollback_bundle -> apply_exact_operations -> regenerate_target_local_outputs -> verify -> write_update_receipt
```

## Repair

```text
observe -> diagnose -> classify -> plan -> dry_run -> review -> future_apply_if_authorized -> verify -> record
```

## Rollback

```text
observe -> load_rollback_bundle_or_prior_plan -> classify -> plan -> dry_run -> review -> future_apply_if_authorized -> verify -> record
```

## Uninstall

```text
observe -> classify_owned_and_preserved_surfaces -> plan -> dry_run -> review -> future_apply_if_authorized -> verify -> record
```

## Release

```text
validate_source -> build_local_archive -> validate_archive -> draft_release_text -> review -> future_publish_if_authorized
```

All apply transitions are future-only and require separate reviewed queue
authority. This planning task does not authorize them.
