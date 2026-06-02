# Capability Observations

- command: `capability scan`
- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `d5e3e818841931702cd4e2cde49452744afab985`
- mode: report_only
- task_execution: false
- repair_execution: false
- capability_apply_behavior: false
- branch_mutation: false
- target_mutation: false
- release_publication: false
- provider_or_model_calls: none
- network_calls: none

## Observations

- observation_count: 47

- `autonomous_task_scheduler`: state=unknown class=queue_evidence ref=`.aide/queue/X-OS-02-capability-reality-ledger-v0/task.yaml` confidence=high
- `capability_reality_ledger`: state=implemented class=unknown ref=`.aide/capabilities/capability-seeds.yaml` confidence=high
- `capability_reality_ledger`: state=implemented class=schema_only ref=`.aide/ledgers/capability-ledger.schema.json` confidence=high
- `capability_reality_ledger`: state=implemented class=command_surface ref=`.aide/scripts/aide_lite.py` confidence=high
- `capability_reality_ledger`: state=implemented class=docs_only ref=`docs/reference/capability-reality-ledger.md` confidence=high
- `capability_reality_tests`: state=tested class=fixture_only ref=`.aide/evals/golden-tasks/capability_command_surface_golden/task.yaml` confidence=high
- `capability_reality_tests`: state=tested class=test_only ref=`.aide/evals/golden-tasks/capability_command_surface_golden/task.yaml` confidence=high
- `capability_reality_tests`: state=tested class=fixture_only ref=`.aide/evals/golden-tasks/capability_ledger_generation_golden/task.yaml` confidence=high
- `capability_reality_tests`: state=tested class=test_only ref=`.aide/evals/golden-tasks/capability_ledger_generation_golden/task.yaml` confidence=high
- `capability_reality_tests`: state=tested class=test_only ref=`.aide/scripts/tests/test_x_os_02_capability_reality.py` confidence=high
- `gateway_runtime_forwarding`: state=stubbed class=policy_only ref=`.aide/policies/gateway.yaml` confidence=high
- `gateway_runtime_forwarding`: state=stubbed class=runtime_code ref=`core/gateway/README.md` confidence=high
- `gateway_runtime_forwarding`: state=stubbed class=docs_only ref=`docs/reference/gateway-skeleton.md` confidence=high
- `github_release_draft`: state=documented class=policy_only ref=`.aide/policies/github-release-draft.yaml` confidence=high
- `github_release_draft`: state=documented class=local_generated ref=`.aide/release/latest-github-release-draft.json` confidence=high
- `github_release_draft`: state=documented class=report_only ref=`.aide/release/latest-github-release-draft.json` confidence=high
- `github_release_draft`: state=documented class=docs_only ref=`docs/reference/github-release-draft.md` confidence=high
- `install_repair_upgrade_models`: state=specified class=docs_only ref=`docs/reference/aide-install-model.md` confidence=high
- `install_repair_upgrade_models`: state=specified class=docs_only ref=`docs/reference/aide-repair-model.md` confidence=high
- `install_repair_upgrade_models`: state=specified class=docs_only ref=`docs/reference/aide-rollback-uninstall.md` confidence=high
- `install_repair_upgrade_models`: state=specified class=docs_only ref=`docs/reference/aide-upgrade-model.md` confidence=high
- `legacy_bootstrap_prompt_history`: state=deprecated class=unknown ref=`.aide/memory/project-state.md` confidence=high
- `legacy_bootstrap_prompt_history`: state=deprecated class=docs_only ref=`AGENTS.md` confidence=high
- `legacy_bootstrap_prompt_history`: state=deprecated class=docs_only ref=`docs/reference/source-of-truth.md` confidence=high
- `provider_adapter_metadata`: state=specified class=no_call ref=`.aide/providers/capability-matrix.yaml` confidence=high
- `provider_adapter_metadata`: state=specified class=no_call ref=`.aide/providers/provider-catalog.yaml` confidence=high
- `provider_adapter_metadata`: state=specified class=docs_only ref=`docs/reference/provider-adapter-v0.md` confidence=high
- `raw_prompt_direct_execution`: state=removed class=policy_only ref=`.aide/policies/prompt-normalization.yaml` confidence=high
- `raw_prompt_direct_execution`: state=removed class=docs_only ref=`AGENTS.md` confidence=high
- `raw_prompt_direct_execution`: state=removed class=docs_only ref=`docs/reference/source-of-truth.md` confidence=high
- `target_pilot_handoffs`: state=planned class=queue_evidence ref=`.aide/context/latest-task-packet.md` confidence=high
- `target_pilot_handoffs`: state=planned class=local_generated ref=`.aide/reports/target-work-deferral.md` confidence=high
- `target_pilot_handoffs`: state=planned class=report_only ref=`.aide/reports/target-work-deferral.md` confidence=high
- `task_os_docs`: state=documented class=docs_only ref=`docs/reference/README.md` confidence=high
- `task_os_docs`: state=documented class=docs_only ref=`docs/reference/capability-reality-ledger.md` confidence=high
- `task_os_docs`: state=documented class=docs_only ref=`docs/reference/task-os-report-only-commands.md` confidence=high
- `task_os_docs`: state=documented class=docs_only ref=`docs/reference/task-os-v0.md` confidence=high
- `task_os_lifecycle_contracts`: state=specified class=policy_only ref=`.aide/policies/blockers.yaml` confidence=high
- `task_os_lifecycle_contracts`: state=specified class=policy_only ref=`.aide/policies/repair-loop.yaml` confidence=high
- `task_os_lifecycle_contracts`: state=specified class=policy_only ref=`.aide/policies/task-lifecycle.yaml` confidence=high
- `task_os_lifecycle_contracts`: state=specified class=docs_only ref=`docs/reference/task-os-v0.md` confidence=high
- `task_os_report_commands`: state=exposed class=fixture_only ref=`.aide/evals/golden-tasks/task_os_command_surface_golden/task.yaml` confidence=high
- `task_os_report_commands`: state=exposed class=test_only ref=`.aide/evals/golden-tasks/task_os_command_surface_golden/task.yaml` confidence=high
- `task_os_report_commands`: state=exposed class=local_generated ref=`.aide/reports/task-os-command-status.md` confidence=high
- `task_os_report_commands`: state=exposed class=report_only ref=`.aide/reports/task-os-command-status.md` confidence=high
- `task_os_report_commands`: state=exposed class=command_surface ref=`.aide/scripts/aide_lite.py` confidence=high
- `task_os_report_commands`: state=exposed class=test_only ref=`.aide/scripts/tests/test_x_os_01_task_os_commands.py` confidence=high

## Boundary

- no capability was applied or promoted
