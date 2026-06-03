# Remaining Risks

## Review Risks

- `AIDE-CHECK-APPLY-02` has not yet been created or run.
- AIDE-APPLY-02 remains review-gated at `needs_review`; it is not accepted or production-ready.
- Apply mode is implemented only for explicit scoped plans. Review should inspect whether the path and output-record semantics are sufficient before any broader use.
- AIDE Lite Task OS current/wave/checkpoint surfaces still have stale historical guidance outside this task's scope.

## Capability Reality Risks

- The executor is implemented, tested, fixture-tested, report-backed, and review-gated only.
- It is not target-repo capable, install/upgrade/repair/rollback/uninstall capable, release-ready, production-ready, or broad active-repo apply capable.
- Generated scoped executor reports are evidence for the fixture and command surface, not acceptance of the executor.

## Deferred Surfaces

- install apply;
- upgrade apply;
- repair apply;
- rollback/uninstall apply;
- target repo mutation;
- branch/worktree mutation;
- merge;
- push;
- promotion;
- release publication;
- GitHub mutation;
- provider/model calls;
- Gateway calls;
- network calls;
- broad active-repo apply.
