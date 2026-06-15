# TestJob Warning Disposition

All warnings are accepted as non-blocking within the narrow `minimal_test_job_schema` scope.

- Full JSON Schema Draft 2020-12 validation remains deferred. Mitigation: future schema validator or conformance hardening task.
- TestJob remains metadata-only by design. Mitigation: preserve explicit non-capabilities until runtime tasks are separately authorized.
- Test Broker runtime and async execution are absent. Mitigation: unsupported execution subcommands continue to fail closed.
- `.aide/context/latest-task-packet.md` is stale. Mitigation: use live queue truth.
- Prior check scan invocations were corrected. Mitigation: use corrected command forms.
- Generated report churn must be contained. Mitigation: restore or include only deliberate report outputs.
- ReferenceID is next before PatchTransaction. Mitigation: recommend `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.
