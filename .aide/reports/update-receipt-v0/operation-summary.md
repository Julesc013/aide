# UpdateReceipt v0 Operation Summary

Operation receipts record observed future execution facts only. They are not actions.

| Receipt | Class | Source Operation | Path | No Apply | No Mutation |
| --- | --- | --- | --- | --- | --- |
| aide://update-receipt/operation-receipt/runtime-generated-local-state | runtime_generated_preserved | aide://update-plan/operation/runtime-generated-local-state | .aide.local/** | true | true |
| aide://update-receipt/operation-receipt/project-generated-context | validation_skipped | aide://update-plan/operation/project-generated-context | .aide/context/generated/context-pack.json | true | true |
| aide://update-receipt/operation-receipt/preserved-legacy-state | legacy_preserved | aide://update-plan/operation/preserved-legacy-state | .aide/legacy/** | true | true |
| aide://update-receipt/operation-receipt/project-overlay-policy | project_overlay_preserved | aide://update-plan/operation/project-overlay-policy | .aide/project-overlays/policy.yaml | true | true |
| aide://update-receipt/operation-receipt/vendor-file-project-lock-schema | managed_file_updated | aide://update-plan/operation/vendor-file-project-lock-schema | .aide/protocol/aide-project-lock-v0.schema.json | true | true |
| aide://update-receipt/operation-receipt/evidence-only-queue-evidence | evidence_only_preserved | aide://update-plan/operation/evidence-only-queue-evidence | .aide/queue/**/evidence/** | true | true |
| aide://update-receipt/operation-receipt/vendor-file-aide-lite-cli | managed_file_updated | aide://update-plan/operation/vendor-file-aide-lite-cli | .aide/scripts/aide_lite.py | true | true |
| aide://update-receipt/operation-receipt/never-touch-git | never_touch_preserved | aide://update-plan/operation/never-touch-git | .git/** | true | true |
| aide://update-receipt/operation-receipt/vendor-section-agents-summary | managed_section_updated | aide://update-plan/operation/vendor-section-agents-summary | AGENTS.md | true | true |
| aide://update-receipt/operation-receipt/project-owned-readme | project_owned_preserved | aide://update-plan/operation/project-owned-readme | README.md | true | true |
| aide://update-receipt/operation-receipt/local-only-operator-state | local_only_preserved | aide://update-plan/operation/local-only-operator-state | local-only/** | true | true |
| aide://update-receipt/operation-receipt/unknown-unclassified | operation_refused | aide://update-plan/operation/unknown-unclassified | unclassified/** | true | true |
| aide://update-receipt/operation-receipt/migration-recorded | migration_recorded | aide://update-receipt/metadata/migration-recorded | metadata | true | true |
| aide://update-receipt/operation-receipt/lock-updated | lock_updated | aide://update-receipt/metadata/lock-updated | metadata | true | true |
| aide://update-receipt/operation-receipt/ownership-ledger-updated | ownership_ledger_updated | aide://update-receipt/metadata/ownership-ledger-updated | metadata | true | true |
| aide://update-receipt/operation-receipt/install-record-updated | install_record_updated | aide://update-receipt/metadata/install-record-updated | metadata | true | true |
| aide://update-receipt/operation-receipt/validation-run | validation_run | aide://update-receipt/metadata/validation-run | metadata | true | true |
| aide://update-receipt/operation-receipt/rollback-bundle-referenced | rollback_bundle_referenced | aide://update-receipt/metadata/rollback-bundle-referenced | metadata | true | true |
