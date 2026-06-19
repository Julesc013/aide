# AIDE-CHECK-ADAPTER-MANIFEST-01 Prompt Record

The operator prompt requested an independent check of the minimal provider-
neutral AdapterManifest protocol slice.

The prompt's execution-order gate required:

```text
- AIDE-BUILD-ADAPTER-MANIFEST-01 exists;
- the build task is complete at needs_review;
- its result is PASS or PASS_WITH_WARNINGS;
- its task evidence reports missing_evidence: 0;
- the build commit exists at live HEAD or is an ancestor of live HEAD;
- AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01 remains accepted;
- no AdapterManifest repair or superseding task has replaced the build;
- the build recommends this independent check as its next task.
```

The prompt also required:

```text
If the build is absent, incomplete, contradictory, failed, or superseded, stop
as BLOCKED and report the exact live discrepancy.

Do not implement or repair AdapterManifest from this check prompt.
```

Live queue truth does not satisfy the build-result or PatchTransaction
acceptance prerequisites. Therefore this task records a blocked check packet and
does not execute AdapterManifest review.
