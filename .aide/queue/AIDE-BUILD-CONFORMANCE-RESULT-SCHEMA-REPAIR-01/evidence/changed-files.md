# Changed Files

Implementation:

- `core/protocol/conformance_result.py`: added `sha256-canonical-json-v1`, pristine profile loading, and pristine-source validation.
- `.aide/scripts/tests/test_aide_conformance_result.py`: added independent digest, mutation, determinism, and payload-change regression tests.

Generated ConformanceResult outputs:

- `.aide/reports/conformance-result/**`: regenerated affected digest and next-gate fields.

Repair task and reports:

- `.aide/queue/AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01/**`
- `.aide/reports/conformance-result-repair/**`

Queue and logs:

- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
