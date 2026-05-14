# Test Coverage Map

- tests_detected: 36

## Likely Test Targets

- .aide/scripts/tests/test_adapter_compiler.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_aide_lite.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_cache_local_state.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_export_import.py: .aide/policies/export-import.yaml, .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_gateway_commands.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_golden_tasks.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_outcome_controller.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_provider_adapter.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q27_commit_recovery.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q28_git_workflow.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q29_git_helper.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q30_aide_dev_main_policy.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q31_export_pack_governance.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q34_changelog_release.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q35_github_advisory.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q36_intent_compiler.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q37_repo_intelligence.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q38_file_quality.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_review_pack.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_router_profile.py: .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_token_ledger.py: .aide/policies/token-ledger.yaml, .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_verifier.py: .aide/scripts/aide_lite.py
- core/compat/tests/__init__.py:
- core/compat/tests/test_compat_baseline.py:
- core/gateway/tests/__init__.py:
- core/gateway/tests/test_gateway_skeleton.py:
- core/harness/tests/__init__.py:
- core/harness/tests/test_aide_lite.py:
- core/harness/tests/test_aide_verifier.py:
- core/providers/tests/__init__.py:
- core/providers/tests/test_provider_contracts.py:
- core/tests/README.md:
- shared/tests/README.md:
- shared/tests/__init__.py:
- shared/tests/test_boot_slice_cli.py:
- shared/tests/test_boot_slice_runtime.py:

## Missing Test Or Validator Candidates

- core/compat/__init__.py (source, compatibility baseline)
- core/compat/migration_registry.py (source, compatibility baseline)
- core/compat/replay_manifest.py (source, compatibility baseline)
- core/compat/version_registry.py (source, compatibility baseline)
- core/gateway/__init__.py (source, gateway skeleton)
- core/gateway/gateway_status.py (source, gateway skeleton)
- core/gateway/server.py (source, gateway skeleton)
- core/harness/__init__.py (source, AIDE harness)
- core/harness/aide_harness.py (source, AIDE harness)
- core/harness/commands.py (source, AIDE harness)
- core/harness/contract_loader.py (source, AIDE harness)
- core/harness/diagnostics.py (source, AIDE harness)
- core/harness/generated_artifacts.py (source, AIDE harness)
- core/providers/__init__.py (source, provider metadata and contracts)
- core/providers/contracts.py (source, provider metadata and contracts)
- core/providers/registry.py (source, provider metadata and contracts)
- core/providers/status.py (source, provider metadata and contracts)
- hosts/apple/xcode/companion/run_boot_slice.py (source, host adapters)
- hosts/metrowerks/codewarrior/companion/run_boot_slice.py (source, host adapters)
- hosts/metrowerks/codewarrior/ide-sdk/run_boot_slice.py (source, host adapters)
- hosts/microsoft/visual-studio-mac/companion/run_boot_slice.py (source, host adapters)
- hosts/microsoft/visual-studio/com-addin/run_boot_slice.py (source, host adapters)
- hosts/microsoft/visual-studio/extensibility/run_boot_slice.py (source, host adapters)
- hosts/microsoft/visual-studio/vsix-v1/run_boot_slice.py (source, host adapters)
- scripts/aide (tool, AIDE harness)
- scripts/aide-queue-next (tool, AIDE harness)
- scripts/aide-queue-run (tool, AIDE harness)
- scripts/aide-queue-status (tool, AIDE harness)
- scripts/maintenance/task-catalog.yaml (tool, unknown)
- shared/__init__.py (source, unknown)
- shared/cli/__init__.py (source, unknown)
- shared/cli/__main__.py (source, unknown)
- shared/cli/main.py (source, unknown)
- shared/config/__init__.py (source, unknown)
- shared/config/boot_slice.py (source, unknown)
- shared/core/__init__.py (source, unknown)
- shared/core/boot_slice.py (source, unknown)
- shared/core/dispatcher.py (source, unknown)
- shared/diagnostics/__init__.py (source, unknown)
- shared/diagnostics/models.py (source, unknown)
- shared/protocol/__init__.py (source, unknown)
- shared/protocol/models.py (source, unknown)

## Caveats

- test targets are heuristic
- validators are not executed by Q38
