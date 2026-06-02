# Remaining Risks

- AIDE-FIX-OS-03 is complete for local validation but remains `needs_review`.
- `AIDE-APPLY-00` is only the proposed next packet in `.aide/context/latest-task-packet.md`; no queue item or implementation was created in this task.
- Transactional apply behavior remains unimplemented and must stay gated by a future reviewed queue item.
- The root harness wrapper still reports the pre-existing `GENERATED-SOURCE-STALE` warning for `.aide/generated/manifest.yaml`; this repair did not change generated manifest source truth.
