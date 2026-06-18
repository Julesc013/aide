# Track A Prompt Batch 1

Generate this batch, but execute one task at a time.

## 1. AIDE-ACCEPT-CAPABILITY-MANIFEST-01

Status in this run: executed and stopped at `needs_review` with
`ACCEPTED_WITH_WARNINGS`.

Acceptance target:

```text
minimal_capability_manifest
```

Accepted boundary:

```text
CapabilityManifest declares.
ConformanceProfile defines admission requirements.
ConformanceResult records observed outcomes.
Acceptance evidence admits current repo capability.
```

Do not treat declaration as proof, admission, execution, runtime authority, or
adapter trust.

## 2. AIDE-BUILD-CONFORMANCE-PROFILE-01

Build the minimal ConformanceProfile protocol slice for
`minimal_capability_manifest`.

Required vertical slice:

- schema
- helper
- projection
- CLI status/project/validate
- reports
- focused tests
- queue evidence
- validation
- next-task prompt

Non-goals:

- no ConformanceResult
- no admission decision
- no adapter admission
- no execution
- no PatchTransaction
- no runtime
- no provider/model/network/Gateway/GitHub behavior
- no target apply

## 3. AIDE-CHECK-CONFORMANCE-PROFILE-01

Independently check `AIDE-BUILD-CONFORMANCE-PROFILE-01`.

Check gate requirements:

- source-chain review
- warning disposition
- non-capability boundary
- no-overclaiming review
- no-forbidden-ops review
- next-task prompt

Do not accept ConformanceProfile directly from the build. Route to a later
acceptance task if the check passes or passes with warnings.
