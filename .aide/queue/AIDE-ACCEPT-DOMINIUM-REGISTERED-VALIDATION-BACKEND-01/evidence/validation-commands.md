# Validation Commands

Planned and executed validation commands:

```text
py -3 -m json.tool .aide\reports\dominium-registered-validation-backend-accept\acceptance-report.json
py -3 -m json.tool .aide\reports\dominium-registered-validation-backend-accept\accepted-capability.json
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
py -3 .aide\scripts\aide_lite.py validate
rg --pcre2 local absolute path scan over acceptance reports and evidence
rg --pcre2 secret-like value scan over acceptance reports and evidence
git -C <dominium-root> status --short --branch
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py commit check --latest
```
