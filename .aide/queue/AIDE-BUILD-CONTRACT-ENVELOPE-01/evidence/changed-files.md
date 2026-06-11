# Changed Files

Task: `AIDE-BUILD-CONTRACT-ENVELOPE-01`

## Intentional Changes

- `.aide/protocol/aide-envelope.schema.json`: minimal JSON Schema for the public envelope shape.
- `core/protocol/__init__.py`: shared protocol package marker.
- `core/protocol/envelope.py`: minimal envelope builder, validator, lifecycle report projectors, and report writers.
- `.aide/scripts/aide_lite.py`: thin `contract-envelope` CLI dispatch.
- `.aide/scripts/tests/test_aide_contract_envelope.py`: focused envelope, compatibility, projection, and CLI tests.
- `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-01/**`: queue task scaffold and evidence.
- `.aide/reports/contract-envelope/**`: generated status, projection, validation, future-work, and unfinished-work reports.
- `.aide/queue/index.yaml`: task registration.
- `PLANS.md`: plan index entry.
- `IMPLEMENT.md`: execution log entry.

## Restored Generated Churn

The validation run refreshed lifecycle-fixture reports under
`.aide/reports/lifecycle-fixture-runner/**`. Those files are read-only sources
for this task, not deliverables, so they were restored and the
contract-envelope reports were regenerated against the restored source reports.
