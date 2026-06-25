# Validation Commands

```text
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
py -3 .aide/scripts/aide_lite.py local-service init-fixture
py -3 .aide/scripts/aide_lite.py local-service fixture
py -3 .aide/scripts/aide_lite.py local-service status
py -3 .aide/scripts/aide_lite.py local-service validate
```

Final validation also includes compileall, trust/local-process regressions,
task inspect/evidence, broad validation, diff checks, local-state check, and
leak scans.
