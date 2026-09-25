# ExecPlan: AIDE-STABLE-LITE-FORCED-RESTART-01

## Objective and scope

Qualify recovery after an abrupt Windows process exit using the exact current
local Lite ZIP and disposable consumers. The source and generated release bytes
are read-only. This task records test scripts, commands, file hashes, observed
target state and an independent technical verdict. It does not authorize main,
tagging or publication.

## Plan

1. Pin `dev@493e3f13`, the ZIP digest and extracted CLI digest. Reuse the
   previously audited archive extractor and create a fresh external run area.
2. In child Python processes loading only the extracted CLI, force `os._exit`
   immediately after selected durable intent, payload, receipt and removal
   effects. Each test must observe the child exit and target bytes, then launch
   a new unmodified CLI process to preview, refuse unsafe replay, or recover.
3. Cover import/update, repair, rollback and removal on fresh or authored
   disposable targets. Assert preserved authored bytes, no unrelated writes,
   exact receipt and intent state, and no silent conflict resolution.
4. Run applicable source regression and canonical checks only if source code
   changes. Obtain independent review of exact run logs and any source repair.
   Record remaining limits, especially synthetic successor and OS network
   tracing, in the parent coverage control.

## Recovery

Never rerun a crashed effect on the same target without observing its pending
intent. Failed runs remain in their external directory. A changed source or
ZIP requires a new identity-bound canary and relevant review.

## Progress

- [x] Admit this bounded qualification task from current `dev` at `5f2441d1`.
- [x] Run four completed-effect forced exits and one first-payload partial
      exit. Preserve exact external logs, target bytes, two corrected oracle
      failures and the partial recovery gap.
- [x] Frozen `f44f3a28` received REQUEST_CHANGES for stale closeout claims;
      corrected exact `e88b1c2e` received focused ACCEPT_WITH_NOTES. Fresh
      preflight, one-writer dev fast-forward and normal push passed. The first
      GitHub API read lagged, then two API routes and Git refs agreed; no
      mutation was replayed. Partial import recovery remains a source task.
