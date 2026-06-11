# Changed Files

| Path | Kind | Reason | Source |
| --- | --- | --- | --- |
| `core/protocol/envelope.py` | code | Adds schema loading, minimal schema subset validation, runtime validation aggregation, schema/helper alignment checks, and report fields. | authored |
| `.aide/scripts/aide_lite.py` | code | Adds stdout lines for schema validation status while keeping logic in the protocol helper. | authored |
| `.aide/scripts/tests/test_aide_contract_envelope.py` | test | Adds focused tests for schema parsing, subset validation, helper/schema agreement, fail-closed capability behavior, and validation report fields. | authored |
| `.aide/reports/contract-envelope/status.md` | report | Generated status report with schema path and mode. | generated |
| `.aide/reports/contract-envelope/validation.json` | report | Generated validation report with schema runtime alignment fields. | generated |
| `.aide/reports/contract-envelope/validation.md` | report | Generated human-readable validation report with schema runtime alignment fields. | generated |
| `.aide/reports/contract-envelope/future-work.md` | report | Generated future-work report updated for the hardening check path. | generated |
| `.aide/reports/contract-envelope-harden/**` | report | Hardening-specific report, future-work, and unfinished-work outputs. | authored |
| `.aide/queue/AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01/**` | task/evidence | Queue packet and evidence for this hardening task. | authored |
| `.aide/queue/index.yaml` | queue | Adds the hardening task to the filesystem queue index. | authored |
| `PLANS.md` | doc | Adds the plan entry for this substantial queued task. | authored |
| `IMPLEMENT.md` | doc | Records the hardening implementation and validation outcome. | authored |
