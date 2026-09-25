# Observed forced-restart evidence dev effect, 2026-09-26

Independent focused reviewer `/root/customization_review` gave
**ACCEPT_WITH_NOTES**, conditional GO only for exact candidate
`e88b1c2ee6f3206c628f79908e430a7967e9f58c`, tree
`2ffe74918bde44356e9f66737bd5573687733a81`, from
`dev@493e3f13c1b2e754dd8fb5f533380ba13a7b8979`. Original external
review:
`D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/independent-e88b1c2-dev-effect-rereview.md`,
SHA-256 `087ecc4fdb48c7fdf79ed0b99a110653f164961188c0bce5c56202c1e583bee8`.

Fresh effect preflight under `BLACKGLASS-WIN1\Jules` / `Julesc013` found
four equal base refs, clean primary and candidate, one `dev` worktree, base
ancestry, no checked lock/operation markers, exact candidate tree, ZIP SHA
`68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c`
and tar.gz SHA
`d0b424563ea7a85d207546b0e2b0d381641e046659846876adbddf96a954073b`.
One-writer `git merge --ff-only` and normal `git push origin dev` both exited
zero. The immediate readback found local/tracking/`ls-remote` at `e88b1c2e`
but the GitHub git/ref API still returned old `493e3f13`. No mutation was
replayed. A subsequent uncached git/ref API and branch API read, along with
local/tracking/`ls-remote`, all returned exact `e88b1c2e`; primary was clean.
External observed-effect original SHA-256
`8fd2cd5683121d411ef3c5dbad3597ee69db0f7b712c76e9ab9d33e828fd2064`
is preserved outside the repository at
`D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/observed-dev-effect.txt`.

This is evidence-only dev integration. Partial-import recovery, main, tag,
publication and downloaded-byte acceptance remain open.
