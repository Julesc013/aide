# Explicit Non-Capabilities

Accepted UpdatePlan v1 does not provide:

- install apply
- update apply
- migration apply
- repair apply
- rollback apply
- uninstall apply
- target repository mutation
- target scan authority
- real project canary authority
- release archive creation
- public release readiness
- Git tag creation
- GitHub Release creation
- upload
- provider/model/network calls
- Workbench runtime
- Commander
- Omnigent
- branch/worktree automation
- DistributionApplyEngine behavior

Any future task that needs one of these capabilities must explicitly build, check, and accept that capability through the queue.
