# Bound the existing Codex worker dispatch to current pause authority

## Objective and boundary

The existing Windows continuous worker starts `codex exec --json` through
`WindowsJobHost`. Its pre-effect pause check can become stale before the host
resumes a suspended child. Keep that child suspended until a current, durable
control check has a serialization point against operator pause/cancellation.
This WorkUnit changes the existing owner only; it does not activate the worker,
add a new launcher, or claim to intercept unmediated Codex/Work requests.

## Scope and dependencies

Use `core/runtime/continuous_worker/{state,coordinator}.py` and the host's
existing `created_suspended`/`resumed` callbacks. Preserve the durable effect
intent and Job containment. `drain` must still let an active task finish;
`pause-dispatch` must stop an unresumed child. Qualify against the installed
host contract and the existing synthetic pipeline tests. Keep the Lite export
gap explicit; it remains in `AIDE-LITE-EFFICIENCY-01`.

## Verification and recovery

1. Add one deterministic pause-epoch check with a SQLite writer lock held only
   between suspended-child observation and resume. Recheck the task cancellation
   and global pause state there. Release the lock on every exception.
2. Run a Windows test that injects pause after child creation but before resume
   and proves child code never executes. Verify ordinary pipeline and host
   behavior, with no real Codex call.
3. Run the affected tests through the configured D job owner, inspect exact
   receipt/retirement and obtain independent exact source review before dev.

If the host fails before resume, retain its effect intent for reconciliation;
do not assume a process started or retry automatically. Existing running jobs
continue under `pause-dispatch`. No native/hosted activation or release claim.

## Progress

- [x] `a8c9935e` serializes the current control epoch with suspended-child resume.
- [x] One source-bound D job passed 31/31 pipeline cases and retired scratch.
- [x] Independent exact source review accepted dev integration; local and remote
  `dev` were observed at the frozen source. Exact bindings are in
  `evidence/source-qualification-2026-09-29.md`.
- [ ] Qualify a real permitted Codex host invocation and exported Lite boundary
  before claiming end-to-end model-call savings or release acceptance.
