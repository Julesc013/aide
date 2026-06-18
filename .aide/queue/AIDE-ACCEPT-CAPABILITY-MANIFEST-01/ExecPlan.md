# AIDE-ACCEPT-CAPABILITY-MANIFEST-01 ExecPlan

## Objective

Perform a check-only acceptance review for the minimal declaration-only
CapabilityManifest chain and decide whether `minimal_capability_manifest` is
accepted with warnings.

## Scope

This task may write only its own queue packet and evidence, aggregate
acceptance reports under `.aide/reports/capability-manifest-accept/`, the queue
index entry, and root planning/execution log entries required by repository
law.

The task may not mutate CapabilityManifest implementation files, predecessor
reports, OKF pages, generated latest task packets, runtime surfaces,
provider/Gateway/network/GitHub surfaces, branch/worktree automation, target
apply, release, or ConformanceProfile implementation files.

## Source Chain

```text
AIDE-CHECK-TRACK-B-B1-BARRIER-01
-> AIDE-BUILD-CAPABILITY-MANIFEST-01
-> AIDE-CHECK-CAPABILITY-MANIFEST-01
-> AIDE-ACCEPT-CAPABILITY-MANIFEST-01
```

## Plan

1. Verify live `.aide/queue/index.yaml` and source-chain records.
2. Review CapabilityManifest build/check reports, evidence, CLI behavior,
   status semantics, capability inventory, and conformance placeholders.
3. Classify known warnings as blocking or non-blocking.
4. Publish acceptance evidence, acceptance reports, and the first Track A prompt
   batch without executing the ConformanceProfile tasks.
5. Stop at `needs_review` and recommend
   `AIDE-BUILD-CONFORMANCE-PROFILE-01` if accepted.

## Verification Intent

Run JSON parsing for acceptance and predecessor reports, focused
CapabilityManifest tests, CapabilityManifest CLI status/project/validate,
task inspect/evidence for build/check/accept tasks, predecessor validators,
broad validation, Git diff checks, and commit policy validation after commit.

## Exit Criteria

- `minimal_capability_manifest` is accepted with warnings only if build/check
  evidence remains complete and declaration-only.
- All known warnings are classified as non-blocking or deferred.
- Explicit non-capabilities are preserved.
- CapabilityManifest remains declaration-only and does not prove conformance,
  admit adapters, execute capabilities, or authorize runtime behavior.
- The prompt batch records only:
  `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`,
  `AIDE-BUILD-CONFORMANCE-PROFILE-01`, and
  `AIDE-CHECK-CONFORMANCE-PROFILE-01`.
- The next task prompt routes to `AIDE-BUILD-CONFORMANCE-PROFILE-01`.

## Current Status

Completed and awaiting review.
