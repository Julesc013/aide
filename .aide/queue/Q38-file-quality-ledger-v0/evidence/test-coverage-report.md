# Q38 Test Coverage Report

## Generated Report

- Report path: `.aide/reports/test-coverage-map.md`
- Source map: `.aide/repo/test-map.json`
- Command: `py -3 .aide/scripts/aide_lite.py quality tests`

## Findings

- Missing test or validator candidates: 42
- The ledger records likely tests, validators, and evidence refs when Q37
  detected them.
- `.aide/scripts/aide_lite.py` is still a warning-level file because it is a
  large mixed-purpose tool surface, even though Q38 detects likely test refs.

## Interpretation

Missing test or validator candidates mean no obvious direct test, validator, or
golden-task reference was found by deterministic path/name heuristics. They are
not proof that behavior is untested.

## Caveats

- Q38 does not execute coverage tools or infer semantic coverage.
- Generated/evidence/template/archive files are exempt where policy says tests
  are not required.
- Future Q39/Q40 WorkUnits should inspect high-impact source/tool warnings
  before refactor or install work.
