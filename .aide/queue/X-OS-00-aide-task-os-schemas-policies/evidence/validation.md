# Validation

Status: `PASS_WITH_WARNINGS`

All blocking validation gates passed. The warnings are expected governance states for an unreviewed task and dirty source before commit.

## Commands

- `git diff --check`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 146/146 golden tasks, including all six Task OS golden tasks.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test tiers`: PASS.
- `py -3 .aide/scripts/aide_lite.py test telemetry-status`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 315 tests in 582.569s.
- Targeted high-confidence secret scan across Task OS source/docs/evidence and export-pack copies: PASS, no matches.

## Boundary Results

- provider_or_model_calls: none.
- network_calls: none.
- raw_prompt_storage: false.
- raw_response_storage: false.
- target_test_suites_run: false.
- branch_mutations_performed: false.
- release_publication_performed: false.
