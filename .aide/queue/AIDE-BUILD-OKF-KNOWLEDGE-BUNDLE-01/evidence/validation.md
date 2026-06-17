# Validation

Final result: `PASS_WITH_WARNINGS`.

Warnings are non-blocking:

- `full YAML parser unavailable; stdlib structural frontmatter validation used`
- `.aide/context/latest-task-packet.md may lag .aide/queue/index.yaml`
- `git diff --check` exited 0 while warning that `.aide/queue/index.yaml` will be normalized from CRLF to LF next time Git touches it.

Commands run:

```bat
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core/knowledge/okf_bundle.py
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_okf_knowledge_bundle.py
py -3 .aide/scripts/aide_lite.py okf status
py -3 .aide/scripts/aide_lite.py okf project --source current-repo
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
py -3 -m json.tool .aide/reports/okf/projection-report.json
py -3 -m json.tool .aide/reports/okf/validation.json
py -3 -m json.tool .aide/reports/okf/lint.json
py -3 -m json.tool .aide/reports/okf/concept-index.json
py -3 -m json.tool .aide/reports/okf/link-index.json
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py workunit-queue validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py contract-envelope validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py validate
```

Observed results:

- `git diff --check`: exit 0 with CRLF normalization warning for `.aide/queue/index.yaml`.
- `git diff --cached --check`: PASS.
- Python compile checks: PASS.
- Focused OKF tests: PASS, 8 tests.
- `okf status`: `PASS_WITH_WARNINGS`, concept count `24`.
- `okf project --source current-repo`: `PASS_WITH_WARNINGS`, source artifacts mutated `false`.
- `okf validate`: `PASS_WITH_WARNINGS`, required pages exist, all concepts have frontmatter and non-empty `type`, AIDE refs parse, event refs parse, authority boundary preserved, overclaiming check passed.
- `okf lint`: `PASS_WITH_WARNINGS`, broken links `0`, orphan pages `0`, missing source refs `0`, missing evidence refs `0`, stale context findings `1`, overclaiming findings `0`.
- OKF JSON reports: PASS.
- `event-record validate`: `PASS_WITH_WARNINGS`.
- `reference-id validate`: `PASS_WITH_WARNINGS`.
- `test-job validate`: PASS.
- `worker-run validate`: PASS.
- `workunit-queue validate`: PASS.
- `evidence-packet validate`: PASS.
- `contract-envelope validate`: PASS.
- `task inspect`: complete, evidence files `19`, missing evidence `0`.
- `task evidence`: missing evidence `0`.
- Broad `validate`: PASS on rerun with output consumed fully.

Generated churn handling:

- `test-job validate` and `workunit-queue validate` refreshed two predecessor generated report files; those changes were restored because they are outside this task scope.
- Existing unrelated `.aide/intake/latest-*` changes and `.aide/intake/preflight-or-blocker-report.md` are outside this task scope and were preserved unmodified.
