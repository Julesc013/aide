# ProjectLock Fixture Matrix

| Case | Expected | Codes |
| --- | --- | --- |
| channel-changed-digest-unchanged | PASS | none |
| extension-round-trip | PASS | none |
| full-valid-lock | PASS | none |
| minimal-valid-lock | PASS | none |
| optional-component-omitted | PASS | none |
| optional-component-selected | PASS | none |
| reordered-deterministic-lock | PASS | none |
| unknown-optional-feature-preserved | PASS | none |
| absolute-path | FAILED_VALIDATION | project_lock.absolute_path_forbidden |
| aide-local-reference | FAILED_VALIDATION | project_lock.source_state_contamination |
| channel-changed-unapproved-digest | FAILED_VALIDATION | project_lock.digest_mismatch, project_lock.channel_digest_drift |
| component-digest-mismatch | FAILED_VALIDATION | project_lock.component_digest_mismatch |
| dependency-cycle | FAILED_VALIDATION | project_lock.dependency_cycle, project_lock.dependency_unsatisfied |
| extension-required-unknown | FAILED_VALIDATION | project_lock.extension_required_unknown |
| manifest-digest-mismatch | FAILED_VALIDATION | project_lock.digest_mismatch |
| manifest-not-accepted | FAILED_VALIDATION | project_lock.manifest_not_accepted |
| manifest-payload-digest-mismatch | FAILED_VALIDATION | project_lock.payload_digest_mismatch |
| missing-required-component | FAILED_VALIDATION | project_lock.required_component_omitted |
| optional-component-ambiguous | FAILED_VALIDATION | project_lock.optional_component_ambiguous |
| secret-like-field | FAILED_VALIDATION | project_lock.secret_or_credential_forbidden |
| source-latest-reference | FAILED_VALIDATION | project_lock.source_state_contamination |
| source-report-reference | FAILED_VALIDATION | project_lock.source_state_contamination |
| target-overlay-invalid | FAILED_VALIDATION | project_lock.target_overlay_invalid |
| traversal-path | FAILED_VALIDATION | project_lock.path_traversal_forbidden |
| unknown-component | FAILED_VALIDATION | project_lock.component_missing |
| unknown-required-feature | FAILED_VALIDATION | project_lock.unknown_required_feature |
| unsatisfied-dependency | FAILED_VALIDATION | project_lock.dependency_unsatisfied |
| unsupported-protocol | FAILED_VALIDATION | project_lock.protocol_incompatible |
