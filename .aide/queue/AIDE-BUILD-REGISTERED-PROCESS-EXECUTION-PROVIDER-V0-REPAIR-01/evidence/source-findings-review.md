# Source Findings Review

The independent check reported these material findings:

| Finding | Repair posture |
| --- | --- |
| `binding.mismatch_launches_process` | Repair required before any process launch. |
| `receipt.launch_accounting_is_cumulative_or_stale` | Repair required for per-invocation receipt truth. |
| `decoder.failure_marked_complete` | Repair required for result-axis honesty. |
| `state_probe.failure_not_failed_closed` | Repair required for fail-closed state evidence. |
| `cancellation.not_implemented_or_declared` | Repair required by explicit non-capability declaration. |

The failed-check evidence was not rewritten. This repair creates a separate task
packet, repair report, and evidence set.
