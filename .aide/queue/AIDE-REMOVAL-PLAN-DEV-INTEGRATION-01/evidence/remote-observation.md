# Remote dev observation after accepted removal-planner integration

- Execution identity: `BLACKGLASS-WIN1\Jules`; `gh auth status` reported active
  `Julesc013` under that identity. No credential value was recorded.
- Before effect: local primary `dev`, `origin/dev`, and `git ls-remote`
  `refs/heads/dev` all identified
  `1c75abf1d93b34be8998383ea2ce4c9084c9d612`; task candidate was
  `ae0e29e98eb436136f1d62d7830a4d8b20251b32`. The old dev was an
  ancestor, both worktrees were clean, and the dry-run helper plan reported
  `ready_dry_run` with no blockers. One integration writer was used.
- Normal `git push origin task/aide-removal-dev-integration-01` created the task
  ref. Primary `dev` then fast-forwarded locally with `git merge --ff-only`
  to the exact candidate. Normal `git push origin dev` reported
  `1c75abf1..ae0e29e9`; no force push or protected-ref bypass was used.
- After effect: `git ls-remote` independently reported both `dev` and task ref
  at `ae0e29e98eb436136f1d62d7830a4d8b20251b32`. GitHub's Git ref API
  returned the same SHA for `dev`. Local `dev` tree is
  `63d2d1094862f4c97760fe4b3f2177a84e9c1b9e`, worktree clean and
  synchronized with `origin/dev`. Old removal source `d1362f91` remains an
  ancestor.
- Qualified payload and local archive digests are recorded in
  `review-and-artifact-qualification.md`. This observation is dev integration,
  not removal apply, main promotion, stable publication, or hosted acceptance.
