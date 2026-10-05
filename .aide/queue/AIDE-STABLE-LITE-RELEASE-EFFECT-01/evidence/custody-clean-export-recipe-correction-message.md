fix(release): correct clean export adapter recipe

## Summary
- Correct the prepared pure-export Python job before dispatch.

## Why
- The pinned adapter expects its script as argv[1] and supplies its own -B.

## Changed
- Remove only the redundant inner-job -B and preserve rejected exact effect.
- Record actual read-only pinned owner inspection and updated preparation hashes.

## Validation
- PASS: pinned owner job inspect exit0 and writes:false with complete retained JSON.
- PASS: whitespace and structured message checks.
- NOT RUN: clean export; rejected native effect was never dispatched.

## Changelog
- Fixed: clean export recipe matches the existing Python adapter contract.

## Risks
- Corrected source and native effect still require exact independent review.
- Prior source67 proof and dirty-export/stable/containment gates are unchanged.

## Follow-up
- Bind corrected job to frozen source and seek one exact export effect verdict.

AIDE-Task: AIDE-STABLE-LITE-RELEASE-EFFECT-01
AIDE-Phase: clean-export-pre-dispatch-recipe-repair
AIDE-Result: PASS_READONLY_INSPECT_EXPORT_UNRUN
AIDE-Scope: exact-prepared-template-proposal-and-rejection-evidence
AIDE-Token-Impact: no-tests-or-worker-replay-owner-inspection-only
AIDE-Quality-Gate: exact-corrected-source-and-native-effect-review-required
