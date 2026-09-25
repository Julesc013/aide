# ExecPlan: AIDE-STABLE-LITE-TASK-TRUTH-01

## Objective, scope and dependencies

Repair only the installed Lite Task OS report-truth defect. The clean source
base is `dev@d292253b09944f28f0fc794fe3a9679966fe56a0`, tree
`51b60b58d75ae5e72bffda40300b2baca9436a91`. The independently reviewed
consumer finding is in
`.aide/queue/AIDE-STABLE-LITE-CONSUMER-PREQUAL-01/evidence/installed-task-status-finding.md`.
The current local preview archive is read-only here. No generated release
artifact or Git integration effect belongs to this source task.

## Plan and acceptance

1. Add a focused regression using a new target queue with zero items and a
   generic generated packet whose contextual guidance mentions `Q17`.
   Assert no latest task identity and no source-specific X-OS next WorkUnit.
   Keep existing source-repository explicit-ID and leading-PHASE fixtures.
2. Run the red test against unmodified source. Change only the parser,
   empty-queue selection and user-facing empty-state wording needed to make
   the result truthful. Preserve `task status` exit 1 for zero queue items.
3. Run focused Task OS tests, affected golden/canonical checks, source lint or
   syntax validation, and review adversarial packet cases. Record the exact
   commands, source commit/tree, outcomes, warnings and any generated drift.
4. Freeze one source candidate, obtain an independent technical verdict on
   this exact behavior and its target/source boundary. Repair findings with
   a superseding candidate when needed.
5. Hand accepted source to a separately admitted current-generator projection
   and extracted installed consumer; qualify replay and a later exact dev
   integration effect. Keep final stable release gates open.

## Recovery

If tests or review fail, retain red output and the candidate identity.
Regenerate any report-writing outputs only in the correct later projection;
restore only outputs this task generated accidentally. Do not overwrite user
work or treat a stale archive as a source pass. No ref, release or target
effect is required for this source repair.

## Progress

- [x] Admit bounded WorkUnit on a clean task branch from observed dev.
- [x] Reproduce red empty-target regression.
- [x] Implement narrow fix and pass affected tests.
- [x] Obtain exact independent source review, ACCEPT_WITH_NOTES for `f00d937e`.
- [ ] Route accepted source to artifact projection and installed recheck.

The reviewer identified nonempty target queue routing as a distinct
release-blocking follow-up. Project artifacts after that source repair.
