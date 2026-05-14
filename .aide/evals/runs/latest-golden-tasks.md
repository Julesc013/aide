# Latest Golden Tasks

- result: PASS
- task_count: 85
- pass_count: 85
- warn_count: 0
- fail_count: 0
- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false
- token_quality_statement: Token reduction remains valid only if golden tasks pass.

## Tasks

### adapter-managed-section-determinism

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: AGENTS.md
- notes: Checks managed section replacement on an isolated fixture repo.

### aide_branch_plan_golden

- result: PASS
- checks_run: 8
- passed_checks: 8
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/aide-dev-main-plan.json, .aide/git/aide-dev-main-plan.md
- notes: Checks generated AIDE dev/main branch plan shape and no-mutation boundary.

### aide_dev_main_policy_golden

- result: PASS
- checks_run: 30
- passed_checks: 30
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/aide-branch-policy.yaml, .aide/git/aide-dev-main-plan.json
- notes: Checks AIDE main/dev branch policy and promotion gates.

### branch_role_detection_golden

- result: PASS
- checks_run: 15
- passed_checks: 15
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/branch-roles.md, .aide/git/workflow-detection.json, .aide/policies/branch-roles.yaml
- notes: Checks deterministic branch-role classification and conservative unknown handling.

### changelog_json_shape_golden

- result: PASS
- checks_run: 20
- passed_checks: 20
- approx_tokens_if_applicable: n/a
- related_paths: .aide/changelog/changelog.preview.json, .aide/changelog/release-notes.preview.json
- notes: Checks changelog and release-note preview JSON shape.

### changelog_preview_golden

- result: PASS
- checks_run: 9
- passed_checks: 9
- approx_tokens_if_applicable: n/a
- related_paths: .aide/changelog/CHANGELOG.preview.md, .aide/changelog/RELEASE_NOTES.preview.md, .aide/changelog/config.yaml, .aide/changelog/templates/changelog.md.template, .aide/changelog/templates/release-notes.md.template, .aide/policies/changelog.yaml, .aide/policies/commit-messages.yaml
- notes: Checks deterministic changelog preview grouping and malformed commit reporting.

### commit_message_standard_golden

- result: PASS
- checks_run: 14
- passed_checks: 14
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/commit-template.md, .aide/hooks/commit-msg, .aide/policies/commit-messages.yaml, .aide/reports/aide-commit-message-standard.md
- notes: Checks changelog-ready commit message validation anchors.

### compact-task-packet-required-sections

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: 1023
- related_paths: .aide/context/latest-task-packet.md, .aide/policies/token-budget.yaml, .aide/prompts/compact-task.md
- notes: Checks the compact task packet shape and forbidden prompt discipline.

### context-packet-no-full-repo-dump

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: 486
- related_paths: .aide/context/context-index.json, .aide/context/latest-context-packet.md, .aide/context/repo-map.json, .aide/context/test-map.json
- notes: Checks context refs instead of whole-repo dumps.

### docs_consistency_report_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/docs-consistency.yaml, .aide/reports/docs-consistency-report.md
- notes: Checks docs consistency warning surfaces.

### drop_candidate_not_delete_approval_golden

- result: PASS
- checks_run: 7
- passed_checks: 7
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/salvage-map.yaml, .aide/refactors/current-move-map.json, .aide/refactors/current-salvage-map.json
- notes: Checks Q42 fates never become deletion approval.

### export_pack_commit_policy_inclusion_golden

- result: PASS
- checks_run: 8
- passed_checks: 8
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/git/commit-template.md, .aide/hooks/commit-msg, .aide/policies/commit-messages.yaml
- notes: Checks portable commit discipline and changelog support are exported or locally available after import.

### export_pack_excludes_source_branch_state_golden

- result: PASS
- checks_run: 158
- passed_checks: 158
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/policies/export-import.yaml
- notes: Checks source-specific Git detection, helper plans, branch policy, and generated previews are not exported as target truth.

### export_pack_git_policy_inclusion_golden

