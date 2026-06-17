# Lint Review

Result: `PASS_WITH_WARNINGS`.

`okf lint` reports:

- broken links: `0`
- orphan pages: `0`
- missing source refs: `0`
- missing evidence refs: `0`
- stale context findings: `1`
- overclaiming findings: `0`
- authority boundary findings: `0`

The one stale context finding is expected: `.aide/context/latest-task-packet.md` lags `.aide/queue/index.yaml`.

This is warning-class because live `.aide/queue/` truth was used for routing and the check did not rely on the stale task packet.
