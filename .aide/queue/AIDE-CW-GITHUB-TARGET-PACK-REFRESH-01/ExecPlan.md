# ExecPlan: Combined Target Source Artifact Refresh

## Objective and source

Clear the exact pack provenance failure observed after two-parent source merge
`6a581dbcfbd5d208f957956096aacb18b832301a`. The inherited tracked pack
names source `1397b703a9c116a5b555948b8587dc53a668237a`. Generate only local,
no-publish portable and release artifacts from a clean checkpoint.

## Progress

- [x] Observe the committed combined-source failure in `validate`, `doctor`,
  and `pack-status`; no unrelated failure was reported.
- [x] Create this bounded local artifact WorkUnit under the owner's direction.
- [x] Commit clean admission `4deeed08` and preview checkpoint `66ef462c`.
- [x] Generate current-source changelog previews and the portable pack.
- [x] Generate and validate local release bundle and draft; inspect exact assets.
- [x] Commit artifact checkpoint `cda504b9`, rerun the full generator cycle,
  and prove a second 44-file cycle changes zero bytes.
- [x] Commit source-ancestor projection `d4bd4938`.
- [x] Replay all four generators from the committed clean tree; 44 files,
  zero changes.
- [x] Run final canonical and exact-byte consumer checks.
- [ ] Publish the exact qualified integration branch.
- [ ] Fast-forward `dev` only after the above passes; observe remote identity.

## Verification and recovery

Use the current repaired generator from accepted release-integrity `dev`.
Compare generated paths against the allowlist. `pack-status`, release validation,
draft validation, canonical validate, doctor, and explicit asset hash/size checks
must pass. If pre-commit generation fails, repair only this task's generated
outputs in the isolated branch; after publication, fix forward. Do not promote
to main, tag, upload, publish, activate hosted settings, or mutate a target repo.
