# Repair Closure Matrix

| Source finding | Independent check observation | Result |
| --- | --- | --- |
| `binding.mismatch_launches_process` | Capability and provider binding mismatches produced zero runner calls, zero launcher count, `binding_mismatch`, and incomplete evidence. | closed |
| `receipt.launch_accounting_is_cumulative_or_stale` | A reused provider produced two runner calls across two invocations, but each receipt reported `launcher_call_count: 1` and current launch metadata. | closed |
| `decoder.failure_marked_complete` | Decoder exception produced `decoder_outcome: exception`, `domain_outcome: none`, `validation_outcome: incomplete`, and `evidence_completeness: incomplete`. | closed |
| `state_probe.failure_not_failed_closed` | Probe failure after launch produced `state_probe_failure`, `domain_outcome: none`, and incomplete validation/evidence; probe capture failure before launch produced zero calls and non-complete validation state. | closed |
| `cancellation.not_implemented_or_declared` | `CANCELLATION_SUPPORTED` is false and `process_cancellation` is listed as an explicit non-capability. | closed |

No material findings remain in the independent repair check report.