- result: PASS
- checks_run: 15
- passed_checks: 15
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/git/helper-policy.yaml, .aide/policies/branch-roles.yaml, .aide/policies/git-workflow.yaml
- notes: Checks portable Git workflow and helper governance are exported or locally available after import.

### export_pack_task_recovery_inclusion_golden

- result: PASS
- checks_run: 8
- passed_checks: 8
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/policies/recovery.yaml, .aide/policies/task-resumption.yaml, .aide/policies/work-units.yaml
- notes: Checks portable task resumption, WorkUnit, and recovery governance are exported or locally available after import.

### file_classification_policy_golden

- result: PASS
- checks_run: 10
- passed_checks: 10
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/file-classification.yaml, .aide/scripts/aide_lite.py, README.md
- notes: Checks deterministic classification anchors and known AIDE file classes.

### file_quality_ledger_schema_golden

- result: PASS
- checks_run: 33
- passed_checks: 33
- approx_tokens_if_applicable: n/a
- related_paths: .aide/quality/file-quality-ledger.schema.json, .aide/quality/file-quality-record.schema.json, .aide/reports/file-quality-ledger.schema.json
- notes: Checks file quality ledger schema and latest/generated ledger shape.

### file_quality_policy_golden

- result: PASS
- checks_run: 48
- passed_checks: 48
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/docs-consistency.yaml, .aide/policies/file-quality.yaml, .aide/policies/module-quality.yaml, .aide/policies/reuse-modularity.yaml
- notes: Checks Q38 file-quality policy anchors and no-call advisory posture.

### fixture_import_governance_commands_golden

- result: PASS
- checks_run: 9
- passed_checks: 9
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/hooks/commit-msg, .aide/scripts/aide_lite.py
- notes: Checks safe fixture import receives governance files and can run portable commit/task/Git commands.

### git_helper_policy_golden

- result: PASS
- checks_run: 26
- passed_checks: 26
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/helper-commands.md, .aide/git/helper-policy.yaml, .aide/git/latest-helper-plan.json, .aide/git/latest-helper-plan.md
- notes: Checks Q29 helper policy anchors and generated helper-plan artifacts.

### git_land_plan_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/helper-commands.md, .aide/git/latest-helper-plan.json
- notes: Checks land dry-run planning and no remote mutation anchors.

### git_live_repo_no_mutation_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/helper-commands.md, .aide/git/helper-policy.yaml, .aide/git/latest-helper-plan.json
- notes: Checks live-repo helper plans remain no-mutation by default.

### git_promote_plan_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/helper-commands.md, .aide/git/helper-policy.yaml, .aide/policies/promotion-rules.yaml
- notes: Checks promotion helper review gates and dry-run command documentation.

### git_prune_guard_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/helper-commands.md, .aide/git/helper-policy.yaml, .aide/policies/prune-policy.yaml
- notes: Checks prune containment and protected-role guards.

### git_workflow_policy_golden

- result: PASS
- checks_run: 16
- passed_checks: 16
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/project-profiles.yaml, .aide/policies/branch-roles.yaml, .aide/policies/git-workflow.yaml, .aide/policies/promotion-rules.yaml, .aide/policies/prune-policy.yaml, .aide/policies/sync-policy.yaml
- notes: Checks Q28 Git workflow policy anchors and project profiles.

### github_ci_advisory_golden

- result: PASS
- checks_run: 12
- passed_checks: 12
- approx_tokens_if_applicable: n/a
- related_paths: .aide/github/ci-advisory.json, .aide/github/ci-advisory.md, .aide/policies/ci-gates.yaml
- notes: Checks Q35 CI gate advisory without workflow installation.

### github_export_inclusion_golden

- result: PASS
- checks_run: 21
- passed_checks: 21
- approx_tokens_if_applicable: n/a
- related_paths: .aide/export/aide-lite-pack-v0/manifest.yaml, .aide/policies/branch-protection.yaml, .aide/policies/ci-gates.yaml, .aide/policies/export-import.yaml, .aide/policies/github-protection.yaml
- notes: Checks Q35 portable policy export and generated advisory exclusion.

