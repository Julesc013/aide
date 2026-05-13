# State Truth Repair

## Stale State Found

- `.aide/profile.yaml` still described QFIX-01/QFIX-02 and Q21 as the current
  focus even after Q24 and the cross-repo readiness checkpoint.
- `scripts/aide self-check` still proposed stale QFIX-02 and Q21 followups.
- `.aide/commands/catalog.yaml` did not describe Q25 checksum scope, safe
  importer mode, or current self-check next-step behavior.

## Files Updated

- `.aide/profile.yaml`: current focus is Q25 repair before Q26 Eureka Pilot
  Review And Handover; future intent records Q22/Q23 target evidence, Q24
  adapter compiler, Q25 active repair, and Q26 next. A later Q26 handover
  refresh updates the next redo to Q27 Commit Discipline And WorkUnit Recovery.
- `core/harness/commands.py`: `_post_token_foundation_step` now recommends
  Q25 review when Q25 is `needs_review` and Q26 when Q25 is passed.
- `core/harness/tests/test_aide_harness.py`: updated assertions so stale
  QFIX-02/Q21 recommendations are rejected.
- `.aide/commands/catalog.yaml`: records Q25 pack-status checksum convention,
  import safe/full mode, exact dry-run reporting, and refreshed self-check
  guidance.
- Root docs and roadmap docs: record Q25 as the repair gate before Q26.

## Current Self-Check Result

`py -3 scripts/aide self-check` returns PASS_WITH_WARNINGS with existing review
gate/generated-manifest warnings and ends with:

```text
next_recommended_step: Q25 review according to .aide/queue/Q25-importer-scope-and-state-truth-repair/status.yaml
```

The stale proposed followups:

- `QFIX-02 AIDE Lite Test Discovery and Runner Fix before Q21 export/import`
- `Cross-repo Q21 export/import only after QFIX-02`

are no longer present.

## Remaining Warnings

- Harness still reports existing review gates and generated manifest source
  fingerprint drift at Q25 time; the later Q26 handover refresh regenerated the
  manifest, leaving only review-gate warnings.
- Q25 remains `needs_review`, so self-check correctly points at Q25 review
  rather than Q26 until review accepts the repair.
- Q27, Q28, and Q29 were recorded as blocked downstream attempts caused by the
  stale Q25 pack/import state. The later Q26 handover refresh supersedes those
  attempts for redo; it does not implement them.

## Next Recommended Queue

After Q25 review accepts this repair, the next queue is Q26 Eureka Pilot Review
And Handover.
