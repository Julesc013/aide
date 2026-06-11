# Remaining Risks And Deferrals

## Remaining Risks

- The runner is intentionally limited to `install-managed-section` / `apply-temp`.
- The runner performs a full marker-bounded block replacement inside the temp workspace because the static expected postimage changes managed-section marker metadata as well as generated content.
- This does not generalize the existing scoped transaction executor or create active lifecycle apply behavior.

## Deferrals

- No service, Commander, provider adapter, plugin framework, branch/worktree allocator, test broker, checkpoint engine, or broad kernel schema suite was implemented.
- No rollback execution or uninstall execution was implemented.
- No target repository mutation, release behavior, GitHub mutation, provider/model calls, Gateway calls, or network calls were performed.
- Commit creation and commit-message validation are deferred until the operator asks for a commit.
- Independent review is deferred to `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`.