### github_protection_policy_golden

- result: PASS
- checks_run: 15
- passed_checks: 15
- approx_tokens_if_applicable: n/a
- related_paths: .aide/github/branch-protection-plan.json, .aide/policies/branch-protection.yaml, .aide/policies/github-protection.yaml
- notes: Checks Q35 GitHub branch-protection advisory remains report-only.

### github_report_only_golden

- result: PASS
- checks_run: 11
- passed_checks: 11
- approx_tokens_if_applicable: n/a
- related_paths: .aide/github/github-advisory.json, .aide/github/github-advisory.md, .aide/github/latest-github-status.md
- notes: Checks Q35 report-only behavior and no live GitHub/CI mutation.

### intent_compile_destructive_prompt_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/prompt-normalization.yaml, .aide/policies/risk-classes.yaml
- notes: Checks destructive raw prompts cannot execute directly.

### intent_compile_git_prompt_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/git-workflow.yaml, .aide/policies/intent.yaml, .aide/policies/promotion-rules.yaml
- notes: Checks Git promotion prompts require branch policy and review evidence.

### intent_compile_install_prompt_golden

- result: PASS
- checks_run: 6
- passed_checks: 6
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/export-import.yaml, .aide/policies/intent.yaml, .aide/policies/prompt-normalization.yaml
- notes: Checks target install prompts become preflight/preservation WorkUnits.

### intent_compile_overbroad_prompt_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/prompt-normalization.yaml, .aide/policies/workunit-sizing.yaml
- notes: Checks overbroad prompts become split recommendations.

### intent_compile_vague_prompt_golden

- result: PASS
- checks_run: 6
- passed_checks: 6
- approx_tokens_if_applicable: n/a
- related_paths: .aide/intake/intent-examples.yaml, .aide/policies/intent.yaml
- notes: Checks that vague prompts do not trigger product work.

### intent_packet_schema_golden

- result: PASS
- checks_run: 85
- passed_checks: 85
- approx_tokens_if_applicable: n/a
- related_paths: .aide/intake/intent-packet.schema.json, .aide/intake/workunit-draft.schema.json
- notes: Checks intent packet and WorkUnit draft shape plus raw prompt storage boundaries.

### malformed_commit_reporting_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/changelog/malformed-commits.md
- notes: Checks malformed and legacy commit reporting without history rewrite.

### migration_ledger_policy_golden

- result: PASS
- checks_run: 106
- passed_checks: 106
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/migration-ledger.yaml, .aide/refactors/migration-ledger-entry.schema.json, .aide/refactors/migration-ledger.schema.json
- notes: Checks Q42 migration ledger policy and draft event shape.

### migration_ledger_schema_golden

- result: PASS
- checks_run: 13
- passed_checks: 13
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/migration-ledger.schema.json
- notes: Checks migration-ledger schema and example dry-run event support.

### migration_policy_golden

- result: PASS
- checks_run: 8
- passed_checks: 8
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/migration.yaml
- notes: Checks Q39 migration stages and no mandatory migration boundary.

### move_map_policy_golden

- result: PASS
- checks_run: 79
- passed_checks: 79
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/move-map.yaml, .aide/refactors/move-map-entry.schema.json, .aide/refactors/move-map.schema.json
- notes: Checks Q42 move-map policy anchors and candidate-only map shape.

### move_map_schema_golden

- result: PASS
- checks_run: 11
- passed_checks: 11
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/move-map.schema.json
- notes: Checks move-map schema exists and remains no-apply.

### path_alias_policy_golden

- result: PASS
- checks_run: 79
- passed_checks: 79
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/path-aliases.yaml, .aide/refactors/path-alias-entry.schema.json, .aide/refactors/path-aliases.schema.json, .aide/refactors/path-aliases.template.yaml
- notes: Checks Q42 path-alias policy anchors and no-apply alias shape.

