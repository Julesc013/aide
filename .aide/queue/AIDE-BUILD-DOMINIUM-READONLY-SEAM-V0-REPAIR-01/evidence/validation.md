# Validation

Commands run during repair:

- `py -3 -m compileall core/interop/dominium .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_dominium_readonly_seam.py .aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py`: PASS.
- `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py`: PASS, 20 tests.
- `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam.py`: PASS, 111 tests.
- `py -3 .aide/scripts/aide_lite.py dominium-seam demo`: PASS_WITH_WARNINGS, source mutation count zero, forbidden operation count zero.
- `py -3 .aide/scripts/aide_lite.py dominium-seam validate`: PASS_WITH_WARNINGS, zero errors.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, `## main...origin/main [behind 24]`.

Final validation:

- JSON parsing for repair reports, task evidence JSON, and regenerated seam reports: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`: PASS, `missing:` empty.
- `git diff --check`: PASS. Git reported CRLF normalization warnings for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors were reported.
- `git diff --cached --check`: PASS with no staged changes.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Bounded value-oriented secret-like scan over changed repair paths: PASS, no matches.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS for the latest existing commit.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, unchanged at `## main...origin/main [behind 24]`.
