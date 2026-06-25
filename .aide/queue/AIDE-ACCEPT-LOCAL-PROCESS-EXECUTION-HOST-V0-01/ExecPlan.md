# AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01 ExecPlan

## Objective

Accept exactly `local_process_execution_host_fixture_v0` after the source build,
two repairs, and Repair 02 independent check completed with zero remaining
material findings and missing evidence zero.

## Scope

Allowed paths are limited to this acceptance task packet, the acceptance report
directory, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

No implementation, tests, schemas, source reports, provider code, interop code,
runtime state, Workbench/MCP behavior, repository mutation, branch/worktree
automation, GitHub mutation, release, or promotion is authorized.

## Dependencies

- `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`: source build completed with warnings.
- `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`: recorded material findings and routed to Repair 01.
- `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`: closed initial build findings pending check.
- `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`: recorded remaining material assertions and routed to Repair 02.
- `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`: reports `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`.
- `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`: reports `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, and recommends this acceptance.

## Plan

1. Verify queue truth and predecessor reports.
2. Record the exact accepted capability and accepted scope.
3. Preserve warnings and explicit non-capabilities.
4. Materialize acceptance task evidence and reports.
5. Update queue index and focused root planning/execution logs.
6. Run task evidence checks, focused local-process tests, broad validation, diff checks, leak scans, and commit policy.
7. Stop at `needs_review` with `ACCEPTED_WITH_WARNINGS` and recommend exactly `AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01`.

## Validation Intent

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`
- `py -3 .aide/scripts/aide_lite.py local-process-execution-host validate`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`
- `git diff --cached --check`
- acceptance report/evidence absolute-path and secret-like scans
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## Exit Criteria

The task stops at `needs_review` with:

```text
result: ACCEPTED_WITH_WARNINGS
accepted_capability: local_process_execution_host_fixture_v0
material_finding_count: 0
missing_evidence: 0
recommended_next_task: AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```
