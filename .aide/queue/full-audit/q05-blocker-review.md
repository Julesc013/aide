# Q05 Blocker Review

Date: 2026-04-29

## Verdict

Q05-generated-artifacts-v0 remains blocked.

The repository has clear source-of-truth rules and generated-output policy, but it does not yet have the executable Harness needed to validate before and after generated-output changes.

## Foundation Review Findings Still Apply

Yes. The foundation review conclusion still applies:

- Q00-Q03 are acceptable with notes but remain `needs_review`.
- Q04 is plan-complete but not implemented.
- Q05 must wait for Q04.

## What Must Happen Before Q05

1. Implement Q04 Harness v0.
   - Add `scripts/aide`.
   - Implement `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.
   - Keep `compile` non-generating in Q04.

2. Prove Q04 behavior.
   - Run command help smoke.
   - Run `aide validate`.
   - Run `aide doctor`.
   - Run `aide compile` and confirm it does not create target artifacts.
   - Run `aide migrate` and `aide bakeoff`.
   - Record evidence.

3. Stop Q04 at review.
   - Update Q04 status to `needs_review` or `blocked`.
   - Review Q04 before Q05 implementation.

4. Settle generated artifact rules in Q05 plan.
   - Define exact target artifacts.
   - Define generated-file markers.
   - Define source contract inputs.
   - Define stale output detection.
   - Define pre/post Harness validation expectations.

## Current Generated Artifact State

- `CLAUDE.md`: absent.
- `.claude/`: absent.
- `docs/reference/generated-artifacts.md`: placeholder/planned.
- `.aide/policies/generated-artifacts.yaml`: policy boundary present.
- Generated downstream artifacts: not implemented.

## Q05 Readiness Decision

Blocked until Q04 implementation and review.
