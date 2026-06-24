# Repair Map

| Finding | Implementation repair | Focused test coverage |
| --- | --- | --- |
| `binding.mismatch_launches_process` | Added pre-launch binding/provider/spec coherence checks in `core/execution/registered_process.py`. | `test_binding_mismatch_fails_closed_before_launch` |
| `receipt.launch_accounting_is_cumulative_or_stale` | Receipts now use current invocation launch metadata and `launcher_call_count: 1` for a valid launch. | `test_reused_provider_receipts_are_per_invocation` |
| `decoder.failure_marked_complete` | Decoder exceptions and undecoded outcomes now make validation/evidence axes `incomplete`. | `test_timeout_and_decoder_outcomes_are_separate_from_process_outcome` |
| `state_probe.failure_not_failed_closed` | State-probe failure now returns `state_probe_failure`, no typed domain result, and incomplete axes. | `test_state_probe_mutation_failure_partial_coverage_and_scrubbing` |
| `cancellation.not_implemented_or_declared` | Added `CANCELLATION_SUPPORTED = False`, `process_cancellation` non-capability, and report evidence. | `test_process_cancellation_is_explicitly_not_supported_in_v0` |
