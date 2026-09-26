# Independent review: managed maintainer workspace

Reviewer: Codex child agent `/root/partial_recovery_review`. Date: 2026-09-26.

**Verdict: REQUEST_CHANGES** for exact commit `5ea1f7cdd53c79a98843a09686ef7bfc7fe9c88e`, tree `fb769c0d029c2b4cbbb7db49922515c64e79dd2f`, parent `36e1a6d54aa088e8d5200d4b8fde4df84b8c6e3b`. Review is limited to the managed-workspace runner, WindowsJobHost delta, job CLI, nonwriting Git queries, tiny tests, and task boundaries. This is source review only, not storage activation, integration, artifact, or release approval.

## Required changes

### 1. Broken scratch aliases falsely retire collected recovery

At `core/execution/managed_workspace.py:301`, `finish_collected` uses `root.exists()` to decide whether scratch remains. A broken Windows junction reports false, so its ordinary-path and original-directory-identity checks are skipped. Line 321 then reports `scratch_absent=True`, releases the reservation, and removes `active.json`, although the unknown reparse entry still exists. The documented promise to preserve and report unknown aliases for reconciliation is not met.

A tiny disposable fixture under the explicitly allowed `D:/Projects/AIDE/_recovery/resource-cleanup-20260926` created a valid collected record and retained output, replaced the original empty scratch directory with a junction to a missing fixture path, and called actual `recover(config_path)`. No test process or output workload was launched.

```text
before_exists False before_lexists True
recovery_phase retired scratch_absent True reservation_released True
after_lexists True active_remaining False
unique_retained True
```

Reproducer: `py -3 -B D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/probe-managed-broken-junction-5ea1f7cd.py`. SHA-256: `5aa9c22e487245161c470e1c7a7ca62f7031f20a1a9ae3b8b9a8bbeeabc672b9`.

Treat only a genuinely absent lexical entry as retired. Any remaining entry, including a broken junction/symlink, must undergo ordinary-path and original identity checks and refuse without retiring recovery evidence. Add a refusal regression asserting that active state and retained output remain intact.

### 2. Actual source maintainer entrypoints can bypass admission

The user requires the actual maintainer test/build/package paths to use resource admission. At this commit, the new CLI is opt-in: `command_test` and `command_selftest` still reach `run_selftest` without a managed-job check (`.aide/scripts/aide_lite.py:44121-44126`); `run_selftest:43732` selects default temporary storage. `command_export_pack:43119` and `command_release_bundle:18462` also call their builders directly without resource admission. An actual Windows-host suite through `job run` verifies the runner, but does not establish that these source campaign entrypoints cannot bypass it.

A bounded mocked handler probe removed `AIDE_JOB_TMP`/`AIDE_JOB_OUTPUT`, stopped before actual work, and observed:

```text
without_managed_context_test_body_called True status 0
without_managed_context_export_builder_called True
without_managed_context_release_builder_called True
```

Reproducer: `py -3 -B D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/probe-managed-entrypoint-bypass-5ea1f7cd.py`. SHA-256: `494540ab47bcdbc8628f1205549c7dfa51bdd900f0b3760ff8529f654ddbd51d`. This imports and mocks the handlers only; no selftest, export or release build runs.

Packaging placement also needs an explicit boundary: `build_export_pack:40227-40235` only permits the canonical source-repository export path, and `build_release_bundle_outputs:18346-18355` writes archives and other outputs into repository release paths. Those bytes are outside managed scratch and `AIDE_JOB_OUTPUT`; a source checkout on a different volume is not covered by the runner's storage-root disk sampling. Wrapping the unchanged packaging command alone does not qualify its output placement.

A minimal source-maintainer guard is necessary before acceptance: refuse these heavy source CLI entrypoints outside the supported managed context while preserving deliberate portable Lite compatibility. Packaging may stay explicitly refused/paused until its actual output placement is qualified. No general scheduler or product-wide migration is needed for this repair. Update the source test-runner instructions to match the enforced source behavior.

## Passing observations and nonblocking notes

- **Admission:** Existing, absolute, ordinary, nonoverlapping roots and declared volume identities are checked before allocation. The configured shared control root uses an OS lock; disk and memory reservation arithmetic accounts for shared volumes. Missing pools/configuration have no root-creation fallback.
- **Limits:** Positive finite limits are required; process count and runtime have additional caps. Windows Job memory/process enforcement and bounded pipe drains are separate from the honestly documented sampled disk thresholds. No hostile filesystem or global quota claim is made.
- **Process ownership:** The WindowsJobHost delta preserves atomic Job assignment and protected-execution environment restrictions. Monitoring records PID plus creation time; reconciliation acts on the named owned Job, not a reusable PID.
- **Retention:** Quiescent output and logs are collected before owned scratch retirement. Collected content digests, original scratch identity, and remaining-output comparison support interrupted retirement. Unknown members/links and conflicting partial collection refuse rather than delete output; finding 1 concerns the skipped broken-root classification.
- **Source identity:** Declared input file hashes, executable hash, HEAD commit/tree, script binding and approved cwd are checked. This establishes the explicitly declared inputs; it does not automatically enumerate undeclared module dependencies or establish a clean entire working tree.
- **Git compatibility:** Default `git detect` and `git plan` select the nonwriting collection path. Explicit `--write-reports` retains their report projections.
- **Activation condition, not a code defect:** Permanent approved pool placement remains unresolved. All campaign checkouts must share one control root; another configured control root is not globally coordinated. The task correctly keeps heavy work paused and does not infer activation, integration, or release approval.
- All changed paths fit the queue's declared allowed paths. Historical cleanup effect evidence was read as task context, not independently reexecuted or requalified in this runner review.

## Verification and resource discipline

- Exact commit, parent and tree confirmed with `git show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' 5ea1f7cdd53c79a98843a09686ef7bfc7fe9c88e`.
- `git diff --check 36e1a6d54aa088e8d5200d4b8fde4df84b8c6e3b 5ea1f7cdd53c79a98843a09686ef7bfc7fe9c88e` passed.
- The two bounded probes above exited 0 and established the required changes. The junction fixture and exact created link were cleaned; no system-temp fixture, new worktree, bulk suite, broad scan, or extra agent was used.
- The recorded 12 tiny tests (20.072 seconds) were inspected, not rerun. The earlier actual-host 10-test PASS predates final collection refinements; the lead's current replay is separate evidence and is not claimed by this report.
- `git status --short --branch` stayed clean. No source, queue, Git ref, or existing review original was modified. No probe process remains live. Only the requested report and small external reproducer scripts remain.
