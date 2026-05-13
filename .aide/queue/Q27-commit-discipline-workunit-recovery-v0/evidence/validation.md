# Q27 Validation

Status: IN PROGRESS.

## Baseline Before Q27 Edits

- `git status --short`: PASS; worktree initially clean.
- `git branch --show-current`: PASS; `main`.
- `git rev-parse HEAD`: PASS; `05330b0842a3e39487bb67d8d8b44b4c40902ad7`.
- `git check-ignore .aide.local/`: PASS; `.aide.local/` is ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing queue review-gate warnings.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; existing queue review-gate warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q25/Q26 review and Q27 redo recommendation.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; generated pack artifacts.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; provenance result `DIRTY_SOURCE_RECORDED`.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: TIMED OUT during baseline run; canonical `py -3 .aide/scripts/aide_lite.py test` passed.

## Final Validation

- Pending.