### path_alias_schema_golden

- result: PASS
- checks_run: 12
- passed_checks: 12
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/path-aliases.schema.json
- notes: Checks path-alias schema exists and remains no-apply.

### promotion_rules_golden

- result: PASS
- checks_run: 6
- passed_checks: 6
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/promotion-rules.md, .aide/policies/promotion-rules.yaml
- notes: Checks task-to-dev and dev-to-main gate anchors.

### prune_policy_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/prune-policy.md, .aide/policies/prune-policy.yaml
- notes: Checks prune guards require containment and remain dry-run/report-only.

### quality_ledger_generation_golden

- result: PASS
- checks_run: 28
- passed_checks: 28
- approx_tokens_if_applicable: n/a
- related_paths: .aide/repo/file-inventory.json, .aide/reports/file-quality-ledger.json
- notes: Checks deterministic quality ledger generation from Q37 outputs.

### quality_no_delete_recommendation_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/file-quality.yaml, .aide/reports/file-quality-ledger.json
- notes: Checks Q38 warning outputs never become deletion advice.

### refactor_map_no_apply_golden

- result: PASS
- checks_run: 991
- passed_checks: 991
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/current-move-map.json, .aide/refactors/current-salvage-map.json, .aide/refactors/map-validation-report.json, .aide/refactors/path-aliases.yaml, .aide/refactors/reference-rewrite-plan.json
- notes: Checks Q42 map outputs and generated bundle remain no-apply/no-mutation.

### refactor_no_apply_golden

- result: PASS
- checks_run: 52
- passed_checks: 52
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/refactor-application.yaml, .aide/refactors/latest-refactor-plan.example.json, .aide/refactors/latest-refactor-readiness.json
- notes: Checks Q39 has no apply, move, delete, rewrite, or deletion-approval behavior.

### refactor_plan_schema_golden

- result: PASS
- checks_run: 54
- passed_checks: 54
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/latest-refactor-plan.example.json, .aide/refactors/refactor-operation.schema.json, .aide/refactors/refactor-plan.schema.json
- notes: Checks refactor plan schema and no-apply example plan shape.

### refactor_policy_golden

- result: PASS
- checks_run: 54
- passed_checks: 54
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/refactor-application.yaml, .aide/policies/refactor-safety.yaml, .aide/policies/refactor.yaml
- notes: Checks Q39 refactor policy anchors and dry-run only posture.

### reference_rewrite_plan_golden

- result: PASS
- checks_run: 513
- passed_checks: 513
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/reference-rewrite.yaml, .aide/refactors/reference-rewrite-entry.schema.json, .aide/refactors/reference-rewrite-plan.schema.json
- notes: Checks Q42 reference rewrite planning remains candidate-only.

### release_notes_preview_golden

- result: PASS
- checks_run: 7
- passed_checks: 7
- approx_tokens_if_applicable: n/a
- related_paths: .aide/changelog/RELEASE_NOTES.preview.md, .aide/changelog/release-notes.preview.json
- notes: Checks release-note preview extraction and preview-only caveat.

### repo_dependency_map_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/dependency-map.yaml, .aide/repo/dependency-map.json
- notes: Checks deterministic dependency map shape and Python import detection.

### repo_doc_link_map_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/doc-link-map.yaml, .aide/repo/doc-link-map.json
- notes: Checks doc link map shape and conservative stale-candidate language.

### repo_explain_file_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/repo/file-inventory.json, .aide/scripts/aide_lite.py
- notes: Checks explain-file data for a stable AIDE Lite file.

### repo_intelligence_no_local_state_golden

- result: PASS
- checks_run: 3
- passed_checks: 3
- approx_tokens_if_applicable: n/a
- related_paths: .aide/repo/file-inventory.json, .gitignore
- notes: Checks local state exclusion and local-path flagging.

### repo_inventory_schema_golden

