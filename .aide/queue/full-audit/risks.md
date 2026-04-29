# Full Audit Risk Register

Date: 2026-04-29

## Must Fix Now

No must-fix-now blockers were found for Q04 implementation.

The missing Harness is the reason to run Q04; it is not a blocker to starting Q04.

## Should Fix Before Q05

1. Implement and review Q04 Harness v0.
   - `scripts/aide` is missing.
   - Harness commands are absent.
   - No executable validation or doctoring exists.

2. Resolve or explicitly accept Q00-Q03 review posture.
   - All four remain `needs_review`.
   - The foundation review says pass with notes, but queue status was not changed.

3. Refresh root docs after Q04.
   - `README.md` and `ROADMAP.md` still describe Q04 as next planning/implementation work.
   - After Q04, they should point to Harness v0 honestly.

4. Define generated artifact markers before Q05 implementation.
   - Mark source inputs.
   - Mark generator identity.
   - Mark review/drift policy.
   - Keep generated outputs non-canonical.

5. Add stale generated output checks in Q05.
   - Q05 should rely on Q04 validation before and after generation.

## Acceptable Deferred Risk

1. Full schema validation is deferred.
   - Q03 uses documented shapes.
   - Q04 can start with restricted structural checks.

2. Compatibility baseline is deferred to Q06.
   - Existing `.aide/compat/**` records are placeholders.
   - Bootstrap-era matrices and inventory remain inputs.

3. Dominium Bridge baseline is deferred to Q07.
   - Bridge skeletons exist.
   - XStack remains Dominium-local.

4. Runtime, Service, Commander, Mobile, IDE extensions, providers, apps, packaging, and release automation are deferred.

## Future Strategic Risk

- The repo contains both bootstrap-era implementation and reboot-era skeletons; future agents may confuse conceptual homes with permission to move files.
- Generated agent-facing outputs could become stale if Q05 does not define drift markers and checks tightly.
- A too-large Harness could collapse into Runtime or automation prematurely.
- Compatibility claims could drift without Q06 evidence.
- Human review gates could lag behind prompt-authorized execution unless status cleanup is handled deliberately.
