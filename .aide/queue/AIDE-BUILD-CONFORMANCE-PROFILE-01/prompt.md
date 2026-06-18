# Prompt: AIDE-BUILD-CONFORMANCE-PROFILE-01

State update: `minimal_capability_manifest` is admitted as
`ACCEPTED_WITH_WARNINGS` at commit `94b5729`. The next authorized Track A task is
`AIDE-BUILD-CONFORMANCE-PROFILE-01`.

Build the first minimal versioned AIDE `ConformanceProfile` protocol slice.
`ConformanceProfile` defines required, optional, and advisory checks before a
capability can be admitted. A nested `ConformanceCase` defines one profile-scoped
case with a stable `case_id`, evaluator metadata, accepted outcomes, dependencies,
source refs, and evidence requirements.

The candidate profile is for `minimal_capability_manifest`:

- `profile_ref`: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- `profile_id`: `minimal_capability_manifest`
- `profile_version`: `1.0.0`
- `lifecycle`: `candidate`
- `subject.ref`: `aide://capability/minimal_capability_manifest`
- `profile_class`: `protocol`, `capability_admission_requirements`

Required outputs:

- schema
- helper
- projection reports
- CLI
- tests
- queue task
- evidence
- validation
- next-task prompt
- commit

Boundary:

- This task defines profile requirements only.
- It must not implement `ConformanceResult`.
- It must not run conformance cases.
- It must not perform admission.
- It must not trust or promote the capability.
- It must not implement adapters, runtime, PatchTransaction, ContextPack, worker
  execution, provider/model/network/Gateway calls, target apply, branch/worktree
  automation, release, promotion, or production readiness.

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-CONFORMANCE-PROFILE-01` next.
