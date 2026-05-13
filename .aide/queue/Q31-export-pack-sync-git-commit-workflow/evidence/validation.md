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

To be completed before review.
