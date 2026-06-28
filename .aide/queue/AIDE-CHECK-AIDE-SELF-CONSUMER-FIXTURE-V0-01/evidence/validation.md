# Validation

Validation outcome: `PASS_WITH_WARNINGS`.

The check ran:

- focused syntax and unittest validation for `.aide/scripts/tests/test_aide_self_consumer_fixture_v0.py`;
- structured JSON review of the fixture manifest, lifecycle scenarios, ownership map, target states, and source-repo refusal case;
- canonical fixture hash comparison before and after DistributionApplyEngine `plan`, `run`, and `verify` operations;
- DistributionApplyEngine `status`, `plan`, `run --mode apply-temp`, and `verify`;
- Q43-Q48 no-apply/no-publish validators;
- broad `aide_lite.py validate`;
- task inspect/evidence checks for the source build task and this check task;
- path, credential-pattern, source-output, and diff hygiene checks.

Material findings: `0`.

Missing evidence after repair of the check packet evidence set: `0`.

Warnings:

- The proof remains fixture-only and does not authorize real target apply.
- DistributionApplyEngine status/plan/verify output still carries stale build-era routing text for the self-consumer fixture; this check records the warning and does not modify implementation.
