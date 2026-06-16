# Test Results

Result: PASS_WITH_WARNINGS.

Focused tests and compile checks:

- `py -3 -m py_compile core/protocol/reference_id.py`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reference_id_scheme.py`: PASS, 20 tests.

ReferenceID commands:

- `py -3 .aide/scripts/aide_lite.py reference-id status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS.

Predecessor validators:

- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.

Warnings:

- The successful result remains `PASS_WITH_WARNINGS` because runtime resolution and full JSON Schema validation are intentionally deferred.
