# Validation

Validation commands run during implementation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial baseline clean on `main`; final status reviewed separately. |
| `py -3 -m py_compile core/protocol/patch_transaction.py .aide/scripts/aide_lite.py` | PASS | Early compile check. |
| `py -3 -m py_compile core/protocol/patch_transaction.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_patch_transaction.py` | PASS | Final compile check. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py` | PASS | 22 focused tests. |
| `py -3 .aide/scripts/aide_lite.py patch-transaction status` | PASS | `PASS_WITH_WARNINGS`. |
| `py -3 .aide/scripts/aide_lite.py patch-transaction project` | PASS | `PASS_WITH_WARNINGS`, no source artifact mutation. |
| `py -3 .aide/scripts/aide_lite.py patch-transaction validate` | PASS | `PASS_WITH_WARNINGS`, deterministic projection true. |
| `py -3 .aide/scripts/aide_lite.py reference-id validate` | PASS_WITH_WARNINGS | Predecessor remains projection-only; no runtime registry. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | Predecessor remains projection-only; no event store. |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | PASS | Predecessor preserved. |
| `py -3 .aide/scripts/aide_lite.py workunit validate` | PASS | Queue WorkUnit validation preserved. |
| `py -3 .aide/scripts/aide_lite.py worker-run validate` | PASS | WorkerRun remains metadata-only; no worker execution. |
| `py -3 .aide/scripts/aide_lite.py test-job validate` | PASS | TestJob remains metadata/projection-only; no Test Broker runtime. |
| `py -3 .aide/scripts/aide_lite.py capability-manifest validate` | PASS_WITH_WARNINGS | Declaration-only boundary preserved. |
| `py -3 .aide/scripts/aide_lite.py conformance-profile validate` | PASS_WITH_WARNINGS | Candidate inactive profile boundary preserved. |
| `py -3 .aide/scripts/aide_lite.py conformance-result validate` | PASS_WITH_WARNINGS | Evidence-projected, runnerless, non-admitting, non-trusting boundary preserved. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` | PASS | Classification `complete`, `missing_evidence: 0`. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` | PASS | 18 evidence files, no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad AIDE validation passed. |
| `py -3 -m json.tool` over generated PatchTransaction JSON reports | PASS | All generated JSON reports parse. |
| Repeated projection/source hash comparison | PASS | `transactions.json` and sample patch artifact stable; source inputs unchanged. |
| Secret-like value scan over changed files | PASS | No high-signal secret-like values found. |

Final Git diff checks and commit-policy validation are recorded after staging.
