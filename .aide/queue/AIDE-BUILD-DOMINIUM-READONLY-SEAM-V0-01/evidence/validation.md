# Validation

Validation completed before final staging:

- `py -3 -m py_compile .aide/scripts/aide_lite.py core/interop/dominium/__init__.py core/interop/dominium/models.py core/interop/dominium/references.py core/interop/dominium/snapshot.py core/interop/dominium/mappings.py core/interop/dominium/projector.py core/interop/dominium/validation.py core/interop/dominium/diagnostics.py core/interop/dominium/refusals.py core/interop/dominium/conformance.py core/interop/dominium/bundle.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py dominium-seam status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py dominium-seam project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py dominium-seam validate`: PASS_WITH_WARNINGS with zero errors.
- `py -3 .aide/scripts/aide_lite.py dominium-seam demo`: PASS_WITH_WARNINGS, source mutation count zero, forbidden operation count zero.
- `py -3 .aide/scripts/aide_lite.py dominium-seam apply`: REFUSED as unsupported read-only boundary operation.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam.py -v`: PASS, 108 tests.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: unchanged at `## main...origin/main [behind 24]`.

Final broad validation, diff checks, task evidence checks, secret scan, and commit-policy validation are appended after final staging.

Final pre-staging validation:

- `git diff --check`: PASS. Git reported CRLF normalization warnings for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors were reported.
- `git diff --cached --check`: PASS with no staged changes.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing:` empty.
- JSON parsing for seam reports and task evidence JSON: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py dominium-seam diff`: PASS, repeated projection byte equality true.
- `py -3 .aide/scripts/aide_lite.py dominium-seam snapshot`: PASS, selected file count 17, behind origin/main 24.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, unchanged at `## main...origin/main [behind 24]`.
- Bounded strict secret-like scan over new seam paths: PASS, no matches.
- `git status --short --branch`: PASS, dirty paths are limited to the task allowlist.
- After compacting negative fixture files, reran `py -3 -m py_compile ...`: PASS.
- After compacting negative fixture files, reran `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam.py`: PASS, 108 tests.
- After compacting negative fixture files, reran JSON parsing for seam reports and task evidence JSON: PASS.
- After compacting negative fixture files, reran `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- After compacting negative fixture files, reran `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing_evidence: 0`.
- After compacting negative fixture files, reran `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing:` empty.
