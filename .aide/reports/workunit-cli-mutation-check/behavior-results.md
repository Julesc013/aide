# WorkUnit CLI Mutation Check Behavior Results

- status: PASS
- direct_python_version: Python 3.14.5
- commands_run: 34
- commands_failed: 0
- live_dry_run_queue_hashes_unchanged: true
- controlled_apply_locality_ok: true
- symlink_escape_check: checked

## Commands

- py_compile: exit 0, expected 0, result True
- unittest_workunit_cli_mutation: exit 0, expected 0, result True
- unittest_workunit_cli: exit 0, expected 0, result True
- unittest_workunit_queue_v1: exit 0, expected 0, result True
- unittest_evidence_packet_schema: exit 0, expected 0, result True
- unittest_contract_envelope: exit 0, expected 0, result True
- unittest_lifecycle_fixture_runner: exit 0, expected 0, result True
- workunit_status: exit 0, expected 0, result True
- workunit_list: exit 0, expected 0, result True
- workunit_inspect_build: exit 0, expected 0, result True
- workunit_validate: exit 0, expected 0, result True
- workunit_create_dry_run: exit 0, expected 0, result True
- workunit_block_dry_run: exit 0, expected 0, result True
- workunit_evidence_add_dry_run: exit 0, expected 0, result True
- workunit_claim_unsupported: exit 2, expected nonzero, result True
- workunit_run_unsupported: exit 2, expected nonzero, result True
- workunit_finish_unsupported: exit 2, expected nonzero, result True
- workunit_repair_unsupported: exit 2, expected nonzero, result True
- workunit_create_neither_mode: exit 2, expected nonzero, result True
- workunit_create_both_modes: exit 2, expected nonzero, result True
- workunit_block_neither_mode: exit 2, expected nonzero, result True
- workunit_evidence_add_invalid_role: exit 2, expected nonzero, result True
- create_parent_traversal_id: exit 1, expected nonzero, result True
- create_separator_id: exit 1, expected nonzero, result True
- create_hidden_id: exit 1, expected nonzero, result True
- create_wildcard_id: exit 1, expected nonzero, result True
- block_unknown_task: exit 1, expected nonzero, result True
- evidence_unknown_task: exit 1, expected nonzero, result True
- evidence_absolute_external_path: exit 1, expected nonzero, result True
- evidence_secret_like_path: exit 1, expected nonzero, result True
- evidence_symlink_escape: exit 1, expected nonzero, result True
- apply_create_controlled_cli: exit 0, expected 0, result True
- apply_block_controlled_cli: exit 0, expected 0, result True
- apply_evidence_add_controlled_cli: exit 0, expected 0, result True
