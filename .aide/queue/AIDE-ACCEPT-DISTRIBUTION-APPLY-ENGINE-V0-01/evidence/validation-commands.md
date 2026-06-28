# Validation Commands

Commands to run after acceptance files are present:

```text
py -3 -m compileall core/distribution .aide/scripts/tests/test_aide_distribution_apply_engine_v0.py
py -3 .aide/scripts/tests/test_aide_distribution_apply_engine_v0.py
py -3 .aide/scripts/aide_lite.py distribution-apply status
py -3 .aide/scripts/aide_lite.py distribution-apply plan --scenario managed-file-update
py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp
py -3 .aide/scripts/aide_lite.py distribution-apply verify
py -3 .aide/scripts/aide_lite.py install validate
py -3 .aide/scripts/aide_lite.py upgrade validate
py -3 .aide/scripts/aide_lite.py rollback validate
py -3 .aide/scripts/aide_lite.py uninstall validate
py -3 .aide/scripts/aide_lite.py release validate
py -3 .aide/scripts/aide_lite.py release draft-validate
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01
rg -n "BEGIN (RSA|DSA|EC|OPENSSH|PRIVATE) KEY|api[_-]?key|secret|token|password" .aide/queue/AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01 .aide/reports/distribution-apply-engine-v0-acceptance PLANS.md IMPLEMENT.md .aide/queue/index.yaml
git diff -U0 -- .aide/queue/index.yaml PLANS.md IMPLEMENT.md | rg -n --pcre2 "latest-(task|context)-packet|raw (prompt|response)|C:[/\\]Users"
rg -n --pcre2 "latest-(task|context)-packet|raw (prompt|response)|C:[/\\]Users" .aide/reports/distribution-apply-engine-v0-acceptance .aide/queue/AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01 --glob '!validation-commands.md' --glob '!safety-scans.md'
rg -n "\.aide\.local" .aide/reports/distribution-apply-engine-v0-acceptance .aide/queue/AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01 --glob '!task.yaml' --glob '!validation-commands.md' --glob '!safety-scans.md'
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
