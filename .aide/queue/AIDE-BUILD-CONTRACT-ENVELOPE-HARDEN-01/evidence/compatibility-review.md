# Compatibility Review

- Existing lifecycle fixture run report parses.
- Existing lifecycle fixture verify report parses.
- Existing lifecycle fixture acceptance report remains projected additively when present.
- Existing projection paths remain stable under `.aide/reports/contract-envelope/projections/`.
- Existing source reports are not destructively migrated.
- Top-level scalar source report `status` fields remain unchanged.
- `fixture_temp_apply_only` remains the only recognized capability label.
- Unknown optional fields remain tolerated.
- Unknown required capabilities fail closed.

Final lifecycle fixture compatibility checks passed:

- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py`

No canonical fixture diff remained after validation.
