# Q05 Readiness Review

Date: 2026-04-29

## Verdict

Q05-generated-artifacts-v0 is not ready.

The source-of-truth and generated-output policy are clear enough to plan Q05 later, but the executable Harness prerequisite is missing. Q05 should not proceed until Q04 Harness v0 exists and can validate the repo before and after any generated-output change.

## Blocking Fixes

1. Complete Q04 Harness v0 implementation.
   - Add `scripts/aide`.
   - Implement `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff` with the boundaries in the Q04 ExecPlan.
   - Use Python standard library only unless a future reviewed dependency decision says otherwise.

2. Prove Harness behavior.
   - `scripts/aide --help` works.
   - `scripts/aide validate` validates the current repo or fails only with documented actionable errors.
   - `scripts/aide doctor` produces useful diagnostics.
   - `scripts/aide compile` prints a compile plan without creating generated artifacts.
   - `scripts/aide migrate` reports no-op baseline or missing records without changing repo state.
   - `scripts/aide bakeoff` does not call providers, models, native tools, or network services.

3. Review Q04.
   - Write Q04 `changed-files.md`, `validation.md`, `command-smoke.md`, and `remaining-risks.md`.
   - Move Q04 to `needs_review`.
   - Pass or explicitly accept Q04 before Q05.

4. Settle review posture for Q00-Q03.
   - This foundation review finds Q00-Q03 acceptable with notes.
   - The queue status still says `needs_review`, so future queue processing should either update them after review or explicitly cite this foundation review as the acceptance record.

## Recommended Q05 Scope After Unblock

When Q04 is complete and reviewed, Q05 should be limited to generated artifact v0:

- target artifacts: start with explicit agent-facing generated outputs only if named in the Q05 plan; do not generate broad provider or IDE files by default;
- source-of-truth rules: `.aide/` Profile/Contract records remain canonical, generated outputs remain compiled targets;
- generated-file markers: every generated file should include a stable marker naming the source contract, generator, and review policy;
- validation expectations: run `aide validate` before generation, generate deterministically, run `aide validate` after generation, and record drift status;
- no scope creep: do not implement Q06 Compatibility baseline, Q07 Dominium Bridge, Runtime, Hosts, provider calls, release actions, or autonomous worker execution.

## Recommended Next Task

Use a QFIX/Q04 implementation prompt, not a Q05 prompt.
