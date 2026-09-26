# Independent review: canonical output reservations

Reviewer: Codex child agent `/root/partial_recovery_review`. Date: 2026-09-26.

**Verdict: REQUEST_CHANGES** for exact commit `8acfecc44e61cbc9ac13c9fa9f773c7d5b43906b`, tree `1edfe2562ce980404a9f4439e1fda421d9240d0c`, parent `11226a6e7fd073a599d3f0cb482d6874a6e3d11c`. This is the requested new canonical-output reservation scope only. It does not reopen the prior accepted repair or approve permanent placement, actual packaging, integration, artifact qualification, or release.

## Required change: recovery bypasses final canonical qualification

At `core/execution/managed_workspace.py:486-489`, `run` durably records a quiescent job and its host result before the final canonical output check. An interruption after this checkpoint leaves an `exited/0` result without `canonical_after`. At lines 500-519, `recover` neither reconstructs the declared canonical roots nor checks their identities/usage. It preserves the existing result, collects scratch, releases the reservation, and removes active evidence. A quick overrun can therefore be returned as `exited/0` after recovery, defeating the completion qualification added by this delta.

A tiny frozen-code probe wrote 1,025 bytes into a declared canonical root with a 1,024-byte budget and injected an interruption immediately after the real quiescent checkpoint write, before final canonical inspection. Actual `recover()` then returned:

```text
checkpoint_phase quiescent checkpoint_exit 0 final_canonical_check_recorded False
recovered_phase retired result_reason exited result_exit 0
canonical_actual_bytes 1025 canonical_declared_bytes 1024 canonical_error_recorded False
reservation_released True active_remaining False
owned_fixture_cleaned True
```

Reproducer:

```text
py -3 -B D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/probe-canonical-recovery-8acfecc4.py
```

SHA-256: `ac3e69a5448a7a5babe2b315986f309fdf75864b2ecec222a2136142c3a76bd9`.

The probe loads this exact managed-workspace and WindowsJobHost Git blob into memory. Its host is simulated and source validation is mocked to keep the fixture tiny; the runner checkpoint write and recovery path are real. It launches no build or process workload. This is a deterministic interruption at the reachable persisted boundary, not a claim of an independently killed production controller.

Before recovered output can retain a successful qualification, recovery must rebuild and validate the declared canonical roots/volumes and perform the bounded final usage check. Canonical overrun, disappearance, or identity uncertainty must produce failure/refusal while preserving those source outputs. Add a regression for interruption after quiescent checkpoint but before final canonical inspection; normal completion-only coverage does not exercise it.

## Passing observations and nonblocking notes

- The destination whitelist is narrow and exact: export pack, release, and evaluation runs. `canonical_roots` requires existing ordinary roots/ancestors, declared actual volume identities, positive integer budgets, and a combined local allowance. Missing/unqualified destinations do not get created as fallback.
- Per-volume admission adds the full canonical budgets to scratch, log, collection and control reservations. OS capacity sampling includes declared canonical volumes. The tests explicitly distinguish simulated canonical and pool volumes.
- Admission, thirty-second metadata scans, and normal completion use bounded tree checks. The normal completion catch records canonical overrun/identity failure and preserves canonical outputs. The required change concerns the recovery path around that normal completion check.
- Canonical paths are retained source state. Scratch/collection retirement acts on the existing scratch/retained keys and does not delete the canonical output roots.
- Source packaging guards require the two declared existing canonical destinations; evaluation requires its declared runs root. Generator algorithms and established output locations are unchanged.
- **Nonblocking documentation note:** The later monitoring paragraph/comment still says only owned scratch metadata is scanned, while the preceding new documentation correctly includes declared canonical trees. Align that sentence/comment with the bounded canonical scan behavior.
- **Remaining activation/qualification gates:** Permanent approved pools remain unresolved. Synthetic reservations and this source review do not qualify actual generator bytes or authorize packaging activation.

## Verification and custody

- Exact commit, tree and parent confirmed with `git show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' 8acfecc44e61cbc9ac13c9fa9f773c7d5b43906b`.
- `git diff --check 11226a6e 8acfecc4` passed.
- The bounded reproducer above exited 0 and established the required change. Its single tiny fixture lived under the explicitly approved existing review directory and was cleaned.
- The recorded 22-test Windows PASS (21.894 seconds, no skips) was inspected, not independently repeated. The fast normal overrun test covers uninterrupted completion; it lacks the interrupted-completion recovery case.
- No packaging build, bulk suite, new worktree/clone, broad scan, system-temp fixture, additional agent, source/queue edit, or Git ref mutation occurred. No probe process or fixture remains live. Only the requested report and small external reproducer remain.
