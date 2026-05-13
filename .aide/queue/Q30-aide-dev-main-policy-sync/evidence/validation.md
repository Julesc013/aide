# Q30 Validation

## Baseline Before Q30 Edits

- `git status --short`: PASS, clean before baseline report generation.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`; a local oh-my-posh init warning appeared once and is unrelated to Git state.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `31bd0b29115c9686c4dbdf35577c6d22770ca346`.
- `git log --oneline --decorate -20`: PASS; Q27-Q29 commit sequences are present.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate warnings and generated-manifest fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning classes.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; reports Q29 at needs_review and older review-gate follow-ups.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS; local oh-my-posh warning emitted after command completion.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 20/20 golden tasks before Q30.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; generated current workflow report.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS; after report generation, dirty tree true and `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS_BLOCKED; dirty tree and missing `dev`.
- `py -3 .aide/scripts/aide_lite.py git sync --dry-run`: PASS_BLOCKED; dry-run only, dirty tree blocks apply.
- `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev`: PASS_BLOCKED; source `main` is canonical/protected and `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main`: PASS_BLOCKED; `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git prune --dry-run`: PASS; current/protected `main` is not eligible.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; 3 malformed pre-Q27 commits reported, no release publishing.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary PASS.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Final Validation

Pending implementation.
