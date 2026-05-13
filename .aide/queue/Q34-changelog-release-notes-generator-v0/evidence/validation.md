# Validation

## Baseline Before Q34 Edits

- `git status --short`: PASS, clean before validation commands.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`, remote `origin/main`.
- `git remote -v`: PASS, `origin` read/write URLs recorded; no remote mutation performed.
- `git rev-parse HEAD`: PASS, `ca2cc5a1b5599eabd0a02f202dabea75d905844b`.
- `git tag --list`: PASS, no tags.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; known queue review-gate warnings and stale generated manifest warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 27/27 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~10..HEAD`: PASS, 10/10 commits.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS, early Q27 preview generated from `HEAD~20..HEAD`.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS, report-only; generated local reports.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS with warnings for dirty tree after generated baseline files and missing `dev`.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS with same report-only state.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, blocked plan due dirty generated baseline files; no mutation.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid, dirty source recorded.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS.

Generated baseline commands refreshed changelog, golden-run, and Git report files. These are Q34-allowed generated artifacts and will be regenerated again after implementation.

## Final Validation

Pending.
