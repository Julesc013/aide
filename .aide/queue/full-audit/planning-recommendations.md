# Planning Recommendations After Full Audit

Date: 2026-04-29

## Immediate Next Task

Run Q04 Harness v0 implementation using `.aide/queue/Q04-harness-v0/prompt.md`.

The prompt should explicitly acknowledge:

- Q00-Q03 are implemented but still `needs_review`.
- The foundation review and full audit support proceeding to Q04.
- Q04 must not generate downstream artifacts.
- Q04 must stop at review.

## Next Three Tasks

1. Q04 implementation.
2. Q04 review and queue status cleanup.
3. Q05 plan-only task for generated artifacts v0.

If Q04 finds contract defects, insert the smallest QFIX before Q05.

## Tasks That Must Not Start Yet

- Q05 implementation.
- Q06 compatibility baseline.
- Q07 Dominium Bridge baseline.
- Q08 self-hosting automation.
- Runtime, broker, scheduler, router, worker, service, Commander, Mobile, IDE extension, provider adapter, app surface, packaging, or release work.

## Suggested Review Gates

Before Q05:

- Review and accept Q04 Harness v0.
- Decide whether Q00-Q03 should be formally moved from `needs_review` to `passed`, or whether the foundation review/full audit are sufficient acceptance records.
- Confirm generated target artifacts are exact and bounded.
- Confirm generated files will carry deterministic markers and source pointers.

During Q04:

- Stop if required Contract/Profile files are missing or contradictory.
- Stop if Harness implementation would need external dependencies.
- Stop if compile behavior starts writing generated target files.
- Stop if Runtime, service, provider, host, or app behavior becomes tempting.

## Suggested Queue Status Cleanup

- Leave Q00-Q03 unchanged during audit-only work.
- After human review, consider a small review/status update that records accepted outcomes for Q00-Q03.
- Let Q04 implementation update only Q04 status and evidence.
- Keep Q05 pending until Q04 review is complete.

## Suggested Human Decisions Before Proceeding

- Is explicit authorization enough to proceed with Q04 while Q00-Q03 still say `needs_review`?
- Should Q04 update `.aide/tasks/catalog.yaml` to say the Q04 packet exists?
- Which generated artifacts should Q05 target first, if any?
- Should Q05 generate agent-facing files only, or remain plan/report-only until drift checks mature?

## Practical Implementation Guidance

Q04 should be boring on purpose: a Python standard-library command wrapper, small diagnostics, restricted text checks, and clear non-mutating reports. That is enough to unlock generated artifact planning without accidentally building the platform early.
