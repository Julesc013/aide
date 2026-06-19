# Validation

Acceptance validation commands are run after the acceptance packet is
materialized:

```bash
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-CHECK-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-CHECK-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py context-pack-v2 status
py -3 .aide/scripts/aide_lite.py validate
```

Results are appended before commit.

Final results:

- build task inspect: complete, `missing_evidence: 0`
- check task inspect: complete, `missing_evidence: 0`
- acceptance task inspect: complete, `missing_evidence: 0`
- acceptance task evidence: no missing files
- ContextPack v2 status: `PASS_WITH_WARNINGS`
- focused ContextPack v2 tests: 13 passed
- Python compilation: passed
- acceptance/check JSON parsing: passed
- broad AIDE validation: `PASS`
- diff checks: passed; `git diff --check` emitted only a queue-index CRLF normalization warning
