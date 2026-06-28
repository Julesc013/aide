# Validation Commands

```text
py -3 -m py_compile .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py
py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py
py -3 .aide/scripts/aide_lite.py distribution-apply verify
py -3 .aide/scripts/aide_lite.py install validate
py -3 .aide/scripts/aide_lite.py upgrade validate
py -3 .aide/scripts/aide_lite.py rollback validate
py -3 .aide/scripts/aide_lite.py uninstall validate
py -3 .aide/scripts/aide_lite.py release validate
py -3 .aide/scripts/aide_lite.py release draft-validate
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01
rg -n --pcre2 "(?i)(BEGIN (RSA|DSA|EC|OPENSSH|PRIVATE) KEY|api[_-]?key\s*[:=]|secret\s*[:=]|token\s*[:=]|password\s*[:=])" .aide/fixtures/aide-self-consumer-fixture-v0 .aide/reports/aide-self-consumer-fixture-v0 .aide/queue/AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py PLANS.md IMPLEMENT.md .aide/queue/index.yaml
git diff -U0 -- .aide/queue/index.yaml PLANS.md IMPLEMENT.md | rg -n --pcre2 "latest-(task|context)-packet|raw (prompt|response)|C:[/\\]Users"
rg -n --pcre2 "latest-(task|context)-packet|raw (prompt|response)|C:[/\\]Users" .aide/fixtures/aide-self-consumer-fixture-v0 .aide/reports/aide-self-consumer-fixture-v0 .aide/queue/AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py --glob '!validation-commands.md' --glob '!safety-scans.md'
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
