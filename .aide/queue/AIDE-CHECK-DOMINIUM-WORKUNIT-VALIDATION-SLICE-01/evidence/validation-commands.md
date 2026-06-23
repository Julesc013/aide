# Validation Commands

Executed:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse 8d8f511c77388b96118eb530f5361090b66911c1
py -3 .aide\queue\AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01\evidence\independent_workunit_validation_check.py
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py validate
```

The independent harness performs:

- source authority inspection;
- executor call instrumentation;
- unsupported capability refusal probe;
- malformed request refusal probe;
- independent workspace digest recomputation;
- two clean deterministic reruns in temporary roots;
- no absolute path or secret-like leakage scan;
- ContextDescriptor, ContextPack, WorkUnit, EvidencePacket, and EventRecord
  structural/reference checks;
- false-boundary verification.
