# Next Task Prompt Seed

Task ID: `AIDE-APPLY-LIFECYCLE-PLAN-01`

Goal: Create a planning-only queue task that scopes future AIDE apply lifecycle work after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was accepted with notes. The task must inventory lifecycle surfaces, prerequisites, blockers, prohibited operations, allowed paths, validation needs, evidence requirements, and review gates. It must not implement or execute install apply, upgrade apply, repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Required starting facts: `AIDE-TASK-OS-STATUS-REPAIR-01` is review-gated; Task OS reports selected next WorkUnit as `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`; lifecycle apply authorization remains false.
