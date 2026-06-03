# AIDE-APPLY-02 Review Gate

Review gate: `queue_review_required`.

The future implementation must end at `needs_review` and hand off to `AIDE-CHECK-APPLY-02`.

## Stop Conditions

Stop and record a blocker if implementation requires:

- paths outside `allowed-paths.md`;
- mutation of protected paths;
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
- broad active-repo apply;
- broad deletes;
- broad moves;
- mutation without preimage hash checks;
- mutation without postimage verification;
- mutation without rollback-compatible record;
- mutation without evidence;
- self-promotion from review-gated to accepted or production-ready.

## Checkpoint Handoff

After implementation evidence is written, the next task is `AIDE-CHECK-APPLY-02`. That checkpoint must independently review scoped transaction executor safety, tests, evidence, capability reality, and preserved forbidden-operation boundaries.
