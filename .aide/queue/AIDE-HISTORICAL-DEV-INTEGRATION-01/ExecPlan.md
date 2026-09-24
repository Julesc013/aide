# ExecPlan: historical disposition dev integration

## Objective and scope

Merge the exact reviewed historical source and owner decisions into accepted
customization dev with both histories retained. Work only in the source branch
delta, queue coordination, root indexes, and generated portable/release outputs.
Do not activate native or hosted effects or publish a release.

## Dependencies and sequence

1. Confirm current dev, historical head, merge base, clean worktree, and one
   shared-Git writer. Run the helper plan and read-only merge preflight.
2. Merge without an automatic commit. Keep accepted dev generated artifacts
   during source conflict resolution and reconcile queue/root documents.
3. Commit the coherent source merge with an explicit artifact-refresh gap.
4. Regenerate the portable export and local release/draft from that committed
   combined source, then qualify exact outputs and post-commit replay.
5. Obtain independent technical review of the exact integrated candidate.
6. Publish the task branch and fast-forward dev only if refs and checks remain
   valid; observe remote identities and close task evidence.

## Progress

- [x] Exact current dev and published historical heads checked; merge preflight run.
- [x] Both parent histories merged; queue and root-document conflicts resolved.
- [x] Current dev generated snapshot retained during source merge.
- [x] Combined source committed at `e40aec47`; current generator refreshed
  portable/release/draft outputs and a stable 888-file replay changed zero.
- [x] Affected tests and canonical local checks passed as recorded in evidence.
- [x] Post-commit provenance exposed a dirty-source record in the first
  projection; regenerate from clean `3326868b` with export first and record
  the corrected clean manifest and asset hashes.
- [x] Commit qualified generated projection at `7c12fc40`; post-commit
  release bundle, validate, draft, and draft-validate replay changed zero of
  44 release files. Pack status is `PASS_SOURCE_ANCESTOR`.
- [x] Obtain independent technical review of exact commit `7c12fc40`:
  `ACCEPT_WITH_NOTES` for source/artifact integration, with an evidence-only
  closeout and narrow check required before the dev fast-forward.
- [ ] Check this evidence-only closeout, update remote dev, and observe its
  resulting commit and tree.

## Verification and likely blockers

Run focused historical checks including raw A/B/C, affected customization and
portable consumer tests, release/draft validation, canonical validate/doctor,
archive checksums and replay. Preserve the Windows privilege skip explicitly.
The known 27 conflict paths are mostly derived artifacts; queue index,
DOCUMENTATION.md, and IMPLEMENT.md require both histories. Recheck actual
conflicts before mutation, and never copy the older branch's generated pack or
release snapshot over current dev.
