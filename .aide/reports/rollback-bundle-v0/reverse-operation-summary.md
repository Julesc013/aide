# RollbackBundle v0 Reverse Operation Summary

- reverse_operation_count: 15
- reverse_operations_are_plans_not_actions: true

- `aide://rollback-bundle/reverse-operation/runtime-generated-local-state` manual_review_required for `.aide.local/**`
- `aide://rollback-bundle/reverse-operation/project-generated-context` regenerate_project_output for `.aide/context/generated/context-pack.json`
- `aide://rollback-bundle/reverse-operation/preserved-legacy-state` manual_review_required for `.aide/legacy/**`
- `aide://rollback-bundle/reverse-operation/project-overlay-policy` manual_review_required for `.aide/project-overlays/policy.yaml`
- `aide://rollback-bundle/reverse-operation/vendor-file-project-lock-schema` restore_managed_file_preimage for `.aide/protocol/aide-project-lock-v0.schema.json`
- `aide://rollback-bundle/reverse-operation/evidence-only-queue-evidence` manual_review_required for `.aide/queue/**/evidence/**`
- `aide://rollback-bundle/reverse-operation/vendor-file-aide-lite-cli` restore_managed_file_preimage for `.aide/scripts/aide_lite.py`
- `aide://rollback-bundle/reverse-operation/never-touch-git` refuse for `.git/**`
- `aide://rollback-bundle/reverse-operation/vendor-section-agents-summary` restore_managed_section_preimage for `AGENTS.md`
- `aide://rollback-bundle/reverse-operation/project-owned-readme` manual_review_required for `README.md`
- `aide://rollback-bundle/reverse-operation/local-only-operator-state` manual_review_required for `local-only/**`
- `aide://rollback-bundle/reverse-operation/unknown-unclassified` manual_review_required for `unclassified/**`
- `aide://rollback-bundle/reverse-operation/restore-project-lock` restore_project_lock for `None`
- `aide://rollback-bundle/reverse-operation/restore-install-record` restore_install_record for `None`
- `aide://rollback-bundle/reverse-operation/restore-ownership-ledger` restore_ownership_ledger for `None`
