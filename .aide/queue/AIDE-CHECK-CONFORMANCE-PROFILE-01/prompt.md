# Prompt: AIDE-CHECK-CONFORMANCE-PROFILE-01

## Attached Prompt Summary

The attached request names the next gate as:

```text
AIDE-CHECK-CONFORMANCE-PROFILE-01
```

Expected outcome if live evidence matches:

```text
PASS_WITH_WARNINGS
next: AIDE-ACCEPT-CONFORMANCE-PROFILE-01
then: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
```

The task is check-only. It must review the completed
`AIDE-BUILD-CONFORMANCE-PROFILE-01` slice without implementation repair, preserve
the declaration/profile/result/admission separation, classify warnings, generate
reports and evidence, run the validation matrix, and stop at `needs_review`.

## Explicit Non-Goals

Do not implement `ConformanceResult`, conformance runner/execution/admission,
adapter admission/execution, `PatchTransaction`, `AdapterManifest`, ContextPack
v2, runtime, Service, Commander, Test Broker runtime, provider/model/network
calls, target apply, branch/worktree automation, release, promotion, or
production readiness.
