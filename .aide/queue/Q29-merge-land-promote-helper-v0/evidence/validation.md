# Q29 Validation

## Baseline Before Q29 Edits

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `0fb6bb2872d718a3ad9f402c2cf026e2b583ebc4`.
- `git log --oneline --decorate -30`: PASS; Q28 commit sequence is present.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`; shell also emitted a local oh-my-posh init warning unrelated to Git ignore behavior.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate and generated-manifest fingerprint warnings.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning classes.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q29 was still listed as superseded before this reopen.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 15/15 golden tasks.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; report-only, writes workflow detection artifacts.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS; current branch `main`, role `canonical`, dirty tree true after generated detection write, `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; pre-Q27 malformed commits are reported, no release publishing.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: baseline timed out at two minutes before Q29 changes; rerun with longer timeout in final validation.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Final Validation

Pending Q29 implementation.
