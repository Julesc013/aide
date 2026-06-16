# Test Results

Focused tests:

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reference_id_scheme.py`: PASS, 20 tests.

Compile checks:

- `py -3 -m py_compile core/protocol/reference_id.py .aide/scripts/tests/test_aide_reference_id_scheme.py .aide/scripts/aide_lite.py`: PASS.

Notes:

- `py -3 -m unittest .aide.scripts.tests.test_aide_reference_id_scheme`: NOT USED as a final command because `.aide` is a dot-prefixed directory and the dotted module form fails with an empty module segment. Discovery is the supported focused invocation for this file.
