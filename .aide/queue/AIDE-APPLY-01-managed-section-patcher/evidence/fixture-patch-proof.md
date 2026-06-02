# Fixture Patch Proof

## Fixture Inputs

- Source fixture: `.aide/examples/apply/managed-section-fixtures/valid_input.md`
- Replacement fixture: `.aide/examples/apply/managed-section-fixtures/replacement.md`
- Expected output: `.aide/examples/apply/managed-section-fixtures/expected_output.md`

## Generated Proof

- `managed-section fixture-plan`: PASS.
- `managed-section fixture-verify`: PASS, 138 checks.
- `.aide/reports/managed-section-fixture-plan.json` records `mode: fixture_only`, `status: PASS`, patch hashes, operation record, and `real_repo_apply_allowed: false`.
- `.aide/reports/managed-section-fixture-validation.md` validates the fixture plan and no-apply boundary.

## Test Coverage

- `core/apply/tests/test_managed_sections.py` verifies in-memory patching and fixture-only file patch records.
- `.aide/scripts/tests/test_aide_apply_01_managed_sections.py` verifies the AIDE Lite fixture plan output and command boundary.
- `managed_section_fixture_patch_golden`: PASS.
