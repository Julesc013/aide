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

## Next no-model host check

Exercise the installed `codex --version` executable through the existing
Windows Job host with a bounded output directory under the configured D job.
Assert suspended-child and resume checkpoints, quiescence and exact CLI output.
This checks real executable launch compatibility without a model request;
it does not discharge the live Codex effect or Lite release gates.

Test-only source `6e21e70f` passed 32/32 pipeline cases under the configured
D runner, including the installed Codex version launch in the existing Job.
The production `core/runtime/continuous_worker` source remains byte-identical
to independently accepted `a8c9935e`. Receipt and limits are in
`evidence/installed-codex-no-model-2026-09-29.md`.

## 2026-09-29 one-turn result boundary

Objective: before the existing worker uses a Codex `exec --json` result, require
one observed thread start, one turn start and one completion in order. Reject
duplicate or conflicting completions, missing starts, and malformed session
identity rather than accepting the last usage or a stale message. Keep normal
single-turn streams and the existing pause/Job owner unchanged. Add focused
parser regressions and update the synthetic pipeline stream, then run affected
state and pipeline tests under the configured D owner. Retain an exact failed
attempt if one occurs. Obtain independent source review before dev integration.
No live model turn, worker activation, Lite export, or release acceptance is
part of this source slice.
