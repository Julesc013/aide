# ExecPlan: project-owned three-way updates

## Objective and scope

Close the mandatory update/customization gap from campaign coverage: a project
can resolve a real overlapping upstream change without losing its direct edit,
and an explicitly disabled optional feature stays disabled over later packs.
An absent previously owned file with no declared disable is a conflict, not a
new copy. Use the existing guarded import transaction and receipt. The owner
authorized this bounded implementation and technical-review route.

Allowed paths are the importer, its regression tests, the portable-pack user
guide, this WorkUnit, parent campaign evidence, queue index, PLANS/IMPLEMENT,
and the deterministic export/changelog/release projections generated only
after source is frozen. No real target repository, hosted target, main or
publication effect is in scope.

## Dependencies and exact base

- Local and remote `dev@d4b67c96ff81eb10aeecd6763b538331844619c9`
  contain the qualified rollback/removal lifecycle candidate and its closeout.
- External read-only design note:
  `D:/Projects/AIDE/_review_scratch/three-way-update-and-disable-design-723322cf.md`,
  SHA-256 `a080427b461906dca55c4e24c3bb1f8336ba0e59f6e1dfcd8a4222b321a6e0c9`.
  It is implementation analysis, not an adopted competing spec.
- External test-only patch:
  `D:/Projects/AIDE/_review_scratch/three-way-red-regressions-9a0843c3.patch`,
  SHA-256 `215cecb5881266689bf11b86b40603afae5b6e05e4cf0a9cd24943dcfe28b732`.
  Recheck its context on this new branch; it has not been applied or run.

## Sequence and checks

1. Verify clean base, patch identity/context, and current receipt/import
   contracts. Apply test-only regressions; run each to preserve red failure.
2. Implement manual `--resolve TARGET FILE` and Python `resolutions` for one
   receipt-owned ordinary file, with exact predecessor pack, plan digest,
   regular-file input and stale/race refusal. Keep AGENTS managed-block
   resolution closed until a focused preservation oracle exists.
3. Store resolved installed bytes separately from upstream source digest in
   a versioned receipt. Keep overlays across V2/V3 until another explicit
   resolution; do not let repair, rollback or removal claim unknown bytes.
4. Add a project-owned versioned disable declaration for one explicit
   optional package path group (`local_state_examples` for
   `.aide.local.example/`). Unknown IDs and essential paths fail closed.
   Test two updates, direct changes, missing rationale and reenablement.
5. Run focused/adversarial and affected importer/lifecycle tests. Freeze
   source for independent review. Regenerate the current pack/release outputs
   only after source passes, then run extracted fresh/brownfield consumers,
   canonical checks, exact artifact review and zero-diff postcommit replay.
6. Integrate only the independently accepted exact candidate through one
   writer, then record observed remote `dev`. Parent release gates remain open.

## Recovery and effect boundary

The existing import intent and guarded Windows write transaction own effects.
Resolution files, project control bytes, target preimages and receipt identity
must be bound to one preview and rechecked at effect time. Any uncertain
effect is reconciled before replay. No duplicate updater or automatic semantic
merge is introduced. The independent reviewer must judge changed source,
security predicates and final delivered bytes at their exact revisions.

## Progress

- [x] Read-only design and red test patch prepared externally.
- [x] Task branch/worktree created from observed `dev@d4b67c96`.
- [x] Apply the test-only patch and run both cases separately on the exact
      admitted base. They fail at the expected missing-resolution API and
      missing-receipt-owned-file conflict assertions; external logs are bound
      in `evidence/red-regressions.md`.
- [x] Implement v2 overlay/disable receipts, plan-bound manual resolution,
      missing-owned conflict, guarded input reads, explanations, compatibility
      and effect-time checks. Fourteen focused cases passed on the preceding
      source; two delta cases passed on final source. Exact hashes and logs are
      in `evidence/source-candidate-validation.md`.
- [x] Freeze source commit `acbcb9c8` and obtain independent technical review.
      It returned `REQUEST_CHANGES` for a receipt-owned CRLF `AGENTS.md`
      update regression. Add a red/green Windows oracle and superseding repair;
      exact external review and test hashes are in `evidence/crlf-review-repair.md`.
- [x] Obtain independent delta review of CRLF repair commit `32395301`.
      It returned `REQUEST_CHANGES`: a re-digested receipt could relabel a
      direct AGENTS edit and overwrite it. The reviewer also independently
      confirmed the pre-existing ordinary managed-file analogue. Both exact
      reports and red oracles are bound in `evidence/predecessor-baseline-repair.md`.
- [x] Independently review predecessor-bound source `12758e07`; it received
      ACCEPT_WITH_NOTES for source integration. The first full importer run
      completed 94/95 cases with one outdated forged-receipt fixture. The
      corrected exact single case passes; the update-only full rerun was stopped
      after 13 passing cases when the accepted repair-health source became
      available for one combined qualification run. See
      `evidence/full-suite-correction.md`. No artifact generation precedes
      a passing full suite.
- [x] Run full combined 100-case importer suite, affected Q31/Q34/Q47/Q48
      suites, deterministic generators, canonical checks, extracted ZIP/tar
      canary and independent artifact review. Exact identities, results and
      limitations are in `evidence/combined-qualification-99a9e54d.md`.
- [ ] Commit the generated projection, prove zero-diff postcommit replay,
      obtain exact effect review and integrate qualified bytes into observed
      remote `dev`.
