# Validation Results

Structural checks:

- `git status --short --branch`: PASS; dirty paths are within the Phase A allowlist.
- `git diff --check`: PASS; Git reported CRLF normalization warning for the schema file but no whitespace errors.
- `git diff --cached --check`: PASS; no staged changes at the time of check.
- `py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests`: PASS.

Focused and full individual seam modules:

- `test_aide_dominium_readonly_seam_repair_05.py`: PASS, 7 tests, 1.778 seconds.
- `test_aide_dominium_readonly_seam_repair_04.py`: PASS, 7 tests, 2.399 seconds.
- `test_aide_dominium_readonly_seam_repair_03.py`: PASS, 15 tests, 634.946 seconds, portability-heavy.
- `test_aide_dominium_readonly_seam_repair_02.py`: PASS, 12 tests, 724.780 seconds, portability-heavy.
- `test_aide_dominium_readonly_seam_repair.py`: PASS, 20 tests, 228.257 seconds.
- `test_aide_dominium_readonly_seam.py`: PASS, 111 tests, 334.628 seconds.

Seam CLI:

- `dominium-seam status`: PASS_WITH_WARNINGS, 4.579 seconds.
- `dominium-seam snapshot`: PASS, 4.623 seconds.
- `dominium-seam project`: PASS_WITH_WARNINGS, 546.058 seconds.
- `dominium-seam validate`: PASS_WITH_WARNINGS, 27.187 seconds.
- `dominium-seam diff`: PASS, 52.271 seconds.
- `dominium-seam demo`: PASS_WITH_WARNINGS, 125.461 seconds.

Additional verification:

- Schema surface audit: PASS, zero unclassified objects and zero unintentionally open objects.
- Extension denylist matrix: PASS, denied variants returned `extension.authority_change`; benign extensions passed.
- Actual guard nonce probes: PASS, every forbidden family reached the guard and did not call the injected executor.
- Guard report digest recomputation: PASS.
- Operation coverage derivation from guard evidence: PASS in Repair 05 tests.
- Negative fixture replay: PASS through individual seam modules.
- Actual unsupported CLI probes: PASS through conformance tests.
- Dominium source mutation check: PASS, `source_mutation_count: 0`.
- Required output set and isolated portability: PASS through `dominium-seam project` and portability-heavy test modules.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- JSON parse scan over Repair 05 queue/reports and regenerated seam JSON: PASS, 71 files parsed.
- Initial strict secret-like scan: NOT MATERIAL, two false positives (`token` local variable and a test forbidden-fragment literal).
- Refined secret-like scan over Repair 05 queue/reports, Dominium interop code, and changed seam tests: PASS, zero secret-like hits.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, no dirty Dominium paths; checkout remains `main...origin/main [behind 24]`.
- Final `git diff --check`: PASS; Git reported CRLF normalization warning for the schema file but no whitespace errors.

Post-commit validation still required:

- `py -3 .aide/scripts/aide_lite.py commit check --latest`.
