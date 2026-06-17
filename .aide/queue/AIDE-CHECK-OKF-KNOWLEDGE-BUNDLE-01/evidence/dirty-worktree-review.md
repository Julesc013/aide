# Dirty Worktree Review

Initial live worktree state at check start:

```text
## main...origin/main
```

No pre-existing uncommitted `.aide/intake` changes were present. The prompt-reported intake files had already been committed in live HEAD `744503c56d37c132410485aacee3c26347cd96c4`.

Generated report churn appeared after status and validation commands in:

- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-task-status.md`
- `.aide/reports/test-job/projection-report.md`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`

Those diffs were generated refresh noise outside the allowed check deliverables and were restored before this check task wrote artifacts.

After this check task added its queue index entry, `okf project --source current-repo` refreshed generated OKF page `source_hashes` for `.aide/queue/index.yaml`. Those `.aide/knowledge/okf/**` output diffs were also restored because this check is not authorized to update the OKF build output.

The check did not stage or commit unrelated intake or generated predecessor report changes.
