# Validation Commands

Primary commands:

```text
py -3 -m compileall core/interop/eureka core/execution core/protocol .aide/scripts/tests
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py
py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter run --eureka-root <local-eureka-checkout> --expected-revision e582028b1db977e28ba6ddc0ed284ca6ccf48234
py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
