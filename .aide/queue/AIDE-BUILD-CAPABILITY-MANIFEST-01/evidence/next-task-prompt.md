# AIDE-CHECK-CAPABILITY-MANIFEST-01
# Independent Check For Minimal AIDE CapabilityManifest

Create and process AIDE-CHECK-CAPABILITY-MANIFEST-01.

Use .aide/queue/index.yaml as canonical queue truth.

Independently review AIDE-BUILD-CAPABILITY-MANIFEST-01.

Scope:

- Check only.
- No implementation except minimal evidence/report generation if queue policy requires it.
- No ConformanceProfile.
- No ConformanceResult.
- No adapter admission.
- No adapter execution.
- No runtime.
- No scheduler.
- No leases.
- No supervisor.
- No Service.
- No Commander.
- No PatchTransaction.
- No AdapterManifest.
- No ContextPack v2.
- No Test Broker runtime.
- No worker execution.
- No provider/model calls.
- No network.
- No Gateway/GitHub mutation.
- No branch/worktree automation.
- No target apply.
- No active apply.
- No release.
- No production readiness.
- No broad autonomous runtime behavior.

Verify:

- CapabilityManifest schema exists and follows the AIDE envelope pattern.
- CapabilityManifest helper exists and is deterministic.
- capability-manifest status/project/validate commands work.
- Capability reports parse.
- Required initial capabilities are projected.
- Accepted capabilities have evidence/source/report refs.
- accepted_with_warnings is preserved.
- metadata_only/report_only/projection_only/runtime/mutating flags are truthful.
- explicit_non_capabilities are present.
- ConformanceProfile placeholders do not imply admission.
- Future/deferred layers are not marked accepted.
- Reconciler/OKF/ReferenceID/EventRecord integrations are truthful.
- Existing protocol, OKF, and Reconciler validators remain compatible.
- Focused tests pass.
- Validation evidence exists.
- No secrets are emitted.
- No forbidden operations were introduced.

Expected result:

PASS, PASS_WITH_WARNINGS, FAILED_VALIDATION, BLOCKED, or PARTIAL.

Recommended next task if PASS or PASS_WITH_WARNINGS:

```text
AIDE-ACCEPT-CAPABILITY-MANIFEST-01
```

Recommended next task after acceptance:

```text
AIDE-BUILD-CONFORMANCE-PROFILE-01
```
