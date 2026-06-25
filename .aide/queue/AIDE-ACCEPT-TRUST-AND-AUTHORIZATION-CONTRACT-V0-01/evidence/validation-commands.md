# Validation Commands

```text
py -3 .aide/queue/AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01/evidence/acceptance_review.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py trust validate
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
