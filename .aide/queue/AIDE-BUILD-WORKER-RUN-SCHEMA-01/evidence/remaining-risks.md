# Remaining Risks

- Full JSON Schema Draft 2020-12 validation is not implemented; current validation uses the established minimal local subset.
- WorkerRun is metadata-only; no live worker execution semantics have been tested because they are out of scope.
- Queue index CRLF normalization warning remains non-blocking and pre-existing in behavior.
- Generated predecessor reports can churn during broad validation commands; unrelated churn was restored in this task.
