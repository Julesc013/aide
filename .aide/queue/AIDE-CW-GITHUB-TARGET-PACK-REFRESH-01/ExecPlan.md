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
- [ ] Commit a clean admission checkpoint before generation.
- [ ] Generate current-source changelog previews and the portable pack.
- [ ] Generate and validate local release bundle and draft; inspect exact assets.
- [ ] Commit the artifact checkpoint, rerun the full generator cycle, and commit
  any source-ancestor projection required for final byte convergence.
- [ ] Replay from the committed clean tree and prove zero tracked output changes.
- [ ] Run canonical checks and publish the exact qualified integration branch.
- [ ] Fast-forward `dev` only after the above passes; observe remote identity.

## Verification and recovery

Use the current repaired generator from accepted release-integrity `dev`.
Compare generated paths against the allowlist. `pack-status`, release validation,
draft validation, canonical validate, doctor, and explicit asset hash/size checks
must pass. If pre-commit generation fails, repair only this task's generated
outputs in the isolated branch; after publication, fix forward. Do not promote
to main, tag, upload, publish, activate hosted settings, or mutate a target repo.
