# Operation Auditability Review

| Assertion | Outcome | Severity | Source Finding |
| --- | --- | --- | --- |
| `operation.guard_report_not_static` | FAIL | MATERIAL | `operation.guard_report_is_not_static` |
| `operation.lossless_aggregate_dimensions` | PASS | MATERIAL | `operation.aggregate_key_preserves_semantics` |
| `operation.raw_trace_reconciles` | PASS | WARNING | `None` |
