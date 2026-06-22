# Validation Commands

- `py -3 -m py_compile .aide/scripts/aide_lite.py core/interop/dominium/*.py .aide/scripts/tests/test_aide_dominium_readonly_seam_repair_04.py`: PASS
- `py -3 .aide/scripts/tests/test_aide_dominium_readonly_seam_repair_04.py`: PASS
- `direct project_dominium_seam(write_portability=False) + validate + diff + demo + portability_check`: PASS
- `Repair 03 targeted non-portability regression methods`: PASS
- `Repair 02 targeted non-portability regression methods`: PASS
- `Base seam targeted regression methods excluding CLI project portability path`: PASS
- `Full Repair 02 and Repair 03 suites`: TIMEOUT_REPLACED_BY_TARGETED_PLUS_STANDALONE_PORTABILITY
