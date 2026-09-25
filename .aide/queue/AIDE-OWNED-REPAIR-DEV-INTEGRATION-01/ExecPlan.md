# ExecPlan: owned repair dev integration

## Objective and scope

Merge the exact accepted owned repair source with current dev, retaining the
newer removal planner and release generator. This WorkUnit authorizes combined
source and artifact qualification and qualified dev integration. It does not
qualify full lifecycle, native/hosted operation, main, or publication.

## Dependencies and sequence

1. Confirm one integration writer, clean current dev, remote identity, merge
   base, exact reviewed source and evidence-only closeout.
2. Merge both parent histories. Resolve code/tests and queue/root records by
   preserving both workstreams. Keep dev-generated outputs until regeneration.
3. Commit coherent combined source with a prevalidated structured message.
4. Regenerate the portable pack and local release outputs with current
   deterministic tooling; run affected tests, extracted consumer canaries,
   canonical checks, provenance, and post-commit replay.
5. Obtain independent review of the exact combined source and artifacts.
   Repair and rereview material findings. Fast-forward and observe remote dev
   only after review and gate satisfaction.

## Progress

- [x] Read-only merge preflight and remote identity check completed.
- [x] Exact source review accepted `45c5ce91` for dev source integration.
- [ ] Reconcile and test the combined source.
- [ ] Qualify regenerated artifacts and consumers.
- [ ] Obtain independent combined acceptance and integrate dev.

## Recovery

Stop on unrecognized conflicts or changed remote refs. Preserve both worktrees
and the merge state; record test handles and uncertain effects before retrying.
Do not claim accepted source review as combined artifact or release acceptance.
