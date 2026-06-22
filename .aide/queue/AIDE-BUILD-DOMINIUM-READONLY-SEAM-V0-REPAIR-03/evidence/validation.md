# Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | baseline branch main; working tree clean before Repair 03 scaffold |
| `py -3 .aide/scripts/aide_lite.py git plan` | PASS | ready_dry_run; generated .aide/git report churn restored because outside Repair 03 allowlist |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id <predecessor>` | PASS | accepted charter and all seam predecessor build/check/repair tasks reported missing_evidence: 0 |
| `git show -s --format="%H %s" <six predecessor commits>` | PASS | all source-chain commits resolved |
| `py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests` | PASS | compiled after Repair 03 code and test changes |
| `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam.py` | PASS | 111 tests passed |
| `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py` | PASS | 20 tests passed |
| `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam_repair_02.py` | PASS | 12 tests passed |
| `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam_repair_03.py` | PASS | 15 tests passed |
| `py -3 .aide/scripts/aide_lite.py dominium-seam status` | PASS | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py dominium-seam snapshot` | PASS | PASS; pinned Dominium revision c92b386027890c1bbf14aef6eaafe0357b7b03dd; behind_origin_main 24 |
| `py -3 .aide/scripts/aide_lite.py dominium-seam project` | PASS | PASS_WITH_WARNINGS; refreshed seam artifacts and portability result |
| `py -3 .aide/scripts/aide_lite.py dominium-seam validate` | PASS | PASS_WITH_WARNINGS; error_count 0 |
| `py -3 .aide/scripts/aide_lite.py dominium-seam diff` | PASS | PASS; byte_equal true |
| `py -3 .aide/scripts/aide_lite.py dominium-seam demo` | PASS | PASS_WITH_WARNINGS; source_mutation_count 0; forbidden_operation_count 0 |
| `Repair 03 unsupported-operation probe matrix` | PASS | 17 unsupported verbs returned typed REFUSED and preserved false-boundary output |
| `Repair 03 historical root preservation check` | PASS | changed_historical_file_count 0 |
| `rg secret-like scan over changed repair surfaces` | PASS_WITH_NOTES | only benign matches: secret-scan filenames and internal ContextVar token variable |
| `git diff --check` | PASS | whitespace check passed; Git emitted expected LF normalization warning for rewritten schema JSON |
| `git diff --cached --check` | PASS | no staged diff issues |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | broad AIDE validation passed |
