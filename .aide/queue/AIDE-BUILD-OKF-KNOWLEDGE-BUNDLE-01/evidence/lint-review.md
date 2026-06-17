# Lint Review

Command:

```bat
py -3 .aide/scripts/aide_lite.py okf lint
```

Observed result:

- lint status: `PASS_WITH_WARNINGS`
- broken links: `0`
- orphan pages: `0`
- missing source refs: `0`
- missing evidence refs: `0`
- stale context findings: `1`
- overclaiming findings: `0`
- authority boundary findings: `0`

The stale latest-task-packet finding is expected and non-blocking because queue truth is canonical.
