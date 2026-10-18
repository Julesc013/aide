### Independent cooperative request cancellation

**Objective.** A sender can request cancellation of one exact dependency revision;
the registered recipient records its native outcome. The same ledger continues
unrelated requests. Every original delivery/acceptance/result record survives.
This closes a useful P4.requests gap in the existing CLI/MCP lifecycle without
adding a scheduler, messaging store, server or process-control authority.

**Starting evidence.** Accepted dev/main is 8fe2d12c. The qualified Lite 1.1.0
publication packet at f708e8c6 is preserved locally and remotely, awaiting
interactive authentication. Its source, branch and frozen assets remain untouched.
Developing independently may change dev/main; the later publication effect must
reconcile its exact ref guards before executing, not silently reuse stale guards.

**Design and compatibility.**
- Extend Requests and its existing dependency_observe tool. Retain linear normal
  stages. Add cancellation_requested and cancellation_acknowledged as explicit
  observations, not automatic process termination or completion.
- Require an explicitly initialized v2 configuration with known required
  cancellation semantics. Existing v1 configurations keep existing behavior and
  refuse cancellation. Old implementations must refuse the v2 configuration;
  no silent upgrade or migration of a live ledger.
- Sender cancellation binds request digest, expected observed stage, reason and
  evidence. Permit before adoption only; transactionally refuse stale stage,
  wrong actor/binding, changed revision, expired config or paused controls.
- Recipient acknowledgement binds the exact cancellation observation and evidence,
  with an explicit native disposition: not_started, stopped, already_completed
  or uncertain. This is an attributed observation, not independent proof.
- Identical retries reuse their observation; conflicts refuse. Normal advancement
  after cancellation cannot quietly continue. Preserve earlier return claims,
  all obligations, native-work links and uncertainty. Acknowledgement never marks
  successful adoption or releases a workspace/process owner.
- Status/inbox identify next responsible owner and action. Unknown effects require
  reconciliation. Other request rows and native task/attempt/control tables stay
  unchanged. Shared services and host processes are never touched.

**Scope.** Exact allowlist is in task.yaml. Product work is two existing runtime
modules, one new focused test file and their existing reference. No new execution
binding or actual desktop dispatch claim. Source-runtime features remain outside
the frozen Lite release contract. Generated views/export change only if their
existing owners require it; preserve qualified content and classifications.

**Sequence.**
1. Independent admission; under fresh shared controls preserve the current
   publication branch and switch directly to one new local task branch from
   accepted dev. Checkpoint exact admission metadata.
2. Prepare bounded source, original-assertion-preserving tests and reference.
   Obtain exact source/first-job review before native tests.
3. At most three sequential managed jobs under unchanged 180-second default
   limits. First: existing request/MCP/state suites plus focused cancellation,
   unknown-version/refusal/duplicate/concurrency/restart tests. Second: actual
   fresh-process CLI and MCP two-request scenario, plus applicable existing
   exporter/ownership/pack checks if needed. Third: fixed promotion preview.
   Each failure consumes a slot; reconcile before any reviewed retry.
4. Retain exact command outcomes and evidence that cancellation leaves another
   request independently completable, with no native/control effects. Verify
   original v1 cases unchanged. Source/delivered/operational claims remain scoped.
5. Independent terminal acceptance precedes safe task/dev/main sync and remote
   readback. Retire only this local branch after verified integration. Preserve
   the pending release branch and every frozen release byte.

**Acceptance.** The useful scenario has two requests, independent sender/receiver
CLI/MCP sessions, a revision-bound cancel/ack for one and ordinary return/adoption
for the other across fresh processes. Include uncertain disposition, stale owner,
stale revision, wrong actor, duplicate conflict, paused/expired state and legacy
configuration refusal. Exercise old reader rejection of new required semantics
without altering the old implementation. No test may turn cancellation into
native quiescence, permission or evidence of completed publication.

**Recovery.** All ledgers used in qualification are owned disposable job fixtures;
no live initialization/migration or peer contact. Code handles finite process
collection. Preserve failures, validate collections and retire only owned scratch.
No blind retry, broader resources, new model calls or repeated unchanged host
probes. The broader daily-use host, downstream adoption, efficiency and release
obligations remain open.

**Prepared source.** Explicit v2 configuration, two attributed cancellation
observations, unchanged normal stage and v1 behavior. Status/inbox expose the
next responsible owner. Thirteen focused methods plus the original 60 methods
are prepared for job 1; one actual fresh-process two-request scenario and legacy
reader refusal remain job 2. No native test has run at this checkpoint.

**Job 1 passed.** Source55b5aabb: all73 methods passed without skips.
Worker683ea8c5cdd6494fa575cec354f2731b was collected, digest-verified and
retired with scratch absent and reservation released. Original60 methods are
unchanged. The separate fresh-process workflow and frozen old-reader checks are
prepared for job2; no live coordination or native cancellation claim is made.
