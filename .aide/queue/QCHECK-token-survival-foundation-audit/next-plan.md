# Recommended Next Plan

## Immediate Fixes Before Continuing

1. `QFIX-foundation-review-reconciliation`
   - Purpose: review Q09-Q20, reconcile statuses, update Profile current focus,
     fix self-check next recommendation, fix Q18 task/status drift, and record
     accepted limitations.
   - Acceptance: Q09-Q20 have explicit review outcomes or documented deferrals;
     Profile and self-check no longer point at Q09 as current work.
   - Non-goals: no new Gateway/provider/runtime features.

2. `QFIX-aide-lite-test-discovery-and-runner`
   - Purpose: make `.aide/scripts/tests` discoverable or provide a canonical
     runner command, then wire it into evidence guidance.
   - Acceptance: one command runs Harness, Compat, AIDE Lite, Gateway, Provider,
     compile, diff, and secret checks with clear pass/warn/fail output.
   - Non-goals: no behavior rewrite beyond test harness ergonomics.

3. `Q21-existing-tool-adapter-compiler-v0`
   - Purpose: compile metadata for deterministic existing tools after the
     foundation is reviewed.
   - Acceptance: no model/provider calls, tool metadata validates, route/provider
     metadata can reference deterministic tools safely.
   - Non-goals: no provider execution, no Gateway forwarding.

## Next Ten Queue Items

| Order | Queue | Why |
| --- | --- | --- |
| 1 | QFIX foundation review reconciliation | Make the foundation trustworthy. |
| 2 | QFIX AIDE Lite test discovery/runner | Make validation easy and repeatable. |
| 3 | Q21 Existing Tool Adapter Compiler v0 | Turn metadata into useful deterministic tool routing. |
| 4 | Q22 Real Coding Golden Tasks v0 | Prove quality preservation beyond self-consistency. |
| 5 | Q23 External Repo Pilot v0 | Test usefulness outside AIDE. |
| 6 | Q24 AIDE Lite Module Split | Reduce monolith risk. |
| 7 | Q25 Token Quality Scorecard | Tie savings to quality signals. |
| 8 | Q26 Provider Probe Policy v0 | Define safe live-readiness probing. |
| 9 | Q27 Credential Setup Boundary | Prepare `.aide.local/` credential references safely. |
| 10 | Q28 Gateway Provider Dry-Run Harness | Exercise route/provider lifecycle without live calls. |

## Decision Gates

- Do not enable live provider calls until Q09-Q20 are reviewed and Q22 passes.
- Do not implement Gateway forwarding until provider probe and credential
  boundaries pass.
- Do not claim equivalent coding quality until real coding golden tasks pass.
- Do not add UI/Commander/mobile until external-repo usefulness is shown.

## Explicit Non-Goals

- No live provider calls.
- No model calls.
- No outbound network calls.
- No autonomous loops.
- No UI/Commander/mobile.
- No exact billing claim.
- No semantic cache for code edits.
