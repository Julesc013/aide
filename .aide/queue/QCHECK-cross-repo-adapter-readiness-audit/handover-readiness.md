# Handover Readiness

## Verdict

Readiness: conditional.

AIDE is ready for a controlled Eureka handover review using the already-imported
Eureka AIDE Lite state. It is not ready for broad direct-import instructions or
new pack handoff without a short repair of importer scope, pack checksum
integrity, pack provenance, and source-of-truth guidance.

## What To Hand Over

- The portable AIDE Lite Pack concept and current pack path.
- Eureka's already-imported `.aide/**` state.
- Eureka-specific memory under `.aide/memory/**`.
- Eureka's `.aide/context/latest-task-packet.md`.
- Eureka's `.aide/context/latest-review-packet.md`.
- Eureka pilot evidence under `.aide/queue/EUREKA-AIDE-PILOT-01/**`.
- The rule that target repos generate their own snapshot/index/pack/evidence.

## What Not To Hand Over

- AIDE source `.aide/queue/**` history.
- AIDE source `.aide/memory/**`.
- AIDE generated context/reports/cache/route/controller/latest status.
- `.aide.local/`.
- `.env` or provider credentials.
- Raw prompt or raw response logs.
- Generated adapter previews as canonical truth.
- Gateway/provider runtime behavior.

## Recommended Eureka Operator Flow

Inside `julesc013/eureka` after reviewing `EUREKA-AIDE-PILOT-01`:

```text
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py pack --task "Select and scope the next bounded Eureka implementation task from current repo state"
py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md
```

Then hand Codex the compact task packet, not long chat history.

## First Real Eureka Task

Review the import pilot and choose one bounded Eureka implementation task. The
task should:

- cite `.aide/context/latest-task-packet.md`;
- include target-specific allowed/forbidden paths;
- run Eureka product validation where appropriate;
- write target-local evidence;
- preserve no-provider/no-secret boundaries;
- stop at review.

## Handover Blockers

Hard blockers:

- none for reviewing existing Eureka import evidence.

Conditional blockers before broad pack handoff:

- stale `.aide/profile.yaml` current focus;
- stale Harness `self-check` next-step guidance;
- Q21 importer direct apply is too broad for target-pilot scopes;
- export pack checksum validation fails on `manifest.yaml`;
- export pack manifest provenance is dirty/stale relative to current HEAD;
- Q21 evidence count drift versus current pack count.

## Evidence Required During Handover

- Current Eureka git state and commit.
- `.aide.local/` ignore check.
- AIDE Lite doctor/validate/test or documented target limitation.
- Token estimate for latest task packet.
- Secret scan over `.aide` and guidance surfaces.
- Evidence that product source changes, if any, are in the next bounded task,
  not in the import pilot.
