# Capability Overclaim Report

- command: `capability overclaim-report`
- generated_at: deterministic
- repo_root: `D:/Projects/AIDE/aide`
- current_branch: `task/aide-current-scoped-lite-qualification-01`
- current_commit: `771684bcbd1430e692c0b72d9fa087b8fdc6ac79`
- mode: report_only
- task_execution: false
- repair_execution: false
- capability_apply_behavior: false
- branch_mutation: false
- target_mutation: false
- release_publication: false
- provider_or_model_calls: none
- network_calls: none

## Summary

- result: PASS
- record_count: 1
- summary: overclaim review records detected

## Records

- `capability_reality_ledger`: class=report_only_claimed_as_apply; severity=medium; blocking=false; notes=report-only capability mentions apply boundary; review claim wording

## Boundary

- overclaim reporting did not mutate source, target, branch, release, provider, model, or network state
