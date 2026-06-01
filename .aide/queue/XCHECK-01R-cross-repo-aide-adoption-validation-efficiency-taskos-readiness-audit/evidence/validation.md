# Validation Evidence

Baseline validation before writing XCHECK-01R:

- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, with pre-existing review-packet token warning.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, dry-run helper artifacts refreshed.
- `git diff --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py release status`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-status`: PASS.

Final validation after writing XCHECK-01R:

- `git status --short`: PASS, scoped XCHECK/report/context/generated-evidence changes only.
- `git diff --check`: PASS.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: PASS.
- `py -3 scripts/aide doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, with pre-existing review-packet token warning.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 132/132 golden tasks.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS for the pre-existing latest commit.
- `py -3 .aide/scripts/aide_lite.py pack --task "X-TEST-00 AIDE Cross-Repo Validation Tier Model"`: PASS, wrote `.aide/context/latest-task-packet.md`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 4,156 chars, 121 lines, approximately 1,039 tokens, within 3,200-token task-packet budget.

Target repositories:

- Dominium and Eureka were inspected read-only with Git and file reads.
- No Dominium or Eureka validation suites were run because target generated-state writes were forbidden for XCHECK-01R.
- No target files were modified.
