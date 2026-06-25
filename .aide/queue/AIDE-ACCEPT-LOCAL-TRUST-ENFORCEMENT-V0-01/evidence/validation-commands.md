# Validation Commands

```text
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01
py -3 .aide/scripts/aide_lite.py local-trust validate
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
scoped path and secret-like scan over acceptance task and report surfaces
```
