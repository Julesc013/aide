# Lint Review

Result: `ACCEPTED_WITH_WARNINGS`.

`okf lint` reports:

- broken links: `0`
- orphan pages: `0`
- missing source refs: `0`
- missing evidence refs: `0`
- stale context findings: `1`
- overclaiming findings: `0`
- authority boundary findings: `0`

The stale context finding is `.aide/context/latest-task-packet.md` lagging live queue truth. It is non-blocking because `.aide/queue/index.yaml` and task-local source chain evidence were used as authority.

Broken links and orphan pages remain warning-class unless they indicate source-traceability loss, authority overclaiming, or missing required pages.
