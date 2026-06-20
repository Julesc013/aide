# Parallel Read-Only RepoGraph Lane

Planned but not implemented:

```text
AIDE-PLAN-REPOGRAPH-TRACK-B2-01
AIDE-BUILD-REPOSITORY-FACT-MODEL-01
AIDE-CHECK-REPOSITORY-FACT-MODEL-01
AIDE-ACCEPT-REPOSITORY-FACT-MODEL-01
AIDE-BUILD-EXISTING-FACT-IMPORT-01
AIDE-BUILD-REPOGRAPH-SNAPSHOT-V0-01
AIDE-BUILD-REPOGRAPH-IMPACT-01
AIDE-BUILD-REPOGRAPH-CONTEXTPACK-INTEGRATION-01
AIDE-BUILD-REPOGRAPH-OKF-PROJECTION-01
AIDE-BUILD-REPOGRAPH-RECONCILER-INTEGRATION-01
```

Every RepositoryFact must eventually carry producer, source revision, source digest, authority class, confidence, completeness, freshness, and evidence refs.

This lane is read-only and must not block the read-only Dominium seam.
