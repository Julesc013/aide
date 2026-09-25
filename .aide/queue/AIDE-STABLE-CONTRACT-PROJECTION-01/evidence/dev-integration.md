# Observed stable contract preview dev effect

Effect manifest:
`D:/Projects/AIDE/_review_scratch/stable-contract-projection-2defcad5-dev-effect-manifest.json`,
SHA-256 `7f9ab10193e56cb265ca02dc14d608405a4c374f273bc19fc620554b72c9fad0`.
Independent conditional GO report SHA-256
`531744866cca3d9ee5dfc67ce27b99a77535bf24e4f6fce50806beabc30ca52e`.

Immediately before effect, identity was `BLACKGLASS-WIN1\Jules`, `gh auth
status` exited 0, `gh api user` returned `Julesc013`, both worktrees were
clean, only the primary worktree held `dev`, and no checked Git lock or
unfinished-operation marker existed. Candidate commit/tree and ZIP/tar,
manifest and review hashes matched. Local, tracking, ls-remote and GitHub API
refs all equaled base `a32535a2675f191ae3515f39501658e91ef41103`.

`git merge --ff-only 2defcad541d02cd33fabf75e20c48dfd091ffabe` in the
primary `dev` worktree exited 0. `git push origin dev` normally exited 0.
All four post-effect ref reads returned exact
`2defcad541d02cd33fabf75e20c48dfd091ffabe`; primary tree was
`14b13c209a4aaae7842fc7a58ce18b614005bae2` and worktree clean.
External effect log:
`D:/Projects/AIDE/_review_scratch/stable-contract-projection-2defcad5-dev-effect.log`,
SHA-256 `324fe2eae0e7d9d8d4e42bce602e6fd43ae1f9928358413e8081abc68155fb6d`.

No force push, main/tag/upload/publication, hosted setting or target effect
was performed. A separate evidence-only closeout commit records this result;
it does not alter the frozen reviewed source or archive bytes.
