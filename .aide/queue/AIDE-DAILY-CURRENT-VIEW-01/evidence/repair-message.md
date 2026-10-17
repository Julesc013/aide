test(tasks): exercise current view through the CLI entry point

## Summary

- Repair the new command fixture and preserve the original failed qualification.

## Why

- Direct handler invocation omitted the CLI's required Path conversion.

## Changed

- Use the actual main entry point without weakening any assertion.
- Conserve 29 original passing methods and prepare the affected final attempt.

## Validation

- PASS: original test and product bytes unchanged, collection and retirement.
- FAIL preserved: first job ran 51 methods with eight setup errors and no skips.
- NOT RUN: repaired 22 methods and three actual CLI smoke calls.

## Changelog

- Fixed: task-local qualification entry-point setup.

## Risks

- This checkpoint is not final source qualification or distribution acceptance.

## Follow-up

- Run the exact reviewed final attempt and independently review its outcome.

AIDE-Task: AIDE-DAILY-CURRENT-VIEW-01
AIDE-Phase: affected-qualification-repair
AIDE-Result: original_failure_preserved
AIDE-Scope: new test fixture and task-local qualification evidence
AIDE-Token-Impact: reuse 29 valid original methods
AIDE-Quality-Gate: exact independent source and final effect review
