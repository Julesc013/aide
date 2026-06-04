# AIDE-QUEUE-CLOSURE-02 Prompt

Rerank AIDE queue blockers after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was rechecked and accepted with notes.

Verify live repo truth before relying on handoff claims. Reconcile `AIDE-APPLY-02-scoped-transaction-executor-v0`, historical `AIDE-CHECK-APPLY-02`, `AIDE-APPLY-02-REPAIR-01`, and `AIDE-CHECK-APPLY-02-RECHECK-01`. Preserve historical NEEDS_REPAIR evidence but classify it as superseded when the recheck evidence supports that.

Create only queue-closure report, graph, status, evidence, and queue index artifacts. Do not implement code. Do not execute lifecycle apply planning. Do not perform install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Select exactly one next safe WorkUnit batch. Prefer stale or contradictory queue/task status repair before apply lifecycle planning when current-task truth is unreliable.
