# Validation

## Results

- `git status --short`: PASS, expected Q45/export/generated artifacts remain dirty before final closeout commit.
- `git diff --check`: PASS.
- `git branch --show-current`: PASS, `main`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` is ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; pre-existing stale generated manifest source fingerprint warning remains.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same pre-existing generated manifest warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q45 listed as running before final status update.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS with extended timeout; the default 120 second wrapper timeout was too short for the current internal selftest.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS with extended timeout.
- `py -3 .aide/scripts/aide_lite.py repo validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`: PASS; command refreshed only a Q42 report source commit, which was reverted because it is outside Q45 scope.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install status`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair status`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade observe-current`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade observe-source`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade compare`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade plan`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade dry-run`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade status`: PASS; planned updates 5, skips 8, preservations 209, conflicts 209, no-apply true.
- `py -3 .aide/scripts/aide_lite.py upgrade compatibility`: PASS; unsupported count 8, unknown count 0, no-apply true.
- `py -3 .aide/scripts/aide_lite.py upgrade conflicts`: PASS; conflict count 209, blocking count 8, no-apply true.
- `py -3 .aide/scripts/aide_lite.py upgrade migrations`: PASS; required count 8, optional count 201, automatic migration false.
- `py -3 .aide/scripts/aide_lite.py upgrade explain .aide/scripts/aide_lite.py`: PASS; current script is compatible and no-action with apply/overwrite/delete false.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS after sequential rerun; an earlier parallel export/status attempt hit a Windows file lock and was discarded.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q46 Rollback Uninstall Model v0"`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; latest packet is within budget.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q45_upgrade_model.py -v`: PASS.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: TIMEOUT at 120 seconds twice; stopped the validation process and recorded as unresolved.
- Targeted `rg` secret scan over requested paths: PASS_AFTER_INSPECTION. Matches are policy, docs, path, generated-reference, regex, and test-fixture terms such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, `sk-ant`, and `latest-task-packet`; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt log, or raw response log was found. The requested root `tools` path is absent.
- Targeted high-risk assignment scan for long secret-like values: PASS, no matches.

## Not Rerun

- `py -3 .aide/scripts/aide_lite.py eval run`: NOT_RERUN in final pass because the command rewrites `.aide/evals/runs/latest-*`, which is outside Q45 allowed paths. Q45-specific golden tasks were run during implementation, and AIDE Lite `test`/`selftest` passed their internal eval coverage.
- `py -3 .aide/scripts/aide_lite.py changelog preview` / `changelog validate`: NOT_RERUN in final pass to avoid preview-output churn outside Q45 scope.

## Notes

- No provider, model, network, target-repo, branch, GitHub mutation, install apply, repair apply, upgrade apply, rollback, or uninstall command was run.
- No file moves, deletes, reference rewrites, overwrites, migrations, or target mutations were performed.
