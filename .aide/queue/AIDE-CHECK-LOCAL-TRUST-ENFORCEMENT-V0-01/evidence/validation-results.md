# Validation Results

Initial independent harness:

```text
py -3 .aide/queue/AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01/evidence/independent_local_trust_check.py
PASS
```

The remaining validation command results are appended after final validation.

Final validation:

```text
py -3 .aide/scripts/aide_lite.py local-trust status
PASS

py -3 .aide/scripts/aide_lite.py local-trust validate
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"
PASS (6 tests)

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"
PASS (11 tests)

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
PASS (7 tests)

py -3 -m compileall core/service core/protocol .aide/scripts/tests
PASS

py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
PASS (complete, missing_evidence 0)

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
PASS (missing empty)

py -3 .aide/scripts/aide_lite.py validate
PASS

git diff --check
PASS

git diff --cached --check
PASS

scoped path and secret-like scan over check task and report surfaces
PASS (no hits)
```
