# Consistency Audit

| Source A | Source B | Contradiction | Severity | Recommended Fix | Urgent |
| --- | --- | --- | --- | --- | --- |
| `.aide/profile.yaml` | `.aide/queue/index.yaml` | Profile current focus says Q09 while queue reaches Q20/QCHECK. | high | Update Profile in a reconciliation queue. | yes |
| `.aide/profile.yaml` | Q19/Q20 artifacts | Profile says Gateway/providers deferred; artifacts implement no-call Gateway/provider metadata. | high | Clarify deferred live execution vs implemented metadata. | yes |
| `scripts/aide self-check` | Queue index | Self-check recommends Q09 even after Q20. | high | Update self-check next-step logic. | yes |
| Q18 `task.yaml` | Q18 `status.yaml` and index | Task file says running; status/index say needs_review. | medium | Set task status consistently. | yes |
| `.aide/scripts/aide_lite.py` | generated context packet | current queue lookup ends at Q17. | medium | Discover latest queue dynamically. | soon |
| Q09-Q20 queue states | docs that say implemented | Implemented but not accepted. | high | Review phase outputs explicitly. | yes |
| Q05/Q06 raw statuses | self-check accepted_for_dependency | Raw status remains needs_review despite PASS_WITH_NOTES evidence. | medium | Decide status policy. | soon |
| Generated manifest | Harness validate | Source fingerprint stale. | medium | Reviewed generated-artifact refresh or accepted drift note. | soon |

## Main Consistency Finding

The repo's human docs have advanced faster than its canonical Profile and review
statuses. That is survivable for a checkpoint but unsafe as a long-term
automation foundation.
