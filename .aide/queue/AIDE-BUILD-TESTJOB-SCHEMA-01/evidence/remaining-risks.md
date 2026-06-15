# Remaining Risks

- Low: full JSON Schema Draft 2020-12 validation remains deferred.
  - Mitigation: future conformance or schema-validator hardening task.
- Low: TestJob is metadata-only and does not prove async execution or broker semantics.
  - Mitigation: do not build Test Broker runtime until TestJob is checked and accepted.
- Low: `.aide/context/latest-task-packet.md` remains stale relative to `.aide/queue/index.yaml`.
  - Mitigation: repair only in a separate authorized hygiene task.
- Low: helper validation commands can refresh generated predecessor reports.
  - Mitigation: restore out-of-scope generated churn unless it is an intentional deliverable.
