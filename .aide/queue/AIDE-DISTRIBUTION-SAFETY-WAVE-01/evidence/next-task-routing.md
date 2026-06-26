# Next Task Routing

Recommended next task:

```text
AIDE-BUILD-INSTALL-RECORD-V0-01
```

Reason:

`InstallRecord v0` is the first downstream distribution object after accepted DistributionManifest v1, ProjectLock v0, and OwnershipLedger v1. It should record observed or completed install state without performing install apply or target mutation.

The concrete prompt is materialized at `.aide/reports/distribution-safety-wave-01/next-task-prompt/AIDE-BUILD-INSTALL-RECORD-V0-01.md`.
