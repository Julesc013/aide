# Validation

## Result

PASS_WITH_WARNINGS. All substantive validators passed; warnings are limited to the required review gate, fixture-only scope, expected generated report churn, and export-pack dirty-source provenance.

## Commands Run

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m py_compile core/apply/managed_sections.py`: PASS.
- `py -3 -m unittest discover -s core/apply/tests -t .`: PASS, 10 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_01_managed_sections.py`: PASS, 6 tests.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-plan`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS, 333 checks.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS, 138 checks.
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS, 489 checks.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS, 225 checks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 171/171 golden tasks.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 89 checked files, 96 changed files, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py export-pack`: PASS, 824 included files, 827 checksum entries.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksum validation PASS, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.
- `git diff --check`: PASS.
- `rg -n "sk-ant-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH|PRIVATE) KEY" ...`: PASS, no matches.

## Notes

- A broader term scan produced policy and identifier matches only, including token-budget and secret-scan policy text; no secret material was identified.
- The AIDE Lite parser test intentionally checks that `managed-section apply` is not accepted.
