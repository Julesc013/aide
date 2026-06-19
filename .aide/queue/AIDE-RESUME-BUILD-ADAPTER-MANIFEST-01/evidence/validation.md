# Validation

Validation commands run for the resume build:

```bash
git status --short --branch
py -3 -m py_compile core/protocol/adapter_manifest.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_adapter_manifest.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_adapter_manifest.py
py -3 .aide/scripts/aide_lite.py adapter-manifest status
py -3 .aide/scripts/aide_lite.py adapter-manifest project
py -3 .aide/scripts/aide_lite.py adapter-manifest validate
```

Initial focused validation found a ReferenceID integration mismatch and a
temporary-workspace CLI source omission. Both were corrected before task
evidence was finalized. The final focused compile, tests, project, and validate
passes succeeded with `PASS_WITH_WARNINGS` for AdapterManifest commands.

Additional final broad validation results are appended before commit.

Final validation results:

- `git diff --check`: passed with the known CRLF notice for `.aide/queue/index.yaml`.
- `git diff --cached --check`: passed.
- Python compile: passed.
- focused AdapterManifest tests: 13 passed.
- `adapter-manifest status`: `PASS_WITH_WARNINGS`.
- `adapter-manifest project`: `PASS_WITH_WARNINGS`.
- `adapter-manifest validate`: `PASS_WITH_WARNINGS`.
- `reference-id validate`: `PASS_WITH_WARNINGS`.
- `event-record validate`: `PASS_WITH_WARNINGS`.
- `evidence-packet validate`: `PASS`.
- `workunit validate`: `PASS`.
- `worker-run validate`: `PASS`.
- `test-job validate`: `PASS`.
- `capability-manifest validate`: `PASS_WITH_WARNINGS`.
- `conformance-profile validate`: `PASS_WITH_WARNINGS`.
- `conformance-result validate`: `PASS_WITH_WARNINGS`.
- `task inspect --task-id AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01`: complete with `missing_evidence: 0`.
- `task evidence --task-id AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01`: no missing evidence.
- `aide_lite.py validate`: `PASS`.
- JSON parse for schema and generated AdapterManifest JSON reports: passed.
- Narrow secret-like value scan over changed files: 0 findings.

Unrelated generated report churn from broad validation was restored before
completion.
