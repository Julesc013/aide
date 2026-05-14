# Validation

Interpreter: `py -3`.

## Baseline

- `git status --short`: PASS; working tree had Q44 in-progress changes only.
- `git branch --show-current`: PASS; `main`.
- `git branch --all`: PASS.
- `git remote -v`: PASS.
- `git rev-parse HEAD`: PASS; Q44 started from `85442fe952ef3e48f157d8a868144128e75a329b`.
- `git tag --list`: PASS.
- `git check-ignore .aide.local/`: PASS.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS with pre-existing stale generated manifest source fingerprint warning.
- `py -3 scripts/aide doctor`: PASS with the same pre-existing warning.
- `py -3 scripts/aide self-check`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install status`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, dirty-source provenance recorded.

## Final Pre-Commit Validation

- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS.
- `py -3 scripts/aide doctor`: PASS.
- `py -3 scripts/aide self-check`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install status`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair observe`: PASS; 11 issues, 0 blockers, no-apply true.
- `py -3 .aide/scripts/aide_lite.py repair diagnose`: PASS; 11 diagnoses, 0 blockers, no-apply true.
- `py -3 .aide/scripts/aide_lite.py repair plan`: PASS; 11 operations, 0 conflicts, no-apply true.
- `py -3 .aide/scripts/aide_lite.py repair dry-run`: PASS; 11 planned future writes, 0 skips, 0 conflicts, 0 blockers, target mutation false.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair status`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair classes`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair doctor`: PASS; advisory report only.
- `py -3 .aide/scripts/aide_lite.py repair explain .aide/export/aide-lite-pack-v0/manifest.yaml`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS; generated preview files were restored because changelog outputs are outside Q44 allowed paths.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS; advisory only.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, dirty-source provenance recorded.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q45 Upgrade Model v0"`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q44_repair_doctor.py`: PASS; 8 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS.

## Notes

- `py -3 .aide/scripts/aide_lite.py commit check --latest` failed before the final export/evidence commit because the latest commit at that moment was the earlier Q44 docs commit. The final Q44 export/evidence commit uses the required Q27 structured body and must be checked after commit creation.
- Full `.aide/scripts/tests` discovery was not rerun to completion after an earlier long attempt timed out. The targeted Q44 unit suite, AIDE Lite `test`, AIDE Lite `selftest`, golden eval run, and core unittest suites passed.
- Broad secret-scan pattern returned matches in policy, docs, tests, and evidence terms. A stricter key-shaped scan found only test/evidence strings that forbid `OPENAI_API_KEY=` and `BEGIN PRIVATE KEY`; no actual secret value was found.
- No provider/model calls, network calls, branch mutation, target repo mutation, repair apply, file moves, deletions, overwrites, or reference rewrites were introduced.
