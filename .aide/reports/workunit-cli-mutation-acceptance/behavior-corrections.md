# WorkUnit CLI Mutation Acceptance Behavior Corrections

- status: PASS_WITH_WARNINGS
- implementation_defect: false
- controlled_apply_queue_local: True

## Corrected Results
- PASS: workunit_block_dry_run_live_corrected (exit 0) - Direct quoted note dry-run passed and wrote no queue files.
- PASS: controlled_create_apply_corrected (exit 0) - Temp-root apply created only queue metadata after accepted protocol files were copied into temp root.
- PASS: controlled_block_apply_corrected (exit 0) - Temp-root block apply updated status and blocker evidence only.
- PASS: controlled_evidence_add_apply_corrected (exit 0) - Temp-root evidence add wrote pointer metadata only.
- PASS: controlled_evidence_secret_reject_corrected (exit 1) - Secret-like path rejected fail-closed.
- PASS: controlled_unknown_task_block_corrected (exit 1) - Unknown task rejected fail-closed.
