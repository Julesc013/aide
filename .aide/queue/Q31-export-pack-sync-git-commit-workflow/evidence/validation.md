# Q31 Validation

## Baseline Before Q31 Edits

- `git status --short`: PASS, clean at Q31 intake.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`; no `dev`.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `0e62caef186f47c6c58f3ba75b41d42e14e95b48`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate warnings and generated-manifest fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning classes.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; report-only, recommends earlier review-gated Q25.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 22/22 golden tasks before Q31 additions.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; report-only, `trunk_without_dev`, current branch `main`, role `canonical`.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS with expected dirty-tree/missing-`dev` warnings after baseline-generated artifacts.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS_BLOCKED; dirty tree and missing `dev`, no mutation.
- `py -3 .aide/scripts/aide_lite.py git sync --dry-run`: PASS_BLOCKED; dry-run only.
- `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev`: PASS_BLOCKED; source `main` protected and `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main`: PASS_BLOCKED; source `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git prune --dry-run`: PASS; no eligible protected/current branch pruning.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS, 183 files, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 165 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Final Validation

- `git status --short`: PASS before final evidence/status edits; final commit
  records remaining Q31 generated artifacts.
- `git diff --check`: PASS; PowerShell/Git reported CRLF normalization
  warnings only.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD ->
  origin/main`, `origin/main`; no local or remote `dev`.
- `git remote -v`: PASS, origin
  `https://github.com/Julesc013/aide.git`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; warnings are existing
  review-gate/generated-manifest fingerprint drift classes, not Q31 hard
  failures.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same historical warning
  classes and no Q31 blocker.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; existing queue review
  guidance remains review-gate-only.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS after regenerating the
  Codex adapter managed section; token-ledger near-budget warnings remain
  informational.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 27/27 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS, 20 commits,
  7 categories, 0 malformed commits.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS, report-only,
  `trunk_without_dev`, current branch `main`, role `canonical`.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS with expected warnings
  for dirty generated artifacts and missing `dev`.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, blocked by dirty tree
  classification and absent `dev`, no mutation.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS, 194 portable files, 197 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid,
  source dirty state recorded truthfully, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q32 Eureka Sync From
  Canonical AIDE Pack"`: PASS, `.aide/context/latest-task-packet.md`, 3,692
  chars, 923 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest review packet
  regenerated.
- `py -3 .aide/scripts/aide_lite.py estimate --file
  .aide/context/latest-task-packet.md`: PASS, 923 approximate tokens, within
  budget.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 171 tests. An
  earlier short-timeout run was replaced by this completed run.
- `py -3 -m unittest discover -s .aide/scripts/tests -p
  test_q31_export_pack_governance.py`: PASS, 6 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests
  after rerun. A prior concurrent run observed a transient generated-eval
  report mutation.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- Targeted `rg` secret scan: PASS_AFTER_INSPECTION. Matches are
  policy/test/template/path terms and regex definitions such as `api_key`,
  `SECRET`, `TOKEN`, `PASSWORD`, `sk-ant`, and `latest-task-packet`; no actual
  provider key, `.env` content, `.aide.local` state, private key, raw prompt,
  or raw response was found.
