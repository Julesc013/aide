# Capability Reality Ledger

- command: `capability ledger`
- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `cd7c7bfcc4a27927e865a86df88b3a0e92ffa892`
- mode: report_only
- task_execution: false
- repair_execution: false
- capability_apply_behavior: false
- branch_mutation: false
- target_mutation: false
- release_publication: false
- provider_or_model_calls: none
- network_calls: none

## State Counts

- planned: 1
- specified: 3
- stubbed: 1
- implemented: 1
- tested: 1
- exposed: 1
- documented: 2
- deprecated: 1
- removed: 1
- unknown: 1

## Records

- `task_os_lifecycle_contracts`: dominant_state=specified; modifiers=report_only, review_gated; confidence=high; evidence_refs=4; missing_refs=0
- `task_os_report_commands`: dominant_state=exposed; modifiers=no_call, report_only, review_gated; confidence=high; evidence_refs=4; missing_refs=0
- `capability_reality_ledger`: dominant_state=implemented; modifiers=no_call, report_only, review_gated; confidence=high; evidence_refs=4; missing_refs=0
- `capability_reality_tests`: dominant_state=tested; modifiers=report_only, test_only; confidence=high; evidence_refs=3; missing_refs=0
- `task_os_docs`: dominant_state=documented; modifiers=docs_only, report_only; confidence=high; evidence_refs=4; missing_refs=0
- `gateway_runtime_forwarding`: dominant_state=stubbed; modifiers=apply_gated, no_call, report_only; confidence=high; evidence_refs=3; missing_refs=0
- `provider_adapter_metadata`: dominant_state=specified; modifiers=apply_gated, no_call, report_only; confidence=high; evidence_refs=3; missing_refs=0
- `github_release_draft`: dominant_state=documented; modifiers=local_only, no_call, release_draft_only; confidence=high; evidence_refs=3; missing_refs=0
- `install_repair_upgrade_models`: dominant_state=specified; modifiers=apply_gated, dry_run_only, report_only, target_specific; confidence=high; evidence_refs=4; missing_refs=0
- `target_pilot_handoffs`: dominant_state=planned; modifiers=review_gated, source_generated_only, target_specific; confidence=high; evidence_refs=2; missing_refs=0
- `raw_prompt_direct_execution`: dominant_state=removed; modifiers=removed, review_gated; confidence=high; evidence_refs=3; missing_refs=0
- `legacy_bootstrap_prompt_history`: dominant_state=deprecated; modifiers=deprecated, docs_only; confidence=high; evidence_refs=3; missing_refs=0
- `autonomous_task_scheduler`: dominant_state=unknown; modifiers=apply_gated, unknown; confidence=low; evidence_refs=1; missing_refs=0

## Reality Boundary

- docs_only is not implementation proof
- report_only is not apply behavior
- no_call is not live provider or model integration
- release_draft_only is not publication
- target_specific and source_generated_only are not target truth
