# Validation Commands

```text
py -3 .aide/queue/AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01/evidence/independent_trust_check.py
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"
py -3 .aide/scripts/aide_lite.py trust validate
py -3 .aide/scripts/aide_lite.py trust status
py -3 -m compileall core/protocol .aide/scripts/tests
py -3 .aide/scripts/aide_lite.py trust project --source contract-projection
py -3 .aide/scripts/aide_lite.py trust project --source contract-projection
py -3 .aide/scripts/aide_lite.py validate
```

Additional validation is run after report materialization:

```text
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
