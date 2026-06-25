# Validation Commands

```text
py -3 .aide\scripts\aide_lite.py local-trust fixture
py -3 .aide\scripts\aide_lite.py local-trust status
py -3 .aide\scripts\aide_lite.py local-trust validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
py -3 -m compileall core/service core/protocol .aide/scripts/tests
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide\scripts\aide_lite.py validate
git diff --check
git ls-files .aide.local
new-surface absolute path scan
new-surface secret-like scan
```
