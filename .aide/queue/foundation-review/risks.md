# Foundation Review Risks

Date: 2026-04-29

## Must Fix Before Q05

1. Q04 Harness v0 is not implemented.
   - `scripts/aide` is missing.
   - `aide validate`, `aide doctor`, `aide compile`, `aide migrate`, and `aide bakeoff` cannot run.
   - Q05 needs pre/post validation and drift checks, so this blocks generated artifacts.

2. Q04 queue state is still `pending` and `planning_complete`.
   - Q04 implementation evidence files do not exist.
   - Q04 has not reached `needs_review`, `passed`, or any accepted review outcome.

3. Q00-Q03 remain `needs_review`.
   - The foundation review finds them acceptable with notes, but their queue status files were not changed by this review-only task.
   - Before Q05, either pass them through review or explicitly document that the foundation review is the acceptance gate.

## Should Fix Soon

1. Root docs are slightly stale around Q04.
   - `README.md` and `ROADMAP.md` still describe Q04 as next planning/implementation work.
   - This is acceptable during review, but Q04 implementation should update root docs honestly.

2. Queue helper scripts and future Harness overlap should stay explicit.
   - Queue helpers are implemented.
   - Harness v0 is not implemented.
   - Future docs should keep this distinction crisp.

3. Q05 scope should define generated markers before emitting any target files.
   - Generated files need clear markers, source pointers, and drift expectations.

## Acceptable Deferred Risk

1. Full YAML/schema validation is deferred.
   - Q03 uses documented shapes, and Q04 can start with restricted structural checks.

2. Q06 compatibility baseline is deferred.
   - Compatibility is visible and policy-bound, but migrations and support reconciliation remain later work.

3. Q07 Dominium Bridge baseline is deferred.
   - Dominium and XStack are documented and skeletonized but not implemented.

4. Runtime, Hosts, Commander, Mobile, IDE extensions, providers, apps, packaging, and release automation remain later.
   - No evidence suggests they leaked into Q00-Q04.
