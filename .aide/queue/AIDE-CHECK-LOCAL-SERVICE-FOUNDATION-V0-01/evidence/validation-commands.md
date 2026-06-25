# Validation Commands

```text
py -3 .aide/queue/AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01/evidence/independent_local_service_check.py
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
py -3 .aide/scripts/aide_lite.py local-service status
py -3 .aide/scripts/aide_lite.py local-service validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
absolute local path scan
strict secret-like scan
```
