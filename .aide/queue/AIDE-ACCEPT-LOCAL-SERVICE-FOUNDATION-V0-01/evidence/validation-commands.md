# Validation Commands

```text
py -3 .aide/queue/AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01/evidence/acceptance_review.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01
py -3 .aide/scripts/aide_lite.py local-service validate
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
absolute local path scan
strict secret-like scan
```
