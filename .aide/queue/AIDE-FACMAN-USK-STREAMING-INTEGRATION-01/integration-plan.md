# Historical initial integration plan

This original pre-commit plan is retained below as historical context. Its source/check/merge stages completed; current accepted truth is recorded in ExecPlan.md and evidence/validation.md. The exact original bytes are preserved under evidence/historical-before-closeout/integration-plan.md.

# Reviewed USK streaming remediation integration plan

Current explicit user authority covers full Beta1 implementation, validation, sync, commits and normal checked merges. Primary dev remains clean f1931488bd260ca7f77c5d5e227d08d59dea65ab. Existing task branch must fast-forward to remote18cb4b76b915a3033638cf6b39b39a9e159e0efe before applying the reviewed seven-file correction.

Reuse the clean primary temporarily on its existing task branch to apply/commit the independently reviewed patch, avoiding a third worktree. Preserve the two existing marker-owned evidence worktrees and their source receipts. Return primary to clean dev after non-force task push. Do not rewrite refs, force-push, delete evidence, or merge protected source in this operation.

Approved revised patch SHA25605f1a30f31dac99fcc337f980b85d18c9b5de534d020aa685a2a254d9174b42d supersedes rejectedf4df2a2e. Independent review found no remaining P0/P1/P2 in the revised bounded delta. Existing validation:51Python tests, strict checks, clean Windows x64 5/5native tests. Retain-only state is persisted before streamed effects, and both new and older journal readers lack automatic uncertain cleanup authority. Apply entry budget is enforced before transaction effects.

Verify every resulting source hash against the reviewed receipt, rerun local Python/strict checks, commit and push PR27 for fresh complete hosted CI. PR28 propagation and Linux/macOS/Win32 qualification remain separate. Current provider hygiene promotion precedes another completed unit entering dev under the one-unpromoted-unit rule.

## Completed chain

The current synchronized provider observation is main `ffe1b407abb1bbc340bc925396bd4be197002033`, dev `5e4c660890201accb30a14ed31b97d329a3be3cd`, shared source tree `3faabe599f2ebe5f2a6f87287693f411fe1d6594`; primary is clean dev. This is source/provider integration truth, not FacMan pin adoption or Beta1 product acceptance. The exact final receipt is the ZIP coordinator's `evidence/provider-source/path-admission-canonical-integration-chain.json` (SHA256 `149351d0aae2f6965614b602ddafa82358966be03a34e5926ba146f7f65dfda6`).
