# Prompt: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01

The next task is:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
```

Build the first minimal, versioned AIDE `ConformanceResult` protocol slice for
the accepted candidate ConformanceProfile:

```text
aide://conformance-profile/minimal_capability_manifest-v1.0.0
```

`ConformanceResult` records observed outcomes against a profile. For this first
slice, observations are projected from accepted evidence only.

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

Semantic boundary:

- `record_valid` is independent from `profile_requirements_satisfied`.
- `profile_requirements_satisfied` is independent from `admission_performed`.
- `admission_performed`, `subject_admitted`, and `trusted` must remain false.
- A valid result may record `FAIL`, `ERROR`, `SKIPPED`, `UNAVAILABLE`,
  `NOT_RUN`, `PASS`, or `PASS_WITH_WARNINGS`.
- The first projected result must use `observation.mode: evidence_projection`.
- The first projected result must use `execution_performed: false`.
- The first projected result must use `runner_ref: null`.

Boundary:

- This task records evidence-projected observations only.
- It must not implement a conformance runner.
- It must not execute cases or commands.
- It must not automatically collect results.
- It must not activate the profile.
- It must not perform admission.
- It must not admit or trust the subject.
- It must not implement adapters, runtime, PatchTransaction, ContextPack,
  worker execution, provider/model/network/Gateway calls, target apply,
  branch/worktree automation, release, promotion, or production readiness.

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01` next.
