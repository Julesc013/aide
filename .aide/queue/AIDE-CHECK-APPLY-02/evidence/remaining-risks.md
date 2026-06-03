# Remaining Risks

## Safety Risks

- Symlink or reparse-point target escape is not explicitly rejected before read/write.
- Multi-operation apply can leave earlier writes in place if a later write or post-write verification fails.
- Apply mode is explicit and scoped, but it is not yet accepted for broader repository use.

## Review Risks

- The required example-plan validation command fails until the example hashes or example policy are repaired.
- Direct core output can persist a report missing `report_path`.
- Additional review is needed after repair before the executor can be accepted with notes.

## Lifecycle Risks

- The executor is not install apply, upgrade apply, repair apply, rollback/uninstall apply, target-repo apply, production-ready, release-ready, or broad active-repo apply.
- Queue closure implementation remains separate future work and must not self-authorize prohibited operations.

## Deferred Capabilities

- install apply
- upgrade apply
- repair apply
- rollback/uninstall apply
- target repo mutation
- branch/worktree mutation
- merge
- push
- promotion
- release publication
- GitHub mutation
- provider/model calls
- Gateway calls
- network calls
- broad active-repo apply
