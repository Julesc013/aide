# ExecPlan: Specification Documentation Integration

## Objective

Create a documentation-only integration candidate from current `dev`, validate
the combined result, publish the task branch, and integrate the exact qualified
candidate to `dev` without carrying unfinished runtime work.

## Scope

- Reconcile the completed specification files and their minimum provenance and
  queue dependency closure onto a task branch based on current `dev`.
- Preserve all six adopted contracts and all 34 explicit draft chapters.
- Keep adoption, implementation, verification, activation, and support status
  distinct.
- Produce exact changed-file, validation, exclusion, and ref evidence.
- Integrate only the qualified documentation candidate to `dev`.

## Non-Goals

- No broker, isolated-host, provider, host, store, or target implementation.
- No bulk semantic adoption of the 244 proposed requirements.
- No generated-output cleanup, cache cleanup, worktree pruning, or archive work.
- No root-authority policy amendment, main promotion, tag, or release action.

## Dependencies

- Published source checkpoint `5e3f9240026f6f58825f605f4d1a3d24ca3762c0`.
- Current local and remote `dev` at
  `bfb86c12b9e6d2970024d29c57ba629994ec43cc` when admitted.
- Passed specification foundation, work/effect/identity, and draft-import tasks.
- Owner direction to prepare and integrate the bounded documentation candidate.

## Progress

- [x] Reconcile the parent campaign's stale admission and routing fields.
- [x] Admit this bounded child WorkUnit from the owner's continuation direction.
- [ ] Recheck source and target refs immediately before branch creation.
- [ ] Create an isolated task worktree from current `dev`.
- [ ] Apply only the documented dependency closure from the mixed source branch.
- [ ] Validate content, provenance, links, status language, and exclusions.
- [ ] Commit and publish the exact documentation candidate.
- [ ] Integrate the qualified candidate to `dev` and rerun validation.
- [ ] Record resulting refs, risks, and the separate main-promotion gate.

## Validation

Use exact blob hashes for the adopted contracts, manifest/hash reconstruction for
the imported drafts, relative-link checks, alias and acceptance-design counts,
queue validation, commit checks, changed-path inspection, and post-integration
ref/content checks. Record skipped, stale, failed, timed-out, and unrun checks
without translating them into passes.

## Recovery

The source branch remains untouched and published. Before integration, discard
only this task's isolated worktree and branch if the candidate is invalid. After
integration, recover through a reviewed revert on `dev`; never rewrite shared
history or force-push.
