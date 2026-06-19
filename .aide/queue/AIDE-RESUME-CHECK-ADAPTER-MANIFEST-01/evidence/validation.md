# Validation

Validation commands run:

```bash
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core/protocol/adapter_manifest.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_adapter_manifest.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_adapter_manifest.py
py -3 .aide/scripts/aide_lite.py adapter-manifest status
py -3 .aide/scripts/aide_lite.py adapter-manifest project
py -3 .aide/scripts/aide_lite.py adapter-manifest validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01
py -3 .aide/scripts/aide_lite.py validate
```

Initial check probes passed. Final broad validation results are recorded before
commit.

Final validation results:

- `git diff --check`: passed with the known CRLF notice for `.aide/queue/index.yaml`.
- `git diff --cached --check`: passed before commit.
- Python compile: passed.
- focused AdapterManifest tests: 13 passed.
- `adapter-manifest status`: `PASS_WITH_WARNINGS`.
- `adapter-manifest project`: `PASS_WITH_WARNINGS`.
- `adapter-manifest validate`: `PASS_WITH_WARNINGS`.
- build task inspect/evidence: complete with `missing_evidence: 0`.
- check task inspect/evidence: complete with `missing_evidence: 0`.
- `aide_lite.py validate`: `PASS`.
- JSON parse for resume-check JSON reports: passed.
- narrow secret-like value scan over changed files: 0 findings.
- unsupported operation probes for apply/approve/execute/rollback: failed closed.
