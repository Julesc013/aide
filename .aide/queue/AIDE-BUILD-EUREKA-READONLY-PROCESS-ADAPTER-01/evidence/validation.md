# Validation

Completed validation so far:

- `py -3 -m compileall core/interop/eureka core/execution core/protocol .aide/scripts/tests` passed.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py` passed.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py` passed.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py` passed.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py` passed.
- `py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter run --eureka-root <local-eureka-checkout> --expected-revision e582028b1db977e28ba6ddc0ed284ca6ccf48234` passed with warnings.
- `py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter validate` passed with warnings and `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01` passed and classified the task as complete.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01` passed with no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate` passed.
- `git diff --check` passed.
- `git diff --cached --check` passed.
