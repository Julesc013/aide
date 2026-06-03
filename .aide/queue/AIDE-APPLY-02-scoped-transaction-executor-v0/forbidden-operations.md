# AIDE-APPLY-02 Forbidden Operations

The following operations are forbidden for this authorization task and for future AIDE-APPLY-02 implementation unless a later reviewed queue item explicitly authorizes them:

- scoped transaction executor implementation during `AIDE-APPLY-02-AUTHORIZE`;
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
- mutation outside explicit allowed paths;
- mutation without preimage hash checks;
- mutation without postimage verification;
- mutation without rollback-compatible record;
- mutation without evidence;
- self-promotion from review-gated to accepted or production-ready.

The future executor must remain a scoped transaction executor v0, not install/upgrade/repair/rollback/uninstall apply, not target-repo apply, and not release-ready behavior.