- result: PASS
- checks_run: 21
- passed_checks: 21
- approx_tokens_if_applicable: n/a
- related_paths: .aide/repo/file-inventory.json, .aide/repo/file-inventory.schema.json
- notes: Checks Q37 inventory schema and required file inventory fields.

### repo_ownership_map_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/ownership-map.yaml, .aide/repo/ownership-map.json
- notes: Checks deterministic owner map includes key AIDE surfaces.

### reuse_modularity_report_golden

- result: PASS
- checks_run: 6
- passed_checks: 6
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/reuse-modularity.yaml, .aide/reports/reuse-modularity-report.md
- notes: Checks reuse/modularity candidate-only reporting.

### review-packet-evidence-only

- result: PASS
- checks_run: 20
- passed_checks: 20
- approx_tokens_if_applicable: 1758
- related_paths: .aide/context/latest-review-packet.md, .aide/prompts/evidence-review.md, .aide/verification/review-packet.template.md
- notes: Checks review packet evidence-only shape.

### root_exception_schema_golden

- result: PASS
- checks_run: 11
- passed_checks: 11
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/root-exception.schema.json, .aide/roots/root-exceptions.json
- notes: Checks root exception records include retirement conditions.

### root_fate_no_delete_approval_golden

- result: PASS
- checks_run: 7
- passed_checks: 7
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/root-fates.yaml, .aide/roots/latest-root-classification.json, .aide/roots/latest-root-recycling-plan.json
- notes: Checks root fate vocabulary never becomes deletion approval.

### root_file_classification_schema_golden

- result: PASS
- checks_run: 20
- passed_checks: 20
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/root-file-classification.schema.json, .aide/roots/latest-root-classification.json
- notes: Checks root file classification output shape and no-apply fates.

### root_inventory_schema_golden

- result: PASS
- checks_run: 18
- passed_checks: 18
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/root-inventory.schema.json, .aide/roots/latest-root-inventory.json
- notes: Checks root inventory schema and generated inventory shape.

### root_record_schema_golden

- result: PASS
- checks_run: 13
- passed_checks: 13
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/root-record.schema.json
- notes: Checks root record schema shape.

### root_recycling_plan_schema_golden

- result: PASS
- checks_run: 40
- passed_checks: 40
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/root-recycling-plan.schema.json, .aide/roots/latest-root-recycling-plan.json
- notes: Checks root recycling plan output shape and no-apply posture.

### root_recycling_policy_golden

- result: PASS
- checks_run: 48
- passed_checks: 48
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/root-fates.yaml, .aide/policies/root-inventory.yaml, .aide/policies/root-recycling.yaml, .aide/policies/root-risk.yaml
- notes: Checks Q40 root recycling policy anchors and no-apply posture.

### roots_no_apply_golden

- result: PASS
- checks_run: 40
- passed_checks: 40
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/root-recycling.yaml, .aide/roots/latest-root-classification.json, .aide/roots/latest-root-recycling-plan.json
- notes: Checks root inventory, classification, and plan outputs remain no-apply.

### salvage_map_policy_golden

- result: PASS
- checks_run: 317
- passed_checks: 317
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/salvage-map.yaml, .aide/refactors/salvage-map-entry.schema.json, .aide/refactors/salvage-map.schema.json
- notes: Checks Q42 salvage-map policy anchors and preservation candidate shape.

### salvage_map_schema_golden

- result: PASS
- checks_run: 11
- passed_checks: 11
- approx_tokens_if_applicable: n/a
- related_paths: .aide/refactors/salvage-map.schema.json
- notes: Checks salvage-map schema exists and remains no-apply.

### sync_policy_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/sync-policy.md, .aide/policies/sync-policy.yaml
- notes: Checks multi-machine sync policy anchors remain report-only.

### task_resumption_standard_golden

- result: PASS
- checks_run: 15
- passed_checks: 15
- approx_tokens_if_applicable: n/a
- related_paths: .aide/context/latest-task-packet.md, .aide/policies/task-resumption.yaml, .aide/queue/index.yaml, .aide/reports/aide-task-resumption-standard.md
- notes: Checks repeated and out-of-order task recovery policy anchors.

