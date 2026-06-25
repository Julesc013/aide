# Fixture And Conformance Matrix

| Fixture | Fresh install | Reinstall | Upgrade | Managed section | Unknown ownership | Rollback | Uninstall | Offline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disposable-empty | required | required | not applicable | required | required | required | required | required |
| disposable-existing-manual | required | required | required | required | required | required | required | required |
| disposable-broken-partial | not required | required | required | required | required | required | required | required |
| aide-self-consumer | required | required | required | required | required | required | required | required |
| ScreenSave canary | no direct source mutation | not first gate | required later | required | required | required | not first gate | required |
| Eureka canary | no direct source mutation | not first gate | required later | required | required | required | not first gate | required |
| Dominium canary | no direct source mutation | not first gate | required later | required | required | required | not first gate | required |

Conformance must include:

- schema validation
- semantic validation
- deterministic serialization
- digest test vectors
- negative/refusal fixtures
- path traversal and symlink escape fixtures
- source-generated-state contamination fixtures
- managed-section identity fixtures
- preimage mismatch fixtures
- rollback-bundle absence fixtures
