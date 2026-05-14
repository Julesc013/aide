# Validation

## Baseline

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git rev-parse HEAD`: PASS, `bf27445fd62e79d39fc2d34c30127f9f360cc8b5`.
- `git rev-list --left-right --count origin/main...HEAD`: PASS, `0 6`; local `main` was six commits ahead of `origin/main` before Q42.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; pre-existing generated manifest source fingerprint stale warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same generated manifest stale warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same generated manifest stale warning and Q41 status metadata drift found before repair.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN; existing unknown file classification warnings.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Final

Pending final validation run.
