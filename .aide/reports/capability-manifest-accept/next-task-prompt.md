# AIDE-BUILD-CONFORMANCE-PROFILE-01

Build the minimal ConformanceProfile protocol slice for
`minimal_capability_manifest`.

ConformanceProfile defines required checks before capability admission. It does
not record observed outcomes and does not admit capabilities by itself.

Required slice:

- schema
- helper
- projection
- CLI status/project/validate
- reports
- focused tests
- queue evidence
- validation
- next-task prompt

Use accepted CapabilityManifest reports and evidence where practical.

Non-goals:

- no ConformanceResult
- no admission decision
- no adapter admission
- no adapter execution
- no capability execution
- no PatchTransaction
- no runtime
- no provider/model/network/Gateway/GitHub behavior
- no branch/worktree automation
- no target apply
- no active apply
- no release or production readiness

Recommended next task:

```text
AIDE-CHECK-CONFORMANCE-PROFILE-01
```
