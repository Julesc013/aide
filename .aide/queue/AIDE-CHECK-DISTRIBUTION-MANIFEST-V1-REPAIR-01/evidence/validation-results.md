# Validation Results

```json
{
  "commands": [
    [
      "git",
      "diff",
      "--check"
    ],
    [
      "git",
      "diff",
      "--cached",
      "--check"
    ],
    [
      "py",
      "-3",
      "-m",
      "json.tool",
      ".aide/protocol/aide-distribution-manifest-v1.schema.json"
    ],
    [
      "py",
      "-3",
      "-m",
      "compileall",
      "core/protocol",
      ".aide/scripts/tests"
    ],
    [
      "py",
      "-3",
      "-m",
      "unittest",
      "discover",
      "-s",
      ".aide/scripts/tests",
      "-p",
      "test_aide_distribution_manifest_v1.py"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "distribution-manifest",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "distribution-manifest",
      "project"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "distribution-manifest",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "install",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "install",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "repair",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "repair",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "upgrade",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "upgrade",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "upgrade",
      "compatibility"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "rollback",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "rollback",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "uninstall",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "uninstall",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "release",
      "validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "release",
      "status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "release",
      "draft-validate"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "release",
      "draft-status"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "task",
      "inspect",
      "--task-id",
      "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "task",
      "evidence",
      "--task-id",
      "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "task",
      "inspect",
      "--task-id",
      "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "task",
      "evidence",
      "--task-id",
      "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
    ],
    [
      "py",
      "-3",
      ".aide/scripts/aide_lite.py",
      "validate"
    ]
  ],
  "failing": [],
  "results": [
    {
      "actual_command": [
        "git",
        "diff",
        "--check"
      ],
      "command": [
        "git",
        "diff",
        "--check"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": ""
    },
    {
      "actual_command": [
        "git",
        "diff",
        "--cached",
        "--check"
      ],
      "command": [
        "git",
        "diff",
        "--cached",
        "--check"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": ""
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 -m json.tool .aide/protocol/aide-distribution-manifest-v1.schema.json"
      ],
      "command": [
        "py",
        "-3",
        "-m",
        "json.tool",
        ".aide/protocol/aide-distribution-manifest-v1.schema.json"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "{\n    \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n    \"$id\": \"https://aide.dev/schemas/aide-distribution-manifest-v1.schema.json\",\n    \"title\": \"AIDE DistributionManifest v1\",\n    \"type\": \"object\",\n    \"additionalProperties\": false,\n    \"required\": [\n        \"apiVersion\",\n        \"kind\",\n        \"schema_version\",\n        \"metadata\",\n        \"spec\",\n        \"status\"\n    ],\n    \"properties\": {\n        \"apiVersion\": {\n            \"type\": \"string\",\n            \"const\": \"aide.dev/v1alpha1\"\n        },\n        \"kind\": {\n            \"type\": \"string\",\n            \"const\": \"DistributionManifest\"\n        },\n        \"schema_version\": {\n            \"type\": \"string\",\n            \"const\": \"aide.distribution-manifest.v1\"\n        },\n        \"metadata\": {\n            \"type\": \"object\",\n            \"additionalProperties\": false,\n            \"required\": [\n                \"distribution_ref\",\n                \"name\",\n                \"product\",\n                \"format_version\",\n                \"release_id\",\n                \"release_version\",\n                \"channel\",\n                \"source_revision\",\n                \"source_tree_digest\",\n                \"build_implementation\",\n                \"projection_implementation\",\n                \"timestamp_classification\"\n            ],\n            \"properties\": {\n                \"distribution_ref\": {\n                    \"type\": \"string\",\n                    \"pattern\": \"^aide://distribution/[A-Za-z0-9_.-]+$\"\n                },\n                \"name\": {\n                    \"type\": \"string\",\n                    \"minLength\": 1\n                },\n                \"product\": {\n                    \"type\": \"string\",\n                    \"minLength\": 1\n                },\n                \"format_version\": {\n                    \"type\": \"string\",\n  \n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 -m compileall core/protocol .aide/scripts/tests"
      ],
      "command": [
        "py",
        "-3",
        "-m",
        "compileall",
        "core/protocol",
        ".aide/scripts/tests"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "Listing 'core/protocol'...\nListing '.aide/scripts/tests'...\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_distribution_manifest_v1.py"
      ],
      "command": [
        "py",
        "-3",
        "-m",
        "unittest",
        "discover",
        "-s",
        ".aide/scripts/tests",
        "-p",
        "test_aide_distribution_manifest_v1.py"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "..................\n----------------------------------------------------------------------\nRan 18 tests in 35.505s\n\nOK\n",
      "stdout_excerpt": ""
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py distribution-manifest status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "distribution-manifest",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite distribution-manifest status\nresult: PASS_WITH_WARNINGS\nschema_exists: true\nhelper_exists: true\nq47_release_bundle_exists: true\nmanifest_report_exists: true\nvalidation_report_exists: true\nrecommended_next_task: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01\nproposed_capability: distribution_manifest_v1\ninstall_apply_implemented: false\nupdate_apply_implemented: false\nrepair_apply_implemented: false\nrollback_apply_implemented: false\nuninstall_apply_implemented: false\nrelease_publication_implemented: false\ntarget_repository_mutation_implemented: false\nbranch_worktree_automation_implemented: false\nnetwork_calls_implemented: false\nprovider_model_calls_implemented: false\ngithub_release_creation_implemented: false\ngit_tag_creation_implemented: false\nupload_implemented: false\nworkbench_runtime_implemented: false\nmcp_runtime_implemented: false\nsource_change_preview_apply_rollback_implemented: false\npromotion_implemented: false\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py distribution-manifest project"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "distribution-manifest",
        "project"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite distribution-manifest project\nresult: PASS_WITH_WARNINGS\nmanifest_path: .aide/reports/distribution-manifest-v1/manifest.json\ncomponent_count: 1\nartifact_count: 12\ndistribution_digest: sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569\nsource_artifacts_mutated: false\nrecommended_next_task: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01\nproposed_capability: distribution_manifest_v1\ninstall_apply_implemented: false\nupdate_apply_implemented: false\nrepair_apply_implemented: false\nrollback_apply_implemented: false\nuninstall_apply_implemented: false\nrelease_publication_implemented: false\ntarget_repository_mutation_implemented: false\nbranch_worktree_automation_implemented: false\nnetwork_calls_implemented: false\nprovider_model_calls_implemented: false\ngithub_release_creation_implemented: false\ngit_tag_creation_implemented: false\nupload_implemented: false\nworkbench_runtime_implemented: false\nmcp_runtime_implemented: false\nsource_change_preview_apply_rollback_implemented: false\npromotion_implemented: false\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py distribution-manifest validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "distribution-manifest",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite distribution-manifest validate\nresult: PASS_WITH_WARNINGS\nschema_exists: true\nhelper_exists: true\ncli_registered: true\nmanifest_generated: true\nmanifest_valid: true\nschema_alignment: true\nfixture_matrix_passed: true\nreordered_input_same_digest: true\nq47_release_bundle_mapped: true\nq48_not_distribution_truth: true\ninstall_apply_not_implemented: true\nrelease_publication_not_implemented: true\ntarget_repository_mutation_not_implemented: true\nabsolute_local_paths_suppressed: true\nerror_count: 0\nrecommended_next_task: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01\nproposed_capability: distribution_manifest_v1\ninstall_apply_implemented: false\nupdate_apply_implemented: false\nrepair_apply_implemented: false\nrollback_apply_implemented: false\nuninstall_apply_implemented: false\nrelease_publication_implemented: false\ntarget_repository_mutation_implemented: false\nbranch_worktree_automation_implemented: false\nnetwork_calls_implemented: false\nprovider_model_calls_implemented: false\ngithub_release_creation_implemented: false\ngit_tag_creation_implemented: false\nupload_implemented: false\nworkbench_runtime_implemented: false\nmcp_runtime_implemented: false\nsource_change_preview_apply_rollback_implemented: false\npromotion_implemented: false\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py install validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "install",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite install validate\nresult: PASS\n- PASS Q43 required file exists: .aide/policies/install.yaml\n- PASS Q43 required file exists: .aide/policies/install-preservation.yaml\n- PASS Q43 required file exists: .aide/policies/install-ownership.yaml\n- PASS Q43 required file exists: .aide/policies/install-conflicts.yaml\n- PASS Q43 required file exists: .aide/policies/install-migrations.yaml\n- PASS Q43 required file exists: .aide/policies/install-verification.yaml\n- PASS Q43 required file exists: .aide/install/install-observation.schema.json\n- PASS Q43 required file exists: .aide/install/install-plan.schema.json\n- PASS Q43 required file exists: .aide/install/install-operation.schema.json\n- PASS Q43 required file exists: .aide/install/install-dry-run.schema.json\n- PASS Q43 required file exists: .aide/install/ownership-ledger.schema.json\n- PASS Q43 required file exists: .aide/install/ownership-record.schema.json\n- PASS Q43 required file exists: .aide/install/conflict-report.schema.json\n- PASS Q43 required file exists: .aide/install/conflict-record.schema.json\n- PASS Q43 required file exists: .aide/install/preservation-report.schema.json\n- PASS Q43 required file exists: .aide/install/managed-section.schema.json\n- PASS Q43 required file exists: .aide/install/install-verification.schema.json\n- PASS Q43 required file exists: .aide/install/README.md\n- PASS .aide/policies/install.yaml contains anchor: aide.install-policy.v0\n- PASS .aide/policies/install.yaml contains anchor: observe_plan_dry_run_only\n- PASS .aide/policies/install.yaml contains anchor: no_apply_in_q43\n- PASS .aide/policies/install.yaml contains anchor: no_target_mutation\n- PASS .aide/policies/install-preservation.yaml contains anchor: .aide/memory/**\n- PASS .aide/policies/install-preservation.yaml contains anchor: .ai\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py install status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "install",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite install status\nobservation: present\nplan: present\ndry_run: present\noperations: 462\nconflicts: 458\nmandatory_migration_candidates: 0\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py repair validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "repair",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite repair validate\nresult: PASS\n- PASS Q44 required file exists: .aide/policies/repair.yaml\n- PASS Q44 required file exists: .aide/policies/repair-classes.yaml\n- PASS Q44 required file exists: .aide/policies/repair-safety.yaml\n- PASS Q44 required file exists: .aide/policies/repair-detection.yaml\n- PASS Q44 required file exists: .aide/policies/repair-verification.yaml\n- PASS Q44 required file exists: .aide/policies/doctor.yaml\n- PASS Q44 required file exists: .aide/repair/repair-observation.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-diagnosis.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-plan.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-operation.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-dry-run.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-report.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-classification.schema.json\n- PASS Q44 required file exists: .aide/repair/doctor-report.schema.json\n- PASS Q44 required file exists: .aide/repair/repair-verification.schema.json\n- PASS Q44 required file exists: .aide/repair/README.md\n- PASS .aide/policies/repair.yaml contains anchor: aide.repair-policy.v0\n- PASS .aide/policies/repair.yaml contains anchor: observe_plan_dry_run_only\n- PASS .aide/policies/repair.yaml contains anchor: no_apply_in_q44\n- PASS .aide/policies/repair.yaml contains anchor: no_target_mutation\n- PASS .aide/policies/repair-classes.yaml contains anchor: missing_portable_file\n- PASS .aide/policies/repair-classes.yaml contains anchor: tracked_local_state\n- PASS .aide/policies/repair-classes.yaml contains anchor: future_apply_allowed\n- PASS .aide/policies/repair-classes.yaml contains anchor: rollback_note_required_if_future_apply\n- PASS .ai\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py repair status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "repair",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite repair status\nobservation: present\ndiagnosis: present\nplan: present\ndry_run: present\noperations: 11\nconflicts: 0\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py upgrade validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "upgrade",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite upgrade validate\nresult: PASS\n- PASS Q45 required file exists: .aide/policies/upgrade.yaml\n- PASS Q45 required file exists: .aide/policies/upgrade-compatibility.yaml\n- PASS Q45 required file exists: .aide/policies/upgrade-preservation.yaml\n- PASS Q45 required file exists: .aide/policies/upgrade-conflicts.yaml\n- PASS Q45 required file exists: .aide/policies/upgrade-migrations.yaml\n- PASS Q45 required file exists: .aide/policies/upgrade-verification.yaml\n- PASS Q45 required file exists: .aide/upgrade/current-install-observation.schema.json\n- PASS Q45 required file exists: .aide/upgrade/source-pack-observation.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-comparison.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-plan.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-operation.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-dry-run.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-conflict-report.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-migration-report.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-verification.schema.json\n- PASS Q45 required file exists: .aide/upgrade/upgrade-compatibility-report.schema.json\n- PASS Q45 required file exists: .aide/upgrade/README.md\n- PASS .aide/policies/upgrade.yaml contains anchor: aide.upgrade-policy.v0\n- PASS .aide/policies/upgrade.yaml contains anchor: observe_compare_plan_dry_run_only\n- PASS .aide/policies/upgrade.yaml contains anchor: no_apply_in_q45\n- PASS .aide/policies/upgrade.yaml contains anchor: no_target_mutation\n- PASS .aide/policies/upgrade-compatibility.yaml contains anchor: pack_schema_version\n- PASS .aide/policies/upgrade-compatibility.yaml contains anchor: compatible_with_w\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py upgrade status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "upgrade",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite upgrade status\ncurrent_observation: present\nsource_observation: present\ncomparison: present\nplan: present\ndry_run: present\nplanned_updates: 5\nplanned_skips: 8\nplanned_preservations: 209\nplanned_conflicts: 209\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py upgrade compatibility"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "upgrade",
        "compatibility"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite upgrade compatibility\npath: .aide/upgrade/latest-upgrade-compatibility-report.md\nunsupported_count: 8\nunknown_count: 0\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py rollback validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "rollback",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite rollback validate\nresult: PASS\n- PASS Q46 rollback required file exists: .aide/policies/rollback.yaml\n- PASS Q46 rollback required file exists: .aide/policies/rollback-classes.yaml\n- PASS Q46 rollback required file exists: .aide/policies/rollback-safety.yaml\n- PASS Q46 rollback required file exists: .aide/policies/rollback-verification.yaml\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-observation.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-plan.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-operation.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-dry-run.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-verification.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/rollback-report.schema.json\n- PASS Q46 rollback required file exists: .aide/rollback/README.md\n- PASS .aide/policies/rollback.yaml contains anchor: aide.rollback-policy.v0\n- PASS .aide/policies/rollback.yaml contains anchor: observe_plan_dry_run_only\n- PASS .aide/policies/rollback.yaml contains anchor: no_apply_in_q46\n- PASS .aide/policies/rollback.yaml contains anchor: no_managed_section_removal\n- PASS .aide/policies/rollback-classes.yaml contains anchor: restore_previous_portable_file_future\n- PASS .aide/policies/rollback-classes.yaml contains anchor: blocked_missing_ledger\n- PASS .aide/policies/rollback-classes.yaml contains anchor: blocked_local_state_or_secret\n- PASS .aide/policies/rollback-safety.yaml contains anchor: no_rollback_without_ownership_or_plan_evidence\n- PASS .aide/policies/rollback-safety.yaml contains anchor: no_deletion_of_existing_tools\n- PASS .aide/policies/rollback-safety.yaml contains anchor: no_target_mutation_in\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py rollback status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "rollback",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite rollback status\nobservation: present\nplan: present\ndry_run: present\nfuture_actions: 5\npreservations: 224\nblockers: 0\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py uninstall validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "uninstall",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite uninstall validate\nresult: PASS\n- PASS Q46 uninstall required file exists: .aide/policies/uninstall.yaml\n- PASS Q46 uninstall required file exists: .aide/policies/uninstall-classes.yaml\n- PASS Q46 uninstall required file exists: .aide/policies/uninstall-safety.yaml\n- PASS Q46 uninstall required file exists: .aide/policies/uninstall-verification.yaml\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-observation.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-plan.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-operation.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-dry-run.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-verification.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/uninstall-report.schema.json\n- PASS Q46 uninstall required file exists: .aide/uninstall/README.md\n- PASS .aide/policies/uninstall.yaml contains anchor: aide.uninstall-policy.v0\n- PASS .aide/policies/uninstall.yaml contains anchor: observe_plan_dry_run_only\n- PASS .aide/policies/uninstall.yaml contains anchor: no_apply_in_q46\n- PASS .aide/policies/uninstall.yaml contains anchor: no broad `.aide` deletion\n- PASS .aide/policies/uninstall-classes.yaml contains anchor: remove_portable_file_future\n- PASS .aide/policies/uninstall-classes.yaml contains anchor: preserve_target_memory\n- PASS .aide/policies/uninstall-classes.yaml contains anchor: blocked_missing_ledger\n- PASS .aide/policies/uninstall-safety.yaml contains anchor: uninstall_is_not_rm_rf_aide\n- PASS .aide/policies/uninstall-safety.yaml contains anchor: blanket_aide_deletion_forbidden\n- PASS .aide/policies/uninstall-safety.yaml contains anchor: local_state_or_s\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py uninstall status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "uninstall",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite uninstall status\nobservation: present\nplan: present\ndry_run: present\nfuture_removal_candidates: 233\npreservations: 885\nunknown_ownership_count: 672\nblockers: 0\nno_apply: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py release validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "release",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite release validate\nresult: PASS\n- PASS release model file exists: .aide/policies/release-bundle.yaml\n- PASS release model file exists: .aide/policies/release-artifacts.yaml\n- PASS release model file exists: .aide/policies/release-provenance.yaml\n- PASS release model file exists: .aide/policies/release-validation.yaml\n- PASS release model file exists: .aide/policies/release-versioning.yaml\n- PASS release model file exists: .aide/release/release-bundle.schema.json\n- PASS release model file exists: .aide/release/release-asset.schema.json\n- PASS release model file exists: .aide/release/release-manifest.schema.json\n- PASS release model file exists: .aide/release/release-checksums.schema.json\n- PASS release model file exists: .aide/release/release-provenance.schema.json\n- PASS release model file exists: .aide/release/release-validation.schema.json\n- PASS release model file exists: .aide/release/release-bundle-report.schema.json\n- PASS release model file exists: .aide/release/release-install-notes.schema.json\n- PASS release model file exists: .aide/release/README.md\n- PASS release policy .aide/policies/release-bundle.yaml contains anchor: aide.release-bundle-policy.v0\n- PASS release policy .aide/policies/release-bundle.yaml contains anchor: local_artifact_generation_only\n- PASS release policy .aide/policies/release-bundle.yaml contains anchor: no_publish_in_q47\n- PASS release policy .aide/policies/release-bundle.yaml contains anchor: no_tag_creation\n- PASS release policy .aide/policies/release-bundle.yaml contains anchor: no_github_release_creation\n- PASS release policy .aide/policies/release-artifacts.yaml contains anchor: zip_archive\n- PASS release policy .aide/policies/release-artifacts.yaml contains anchor: tar_gz_archive\n- PASS release policy .aide/policies/releas\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py release status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "release",
        "status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite release status\nbundle_id: aide-lite-pack-v0-2b2a00f7c4628311\nartifact_count: 11\nvalidation_result: PASS\nzip: .aide/release/dist/aide-lite-pack-v0.zip\ntar_gz: .aide/release/dist/aide-lite-pack-v0.tar.gz\nno_publish: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py release draft-validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "release",
        "draft-validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite release draft-validate\nresult: PASS\n- PASS github release draft model file exists: .aide/policies/github-release-draft.yaml\n- PASS github release draft model file exists: .aide/policies/release-publication-boundary.yaml\n- PASS github release draft model file exists: .aide/policies/release-upload-plan.yaml\n- PASS github release draft model file exists: .aide/policies/release-checklist.yaml\n- PASS github release draft model file exists: .aide/release/github-release-draft.schema.json\n- PASS github release draft model file exists: .aide/release/github-release-asset.schema.json\n- PASS github release draft model file exists: .aide/release/github-release-upload-plan.schema.json\n- PASS github release draft model file exists: .aide/release/github-release-checklist.schema.json\n- PASS github release draft model file exists: .aide/release/github-release-publication-boundary.schema.json\n- PASS github release draft model file exists: .aide/release/github-release-draft-validation.schema.json\n- PASS github release draft policy .aide/policies/github-release-draft.yaml contains anchor: aide.github-release-draft-policy.v0\n- PASS github release draft policy .aide/policies/github-release-draft.yaml contains anchor: local_draft_generation_only\n- PASS github release draft policy .aide/policies/github-release-draft.yaml contains anchor: no_publish_in_q48\n- PASS github release draft policy .aide/policies/github-release-draft.yaml contains anchor: no_tag_creation\n- PASS github release draft policy .aide/policies/github-release-draft.yaml contains anchor: no_upload\n- PASS github release draft policy .aide/policies/release-publication-boundary.yaml contains anchor: create_git_tag\n- PASS github release draft policy .aide/policies/release-publication-boundary.yaml contains anchor: push_git\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py release draft-status"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "release",
        "draft-status"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite release draft-status\ndraft_id: aide-lite-pack-v0-github-draft-2b2a00f7c4628311\nsuggested_tag: aide-lite-pack-v0-draft-2b2a00f7c4628311\nasset_count: 12\nvalidation_result: PASS\npublication_status: local_draft_no_publish\nno_publish: true\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "task",
        "inspect",
        "--task-id",
        "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite task inspect\ntask_id: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01\nstatus: needs_review\nclassification: complete\ntask_yaml: .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/task.yaml\nstatus_yaml: .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/status.yaml\nevidence_dir: .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence\nevidence_files: 18\nmissing_evidence: 0\nrecovery_suggestion: noop_already_complete\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "task",
        "evidence",
        "--task-id",
        "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite task evidence\ntask_id: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01\navailable:\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/allowed-paths.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/campaign-state.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/changed-files.md\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/diff-check.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/finding-matrix.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/next-task-prompt.md\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/non-capabilities.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/path-scan.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/remaining-risks.md\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/secret-scan.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/source-chain.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/stop-conditions.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/test-results.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/turn-context.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/validation-commands.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/validation-plan.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/validation-results.json\n- .aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/validation.md\nmissing:\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "task",
        "inspect",
        "--task-id",
        "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite task inspect\ntask_id: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01\nstatus: needs_review\nclassification: complete\ntask_yaml: .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/task.yaml\nstatus_yaml: .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/status.yaml\nevidence_dir: .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence\nevidence_files: 22\nmissing_evidence: 0\nrecovery_suggestion: noop_already_complete\n"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "task",
        "evidence",
        "--task-id",
        "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite task evidence\ntask_id: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01\navailable:\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/artifact-integrity-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/baseline.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/changed-files.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/checksum-value-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/component-graph-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/contamination-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/digest-recomputation.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/extension-boundary-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/fixture-coverage-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/identity-boundary-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/independent_distribution_manifest_repair_check.py\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/next-task-prompt.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/nine-finding-check-matrix.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/no-overclaiming-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/preaccess-path-safety.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/protocol-range-review.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/q47-mapping-regression.md\n- .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/evidence/remaining-risks.md\n- .aide\n...[truncated]"
    },
    {
      "actual_command": [
        "C:\\Program Files\\PowerShell\\7\\pwsh.EXE",
        "-NoProfile",
        "-Command",
        "py -3 .aide/scripts/aide_lite.py validate"
      ],
      "command": [
        "py",
        "-3",
        ".aide/scripts/aide_lite.py",
        "validate"
      ],
      "exit_code": 0,
      "result": "PASS",
      "stderr_excerpt": "",
      "stdout_excerpt": "AIDE Lite validate\nstatus: PASS\n- PASS required file: .aide/policies/token-budget.yaml\n- PASS required file: .aide/memory/project-state.md\n- PASS required file: .aide/memory/decisions.md\n- PASS required file: .aide/memory/open-risks.md\n- PASS required file: .aide/prompts/compact-task.md\n- PASS required file: .aide/prompts/evidence-review.md\n- PASS required file: .aide/prompts/codex-token-mode.md\n- PASS required file: .aide/context/ignore.yaml\n- PASS context compiler config exists: .aide/context/compiler.yaml\n- PASS context compiler config exists: .aide/context/priority.yaml\n- PASS context compiler config exists: .aide/context/excerpt-policy.yaml\n- PASS verifier config exists: .aide/policies/verification.yaml\n- PASS verifier config exists: .aide/verification/evidence-packet.template.md\n- PASS verifier config exists: .aide/verification/review-packet.template.md\n- PASS verifier config exists: .aide/verification/review-decision-policy.yaml\n- PASS verifier config exists: .aide/verification/diff-scope-policy.yaml\n- PASS verifier config exists: .aide/verification/file-reference-policy.yaml\n- PASS verifier config exists: .aide/verification/secret-scan-policy.yaml\n- PASS token ledger artifact exists: .aide/policies/token-ledger.yaml\n- PASS token ledger artifact exists: .aide/reports/token-baselines.yaml\n- PASS token ledger artifact exists: .aide/reports/token-ledger.jsonl\n- PASS token ledger artifact exists: .aide/reports/token-savings-summary.md\n- PASS token ledger records: 83\n- PASS golden task artifact exists: .aide/policies/evals.yaml\n- PASS golden task artifact exists: .aide/evals/golden-tasks/README.md\n- PASS golden task artifact exists: .aide/evals/golden-tasks/catalog.yaml\n- PASS golden task definitions: 171\n- PASS golden task report tasks: 171\n- PASS golden task Markdow\n...[truncated]"
    }
  ]
}
```
