# Validation

Commands run:

```bash
py -3 -m py_compile core/protocol/context_pack_v2.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_context_pack_v2.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_context_pack_v2.py
py -3 .aide/scripts/aide_lite.py context-pack-v2 status
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
```

Results:

- compilation: passed
- focused tests: 13 passed
- ContextPack status: `PASS_WITH_WARNINGS`
- build task inspect: complete, `missing_evidence: 0`
- independent source hash/determinism probe: passed

Final task inspect/evidence, broad validation, diff checks, JSON parsing, and
commit policy are recorded after all check files are materialized.

Final commands:

```bash
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-CHECK-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-CHECK-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
```

Final results:

- task inspect: `classification: complete`, `missing_evidence: 0`
- task evidence: no missing files
- broad AIDE validation: `PASS`
- check-report JSON parsing: passed
- diff checks: passed; `git diff --check` emitted only a queue-index CRLF normalization warning
