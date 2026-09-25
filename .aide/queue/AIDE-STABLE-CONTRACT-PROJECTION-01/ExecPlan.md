# ExecPlan: AIDE-STABLE-CONTRACT-PROJECTION-01

## Objective and scope

Close the export-provenance failure created by the source-only stable Lite
contract candidate. This task owns derived export, changelog, bundle and
draft previews, exact combined validation, artifact review and a qualified
`dev` effect. `task.yaml` bounds paths and excludes main/tag/publication.

## Dependencies

- Current accepted `dev` is `a32535a2675f191ae3515f39501658e91ef41103`.
- Contract repair source is exact reviewed commit
  `d38e5839fe102fd4b38dc29971877753ccb6e2ec`, tree
  `cee0ddf6800b3cb29cf192ae5ac6e9f0da684457`. Its substantive policy
  repair is ancestor `4315a813`, tree `26a8f1081896326c47415a185b0f001f93b8d901`.
- Independent technical rereview ACCEPT is in `evidence/source-review-acceptance.md`.
  A changed source receives focused review.
- The `aa3bcfec` review found committed provenance failure; its report and
  the three failing command logs are retained in the source task.

## Execution plan

1. Confirm source review, clean branch and current `dev` ancestry; rerun
   narrow CLI/policy checks if the review requires them.
2. Run `export-pack`, `changelog preview`, `release bundle`, `release
   validate`, `release draft` and `release draft-validate` from clean source.
   Preserve commands, exits, logs, source/tree and asset hashes.
3. Inspect archive entries, boundaries, checksums and provenance; run
   canonical validate/doctor/pack-status and affected release suites.
4. Commit the exact generated projection. Reconcile HEAD-bound metadata with
   an explicit subsequent metadata commit only if required, recording any
   first failed replay. A final four-command release replay must change zero
   tracked files and preserve archive bytes.
5. Obtain independent exact artifact and dev-effect verdict. Recheck identity,
   shared worktree writers, refs, ancestry and clean state immediately before
   one-writer dev fast-forward and normal push. Observe local and remote refs.
6. Update queue and parent coverage after the effect. Keep final stable
   qualification and publication gates open.

## Verification and recovery

Use deterministic commands and external immutable log hashes. If generation
or review fails, repair and supersede the exact candidate; do not label a
source-only stale pack as passing. If a Git/remote effect is uncertain, read
refs and effects before retrying. Do not overwrite generated outputs from an
older branch or silently rebuild reviewed bytes.

## Progress

- [x] Admit this bounded projection under the owner's campaign delegation.
- [x] Confirm independent acceptance of the frozen contract repair source.
- [x] Generate and qualify derived previews and exact delivered artifacts
  locally, including the 25-command extracted ZIP/tar consumer.
- [ ] Prove committed replay and canonical checks.
- [ ] Obtain independent artifact and dev-effect verdict.
- [ ] Integrate qualified candidate into `dev` and observe remote identity.
