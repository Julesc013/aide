# No Real Apply Boundary

Task: AIDE-APPLY-00-transaction-model

## Enforced Boundary

- Real repository apply mode: not implemented.
- Target repository mutation: false.
- Branch mutation: false.
- Release publication: false.
- GitHub API calls: none.
- Provider/model/Gateway calls: none.
- Network calls: none.

## Proof Points

- `transaction_no_real_apply_golden` - PASS, 15/15.
- `transaction status` reports `mode: report_only`.
- `transaction fixture-plan` and `transaction fixture-verify` write only `.aide/reports/**`.
- Parser registration adds only `status`, `validate`, `fixture-plan`, and `fixture-verify`.
- The no-real-apply golden checks for forbidden command and implementation markers.

## Explicit Non-Goals

- No live file patcher.
- No real apply transaction runner.
- No rollback executor.
- No target install/repair/upgrade/rollback/uninstall apply behavior.
- No branch, tag, or release mutation.
