# Rollback Record Matrix

Result: `PASS_WITH_WARNINGS`

| Record ID | Path | State | Phase | Plan Reference | Target Class | Ownership | Operation | Pre/Post | Inverse | Preconditions / Stops | Manual Preservation | Protected Path | Execution Flags | Residual Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `lifecycle-rollback-compatible-record-example` | `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json` | PASS_WITH_NOTES | install | `lifecycle-report-only-plan-example` | fixture | managed-section | update_managed_section | example placeholders | PASS | PASS | PASS | PASS | PASS | generic example only |
| `fixture-rollback-install-managed-section` | `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json` | PASS | install | `fixture-plan-install-managed-section` | fixture | managed-section | update_managed_section | PASS | PASS | PASS | PASS | PASS | PASS | static fixture record only |
| `fixture-rollback-upgrade-v2` | `.aide/examples/apply/lifecycle-fixtures/rollback-records/upgrade-v2.rollback.json` | PASS | upgrade | `fixture-plan-upgrade-v2` | fixture | generated-file | update_managed_section | PASS | PASS | PASS | PASS | PASS | PASS | static fixture record only |

All fixture records are report-backed and review-gated. None authorize rollback apply or rollback execution.
