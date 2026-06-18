# AIDE-BUILD-CONFORMANCE-PROFILE-01
# Build Minimal ConformanceProfile

Create and process `AIDE-BUILD-CONFORMANCE-PROFILE-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Goal:
Implement the first minimal ConformanceProfile protocol slice for AIDE.

ConformanceProfile defines the checks required before a declared capability can
be considered for admission. It does not record observed outcomes and does not
admit a capability by itself.

Core distinction:

- CapabilityManifest = declared capability
- ConformanceProfile = tests/checks required for admission
- ConformanceResult = observed result
- Acceptance task/evidence = current repo admission record

Build only:

- ConformanceProfile schema
- helper/projection/validation
- conformance profile reports
- thin CLI dispatch if consistent with repo style
- focused tests
- queue evidence
- next-task prompt

Use accepted CapabilityManifest reports and evidence where practical.

Initial profile target:

```text
minimal_capability_manifest
```

Required profile semantics:

- profile identity and version
- capability target refs
- required cases
- optional cases
- fail-closed behavior for missing required cases
- accepted evidence requirements
- source/report/evidence refs
- explicit non-capabilities

Non-goals:

- no ConformanceResult
- no admission decision
- no adapter admission
- no adapter execution
- no capability execution
- no runtime
- no scheduler
- no leases
- no supervisor
- no Service
- no Commander
- no PatchTransaction
- no AdapterManifest
- no ContextPack v2
- no Test Broker runtime
- no worker execution
- no provider/model calls
- no network
- no Gateway/GitHub mutation
- no branch/worktree automation
- no target apply
- no active apply
- no release
- no production readiness
- no broad autonomous runtime behavior

Expected commands:

- `py -3 .aide/scripts/aide_lite.py conformance-profile status`
- `py -3 .aide/scripts/aide_lite.py conformance-profile project`
- `py -3 .aide/scripts/aide_lite.py conformance-profile validate`

Stop at `needs_review` with evidence.

Recommended next task:

```text
AIDE-CHECK-CONFORMANCE-PROFILE-01
```
