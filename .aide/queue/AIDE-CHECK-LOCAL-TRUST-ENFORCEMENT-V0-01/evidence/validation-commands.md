# Validation Commands

Commands planned for this check:

```text
py -3 .aide/queue/AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01/evidence/independent_local_trust_check.py
py -3 .aide/scripts/aide_lite.py local-trust status
py -3 .aide/scripts/aide_lite.py local-trust validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
py -3 -m compileall core/service core/protocol .aide/scripts/tests
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
git status --short --branch --untracked-files=all
```
