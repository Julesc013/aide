# Remaining Risks

| Risk | Severity | Mitigation | Next Task |
| --- | --- | --- | --- |
| Future schema revisions may add JSON Schema constructs the local subset validator does not support. | low | Keep `schema_validation_limitations` explicit and extend the subset only when earned by a slice. | AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01 |
| Consumers may overread `v1alpha1` envelope validation as full protocol stability. | low | Reports state the scope is minimal and not a full public protocol stability claim. | AIDE-ACCEPT-CONTRACT-ENVELOPE-01 |
| PyYAML is not installed in this environment for full YAML parsing. | low | A stdlib structural YAML check and `task inspect`/`task evidence` were run; install-free validation remains sufficient for this slice. | AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01 |
