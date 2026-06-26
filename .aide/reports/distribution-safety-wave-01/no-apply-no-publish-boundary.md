# No-Apply And No-Publish Boundary

The wave starts from accepted metadata objects and remains no-apply/no-publish until later reviewed queue items explicitly change authority.

Forbidden by default:

- install apply to real targets
- update apply to real targets
- migration apply to real targets
- rollback apply to real targets
- uninstall apply to real targets
- target repository mutation
- ScreenSave mutation
- Eureka mutation
- Dominium mutation
- source repo apply outside an active queue item
- release archive creation in this wave-controller task
- Git tags
- GitHub Releases
- uploads
- public release publication
- provider/model/network calls
- live A2A delegation
- branch/worktree automation
- runtime, Workbench, Commander, Omnigent, worker execution, PreviewSession, DevelopmentTransaction apply, or PatchTransaction apply

Allowed in this wave-controller task:

- planning records
- dependency and responsibility reports
- stop-condition and repair-routing matrices
- validation matrix
- next-task prompt for `AIDE-BUILD-INSTALL-RECORD-V0-01`
