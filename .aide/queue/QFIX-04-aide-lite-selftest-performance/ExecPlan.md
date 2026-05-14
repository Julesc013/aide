# QFIX-04 AIDE Lite Selftest Performance Hotfix

## Objective

Make AIDE Lite's frequently used `test` and `selftest` commands materially faster without weakening full golden-task validation or changing provider/model/network boundaries.

## Scope

- Optimize `.aide/scripts/aide_lite.py` selftest behavior.
- Preserve full `eval run` catalog behavior.
- Sync the portable export pack so deployed AIDE Lite receives the same optimization.
- Record evidence under this queue packet.

## Plan

1. Profile the current selftest path.
2. Replace full-catalog golden evaluation inside selftest with a small representative smoke set.
3. Reuse one `run_context()` result for snapshot, index, and context selftest assertions.
4. Avoid repeated path normalization in ignore matching.
5. Regenerate the export pack.
6. Run targeted and broader validation.

## Review Gate

Status ends at `needs_review`. This hotfix does not claim repo-wide optimization is complete.
