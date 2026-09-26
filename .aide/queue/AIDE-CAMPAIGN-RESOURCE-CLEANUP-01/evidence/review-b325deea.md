# Scoped independent rereview: canonical crash qualification

Reviewer: Codex child agent `/root/partial_recovery_review`. Date: 2026-09-26.

**Verdict: ACCEPT_WITH_NOTES** for exact commit `b325deeaca742aaed842235d4227e0068a050acf`, tree `549ad8725d956767f7f9559df5a48f6092baf39e`, parent `8acfecc44e61cbc9ac13c9fa9f773c7d5b43906b`. This reviews only the canonical recovery finding and its superseding delta. The prior REQUEST_CHANGES remains unchanged historical evidence. I found no remaining material defect in this repair. This is source acceptance only.

## Repair assessment

The shared `qualify_canonical_outputs` helper now runs on both normal completion and recovery before collection/retirement. Recovery rebuilds the declared canonical roots, checks the currently approved working root and declared volume identities, and applies the bounded usage checks. An interrupted quiescent `exited/0` checkpoint therefore cannot skip canonical qualification.

Canonical overrun or root/identity uncertainty records `canonical_output_limit_or_identity` with no successful exit code. The original process result is retained in `prior_result`. A later successful usage check does not overwrite an already recorded resource failure. Recovery persists its updated record before either finishing a collected retirement or collecting scratch.

The monitor's `canonical_usage` also compares declared volume identities before bounded tree enumeration. The helper changes records and checks paths; canonical output files and aliases remain outside scratch-retirement deletion.

## Decisive bounded verification

I reran the original checkpoint probe with frozen module bodies from this exact commit, keeping the same 1,025-byte canonical output against a 1,024-byte declaration:

```text
checkpoint_phase quiescent checkpoint_exit 0 final_canonical_check_recorded False
prior_process_exit_preserved 0
recovered_phase retired result_reason canonical_output_limit_or_identity result_exit None
canonical_actual_bytes 1025 canonical_declared_bytes 1024 canonical_error_recorded True
reservation_released True active_remaining False
owned_fixture_cleaned True
```

Command:

```text
py -3 -B D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/probe-canonical-recovery-b325deea.py
```

Probe SHA-256: `fcfaf7a163e37fe1c89309338e29c4c5453889f7e58a962e5b5864116a854eaf`.

The probe uses a tiny simulated completed host and mocked source validation; its checkpoint write and actual recovery are real. It loads exact Git blobs into memory and creates only one small fixture under the explicitly approved existing review directory. No packaging workload is launched.

## Notes and limitations

- **Verification boundary:** The recorded ten affected Windows tests (13.276 seconds, no skips), including changed-volume and crash-boundary regressions, were inspected rather than independently repeated. The old 22-test result remains prior-source evidence.
- **Activation gate:** Permanent approved pool placement is still pending. This source verdict does not authorize activation or infer an operator-approved storage map.
- **Qualification gate:** Actual importer/generator execution, final artifact bytes, integration, and release remain separate unfinished campaign gates. Historical checkout-cleanup effects and the prior accepted source runner are outside this scoped rereview.

Exact commit/tree/parent were confirmed with `git show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' b325deeaca742aaed842235d4227e0068a050acf`. `git diff --check 8acfecc4 b325deea` passed.

No tracked file, queue record, Git ref, or prior review original was modified by this reviewer. No new checkout, bulk test, broad scan, system-temp fixture, or additional agent was used. The probe fixture was cleaned and no probe process remains live; only the small external reproducer and requested report remain.
