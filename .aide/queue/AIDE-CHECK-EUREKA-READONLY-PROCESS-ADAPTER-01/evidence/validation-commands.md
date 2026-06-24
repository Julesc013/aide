# Validation Commands

Commands run for this check:

```text
git diff --name-only 60d54a0..961add0 -- core/execution/registered_process.py core/protocol/process_invocation.py core/protocol/execution_receipt.py core/interop/aide core/interop/dominium
rg -n "eureka|public_alpha|public-alpha" core/execution/registered_process.py core/protocol/process_invocation.py core/protocol/execution_receipt.py
git -C <local-eureka-checkout> status --short --branch
git -C <local-eureka-checkout> rev-parse HEAD
py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter validate
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py
py -3 .aide/scripts/aide_lite.py validate
```
