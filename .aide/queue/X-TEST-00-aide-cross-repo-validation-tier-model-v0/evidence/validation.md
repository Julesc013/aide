# Validation Evidence

Final validation results:

- `git diff --check`: PASS.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide compile --write`: PASS; refreshed stale generated manifest, then rerun with manifest current.
- `py -3 scripts/aide validate`: PASS, 149 info, 0 warning, 0 error.
- `py -3 scripts/aide doctor`: PASS, 149 info, 0 warning, 0 error.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, no warnings.
- `py -3 .aide/scripts/aide_lite.py verify --changed-files`: PASS, 0 warnings.
- `py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md --review-packet .aide/context/latest-review-packet.md --write-report .aide/verification/latest-verification-report.md`: PASS, 0 warnings.
- `py -3 .aide/scripts/aide_lite.py repo inventory`: PASS, unknown_count 0.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 140/140 tasks, 0 warnings.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 306 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, boundary PASS, checksums valid, `DIRTY_SOURCE_RECORDED`.

X-TEST-00 command checks:

- `test tiers`: PASS.
- `test tier-plan`: PASS.
- `test impact-plan --from HEAD`: PASS, recommended `T1`, report-only.
- `test telemetry-status`: PASS.
- `test full-discovery-handoff`: PASS, external handoff only.
- `test summary-validate` valid example: PASS.
- `test summary-validate` invalid raw-log example: expected FAIL.
- `test slow-report-validate`: PASS.

No Dominium or Eureka target tests were run.
