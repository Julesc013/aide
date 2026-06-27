# Independent RollbackBundle v0 Probes

Additional check-local fail-closed probes all returned `FAILED_VALIDATION` with expected refusal codes:

| Probe | Expected Code | Result |
| --- | --- | --- |
| missing target project ref | `rollback_bundle.target_project_missing` | PASS |
| missing candidate project lock ref | `rollback_bundle.candidate_project_lock_missing` | PASS |
| missing install record refs | `rollback_bundle.install_record_missing` | PASS |
| candidate distribution mismatch | `rollback_bundle.candidate_distribution_mismatch` | PASS |
| source distribution mismatch | `rollback_bundle.source_distribution_mismatch` | PASS |
| reverse project overlay mutation | `rollback_bundle.project_overlay_reverse_mutation` | PASS |
| reverse runtime generated mutation | `rollback_bundle.runtime_generated_reverse_mutation` | PASS |
| reverse evidence only mutation | `rollback_bundle.evidence_only_reverse_mutation` | PASS |
| install apply authority claim | `rollback_bundle.apply_authority_claimed` | PASS |
| update apply authority claim | `rollback_bundle.apply_authority_claimed` | PASS |
| uninstall apply authority claim | `rollback_bundle.apply_authority_claimed` | PASS |

Required schema/projection field probes passed for metadata and spec fields.
