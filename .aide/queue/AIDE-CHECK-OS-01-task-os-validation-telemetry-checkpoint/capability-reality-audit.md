# Capability Reality Audit

## Result

PASS_WITH_WARNINGS.

## Evidence

- `.aide/capabilities/capability-seeds.yaml`: present.
- `.aide/capabilities/capability-observation.schema.json`: present.
- `.aide/capabilities/capability-overclaim.schema.json`: present.
- `.aide/ledgers/capability-ledger.schema.json`: present.
- `.aide/reports/capability-command-status.md`: generated.
- `.aide/reports/capability-observations.json`: generated.
- `.aide/reports/capability-ledger.json`: generated.
- `.aide/reports/capability-overclaims.json`: generated.

## Command Results

- `capability status`: PASS; seed_count 13, command_count 5.
- `capability scan`: PASS; observation_count 47.
- `capability ledger`: PASS; record_count 13.
- `capability overclaim-report`: PASS; overclaim_count 1.
- `capability validate`: PASS.

## Ledger State Counts

- planned: 1
- specified: 3
- stubbed: 1
- implemented: 1
- tested: 1
- exposed: 1
- documented: 2
- deprecated: 1
- removed: 1
- unknown: 1

## Overclaim Result

One non-blocking overclaim record exists: `OVERCLAIM-001`, `capability_reality_ledger`, class `report_only_claimed_as_apply`, severity medium, blocking false. This is a wording review, not a readiness blocker.
