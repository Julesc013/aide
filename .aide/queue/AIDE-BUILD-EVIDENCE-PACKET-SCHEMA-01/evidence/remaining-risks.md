# Remaining Risks

| Risk | Severity | Mitigation | Next Task |
| --- | --- | --- | --- |
| EvidencePacket is minimal and v1alpha1, not a full public protocol stability claim. | low | Keep report wording bounded and review independently. | AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01 |
| Schema validation is a minimal local subset, not full JSON Schema Draft 2020-12. | low | Keep limitation explicit until a future reviewed task introduces a full validator. | AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01 |
| Projection logic covers accepted lifecycle and contract-envelope artifacts only. | low | Add new projection sources only after new slices earn them. | future hardening task if needed |
| EvidenceStore and evidence engine behavior remain absent. | low | Do not route runtime trust decisions through this helper until accepted and extended. | future evidence engine task |
