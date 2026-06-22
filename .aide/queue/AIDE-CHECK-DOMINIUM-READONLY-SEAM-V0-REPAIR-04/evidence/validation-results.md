# Validation Results

Completed before final task-inspection pass:

- `git status --short --branch`: passed; branch `main`; only allowed check-task, report, queue index, and planning/execution files changed.
- `git diff --check`: passed.
- `git diff --cached --check`: passed before staging and again after staging the final allowed changes.
- `git rev-parse 270b97d`: passed; resolved to `270b97dc66e477cd37a2f863c8604854a5e90bdf`.
- `git show --no-patch --format=fuller 270b97d`: passed; confirmed Repair 04 commit metadata and message.
- `py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests`: passed.
- Independent Repair 04 check harness: completed full run in 933.9 seconds and returned `REQUEST_CHANGES`, `material_finding_count: 4`, `warning_count: 1`, recommended next task `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
- Combined seam unittest discovery: timed out after 1206.2 seconds; not counted as a pass. Stale Python processes from the timed-out run were stopped.

Split seam module results:

- `test_aide_dominium_readonly_seam_repair_04.py`: passed, 7 tests, 2.087 seconds.
- `test_aide_dominium_readonly_seam_repair_03.py`: passed, 15 tests, 646.308 seconds.
- `test_aide_dominium_readonly_seam_repair_02.py`: passed, 12 tests, 758.767 seconds.
- `test_aide_dominium_readonly_seam_repair.py`: failed, 20 tests, 1 failure, 222.033 seconds. The failure is `test_next_task_routes_to_repair_check`, which expects `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` while live code now routes to `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.
- `test_aide_dominium_readonly_seam.py`: passed, 111 tests, 341.942 seconds.

Explicit live seam command sequence:

- `dominium-seam status`: passed, 4.990 seconds.
- `dominium-seam snapshot`: passed, 4.764 seconds.
- `dominium-seam project`: passed, 556.122 seconds.
- `dominium-seam validate`: passed, 27.486 seconds.
- `dominium-seam diff`: passed, 52.191 seconds.
- `dominium-seam demo`: passed, 121.240 seconds.

Final queue and repository validation:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`: passed; `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`: passed; no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`: passed after standard evidence files were added; `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`: passed; no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py validate`: passed.
- Strict secret-like scan over the new check queue and report roots: passed; no matches.

Material independent check failures:

- `schema.open_object_surfaces_bounded`
- `extension.authority_names_semantically_refused`
- `conformance.guard_evidence_exercised`
- `operation.guard_report_not_static`

The result remains `REQUEST_CHANGES`; no implementation repair was attempted.
