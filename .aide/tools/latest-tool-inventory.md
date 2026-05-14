# Tool Inventory

- generated_by: aide-lite
- source_commit: 9b5b0ba5da291c9366d25dc708b11b4a73c0bcb1
- tool_count: 200
- no_apply: true
- execution_allowed: false
- tool_deletion: false
- tool_rename: false
- tool_migration: false

## Capability Counts

- audit: 37
- context: 84
- docs: 11
- generate: 13
- install: 7
- package: 1
- release: 12
- repo_policy: 56
- test: 82
- unknown: 16
- validate: 35

## Tools

- `.aide/adapters/templates/continue-checks.template.md`: capabilities=validate risk=medium fate=wrap
- `.aide/cache/latest-cache-keys.json`: capabilities=test risk=medium fate=wrap
- `.aide/cache/latest-cache-keys.md`: capabilities=test risk=medium fate=wrap
- `.aide/changelog/RELEASE_NOTES.preview.md`: capabilities=release risk=release fate=wrap
- `.aide/changelog/latest-changelog-report.md`: capabilities=audit,repo_policy,test risk=medium fate=wrap
- `.aide/changelog/release-notes.preview.json`: capabilities=release risk=release fate=wrap
- `.aide/changelog/templates/release-notes.md.template`: capabilities=release risk=release fate=wrap
- `.aide/compat/upgrade-gates.yaml`: capabilities=install risk=medium fate=wrap
- `.aide/context/latest-context-packet.md`: capabilities=context,test risk=medium fate=wrap
- `.aide/context/latest-review-packet.md`: capabilities=context,test risk=medium fate=wrap
- `.aide/context/latest-task-packet.md`: capabilities=context,test risk=medium fate=wrap
- `.aide/context/test-map.json`: capabilities=context,test risk=medium fate=wrap
- `.aide/controller/latest-outcome-report.md`: capabilities=audit,repo_policy,test risk=medium fate=wrap
- `.aide/controller/latest-recommendations.md`: capabilities=test risk=medium fate=wrap
- `.aide/evals/runs/latest-golden-tasks.json`: capabilities=test risk=medium fate=wrap
- `.aide/evals/runs/latest-golden-tasks.md`: capabilities=test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/checksums.json`: capabilities=context,validate risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/export-report.md`: capabilities=audit,context,repo_policy risk=low fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/adapters/templates/continue-checks.template.md`: capabilities=context,validate risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/changelog/templates/release-notes.md.template`: capabilities=context,release risk=release fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/git/sync-policy.md`: capabilities=context,repo_policy risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/hooks/commit-msg`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/import-policy.template.yaml`: capabilities=context,repo_policy risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/import-report.template.md`: capabilities=audit,context,repo_policy risk=low fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/policies/export-import.yaml`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/policies/sync-policy.yaml`: capabilities=context,repo_policy risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/policies/test-map.yaml`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/quality/test-coverage-map.schema.json`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/refactors/rollback-notes.schema.json`: capabilities=context,install risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/repo/test-map.schema.json`: capabilities=context,repo_policy,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/aide_lite.py`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_adapter_compiler.py`: capabilities=context,generate,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_aide_lite.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_cache_local_state.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_export_import.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_gateway_commands.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_golden_tasks.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_outcome_controller.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_provider_adapter.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q27_commit_recovery.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q28_git_workflow.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q29_git_helper.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q31_export_pack_governance.py`: capabilities=context,repo_policy,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q34_changelog_release.py`: capabilities=context,release,test risk=release fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q35_github_advisory.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q36_intent_compiler.py`: capabilities=context,generate,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q37_repo_intelligence.py`: capabilities=context,repo_policy,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q38_file_quality.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q39_refactor_control.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q40_root_recycling.py`: capabilities=context,repo_policy,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q41_tool_absorption.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_review_pack.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_router_profile.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_token_ledger.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_verifier.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/README.md`: capabilities=context,docs risk=low fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-adapter-map.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-capability.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-evidence.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-inventory.schema.json`: capabilities=context risk=low fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-record.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-retirement.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-risk.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/.aide/tools/tool-wrap-plan.schema.json`: capabilities=context risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/core/gateway/tests/test_gateway_skeleton.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/core/providers/tests/test_provider_contracts.py`: capabilities=context,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/docs/reference/aide-lite-test-runner.md`: capabilities=context,docs,test risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/files/docs/reference/cross-repo-pack-export-import.md`: capabilities=context,docs,repo_policy risk=low fate=wrap
- `.aide/export/aide-lite-pack-v0/import-policy.yaml`: capabilities=context,repo_policy risk=medium fate=wrap
- `.aide/export/aide-lite-pack-v0/install.md`: capabilities=context,install risk=medium fate=wrap
- `.aide/gateway/latest-gateway-status.json`: capabilities=test risk=medium fate=wrap
- `.aide/gateway/latest-gateway-status.md`: capabilities=test risk=medium fate=wrap
- `.aide/git/latest-helper-plan.json`: capabilities=test risk=medium fate=wrap
- `.aide/git/latest-helper-plan.md`: capabilities=test risk=medium fate=wrap
- `.aide/git/sync-policy.md`: capabilities=repo_policy risk=medium fate=wrap
- `.aide/github/latest-github-status.md`: capabilities=test risk=medium fate=wrap
- `.aide/hooks/commit-msg`: capabilities=unknown risk=unknown fate=unknown
- `.aide/import/import-policy.yaml`: capabilities=repo_policy risk=medium fate=wrap
- `.aide/import/import-report.template.md`: capabilities=audit,repo_policy risk=low fate=wrap
- `.aide/intake/latest-intent-packet.json`: capabilities=context,test risk=medium fate=wrap

## Warnings

- unknown_tool_candidates: .aide/hooks/commit-msg, .aide/policies/export-import.yaml, .aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/importer-scope-repair.md, .aide/tools/tool-adapter-map.schema.json, .aide/tools/tool-capability.schema.json, .aide/tools/tool-evidence.schema.json, .aide/tools/tool-inventory.schema.json, .aide/tools/tool-record.schema.json, .aide/tools/tool-retirement.schema.json, .aide/tools/tool-risk.schema.json, .aide/tools/tool-wrap-plan.schema.json, scripts/aide-queue-next
- high_risk_tool_candidates: .aide/changelog/RELEASE_NOTES.preview.md, .aide/changelog/release-notes.preview.json, .aide/changelog/templates/release-notes.md.template, .aide/export/aide-lite-pack-v0/files/.aide/changelog/templates/release-notes.md.template, .aide/export/aide-lite-pack-v0/files/.aide/scripts/tests/test_q34_changelog_release.py, .aide/queue/Q34-changelog-release-notes-generator-v0/evidence/export-pack-sync.md, .aide/queue/Q34-changelog-release-notes-generator-v0/evidence/release-notes-preview-report.md, governance/release-policy.md, packaging/catalogs/release-channel-catalog.yaml, packaging/checklists/release-checklist.md, packaging/release-policy.md, scripts/maintenance/release-readiness-checklist.md

## Next

- Q42 Move Map / Salvage Map / Path Alias v0.
