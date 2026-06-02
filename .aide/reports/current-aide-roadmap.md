# Current AIDE Roadmap

This compact roadmap reflects AIDE-CHECK-OS-01.

## Current

`AIDE-CHECK-OS-01 - Task OS and Validation Telemetry Checkpoint`

Result: PARTIAL_NEEDS_REPAIR.

## Next

`AIDE-FIX-OS-03 - Task OS checkpoint report consistency repair`

Expected focus:

- repair report-only Task OS checkpoint status logic for X-OS-02 truth
- repair Task OS next-plan output after X-OS-02
- repair latest-task parsing so current checkpoint/repair/apply packet identity wins over older historical refs
- add tests/goldens for checkpoint-to-repair and later checkpoint-to-apply reporting

## Then

- rerun compact checkpoint verification
- `AIDE-APPLY-00 - Transaction Model`, only if report consistency repair passes

## Deferred

- Eureka and Dominium target validation
- target sync and pilots
- transactional apply implementation beyond report-only transaction modeling
- branch/worktree apply
- merge, push, promotion
- release publication
- GitHub API mutation
- Gateway/provider/model runtime