### test_coverage_map_golden

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: .aide/quality/test-coverage-map.schema.json, .aide/reports/test-coverage-map.md
- notes: Checks heuristic test coverage map shape.

### token-ledger-budget-check

- result: PASS
- checks_run: 14
- passed_checks: 14
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/token-ledger.yaml, .aide/reports/token-ledger.jsonl, .aide/reports/token-savings-summary.md
- notes: Checks estimated token metadata without raw prompt or response storage.

### tool_absorption_policy_golden

- result: PASS
- checks_run: 55
- passed_checks: 55
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/tool-absorption.yaml, .aide/policies/tool-capabilities.yaml, .aide/policies/tool-fates.yaml, .aide/policies/tool-inventory.yaml, .aide/policies/tool-risk.yaml, .aide/policies/tool-wrapping.yaml
- notes: Checks Q41 tool absorption policy anchors and preservation posture.

### tool_adapter_map_schema_golden

- result: PASS
- checks_run: 2839
- passed_checks: 2839
- approx_tokens_if_applicable: n/a
- related_paths: .aide/tools/latest-tool-adapter-map.json, .aide/tools/tool-adapter-map.schema.json
- notes: Checks tool adapter-map schema and advisory mapping output.

### tool_fate_no_delete_approval_golden

- result: PASS
- checks_run: 8
- passed_checks: 8
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/tool-fates.yaml, .aide/tools/latest-tool-classification.json, .aide/tools/latest-tool-wrap-plan.json
- notes: Checks tool fate vocabulary never becomes deletion or execution approval.

### tool_inventory_schema_golden

- result: PASS
- checks_run: 23
- passed_checks: 23
- approx_tokens_if_applicable: n/a
- related_paths: .aide/tools/latest-tool-inventory.json, .aide/tools/tool-inventory.schema.json
- notes: Checks tool inventory schema and generated inventory shape.

### tool_record_schema_golden

- result: PASS
- checks_run: 13
- passed_checks: 13
- approx_tokens_if_applicable: n/a
- related_paths: .aide/tools/tool-record.schema.json
- notes: Checks tool record schema shape.

### tool_wrap_plan_schema_golden

- result: PASS
- checks_run: 2843
- passed_checks: 2843
- approx_tokens_if_applicable: n/a
- related_paths: .aide/tools/latest-tool-wrap-plan.json, .aide/tools/tool-wrap-plan.schema.json
- notes: Checks tool wrap-plan schema and no-execution output shape.

### tools_no_execution_golden

- result: PASS
- checks_run: 2864
- passed_checks: 2864
- approx_tokens_if_applicable: n/a
- related_paths: .aide/tools/latest-tool-adapter-map.json, .aide/tools/latest-tool-classification.json, .aide/tools/latest-tool-inventory.json, .aide/tools/latest-tool-wrap-plan.json
- notes: Checks Q41 tool outputs never enable unknown execution, apply, rename, deletion, or migration.

### verifier-detects-bad-evidence

- result: PASS
- checks_run: 3
- passed_checks: 3
- approx_tokens_if_applicable: n/a
- related_paths: .aide/evals/golden-tasks/verifier-detects-bad-evidence/fixtures/missing-sections.md, .aide/verification/evidence-packet.template.md
- notes: Passes when the verifier refuses to accept malformed evidence silently.

### workunit_idempotency_golden

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/recovery.yaml, .aide/policies/work-units.yaml, .aide/reports/aide-workunit-recovery-standard.md
- notes: Checks WorkUnit idempotency and no-op behavior.

### workunit_sizing_policy_golden

- result: PASS
- checks_run: 12
- passed_checks: 12
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/workunit-sizing.yaml
- notes: Checks WorkUnit sizing policy anchors and split gates.

## Limitations

- Deterministic local checks only.
- No model/provider/network calls.
- No external benchmark or arbitrary code semantic proof.
