chore(git): conserve exported defaults and resume remaining checks

## Summary

- Retain the generated portable pack and prepare the final remaining-stage job.

## Why

- The second attempt completed export but stopped at a stale capability ledger;
  preserving completed effects avoids a redundant rebuild and repeated tests.

## Changed

- Preserve the original failed attempt, corrected Q28 pass and six ownership passes.
- Refresh the existing capability ledger and retain the exact generated pack.
- Add resume mode that reconstructs only the prior fixture and runs unrun stages.

## Validation

- PASS: 36 Git/default methods across preserved first and corrected second runs.
- PASS: six ownership methods, export completion and published-asset conservation.
- FAIL: original doctor result due stale ledger, retained without alteration.
- PASS: full diagnostic validate after explicit ledger refresh.
- NOT RUN: remaining native consumer and changelog qualification awaits checkpoint.

## Changelog

- Changed: development export includes tested current-task view and Git defaults.
- Fixed: stale capability evidence refreshed against actual source inputs.

## Risks

- Development export is not a new published release. Final consumer evidence is pending.
- Final job consumes the third and last admitted allocation; no blind retry or reset.

## Follow-up

- Review actual final outcomes, then synchronize exact accepted dev/main source.

AIDE-Task: AIDE-GIT-DEFAULTS-01
AIDE-Phase: remaining-qualification
AIDE-Result: pending-consumer-qualification
AIDE-Scope: generated-export-evidence-and-resume
AIDE-Token-Impact: unknown
AIDE-Quality-Gate: independent-source-and-effect-review
