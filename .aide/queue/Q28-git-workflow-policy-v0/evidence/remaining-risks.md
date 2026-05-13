# Remaining Risks

- Q28 is not implemented.
- Q28 status is `blocked`, not `needs_review`.
- Q27 is blocked and its required commit discipline and WorkUnit recovery
  outputs are absent.
- Current AIDE Lite validation fails before Q28.
- Current export pack checksum validation fails before Q28.
- The available `python3` is Python 3.9.13 and cannot run existing tests that
  require `Path.write_text(..., newline=...)`.
- No Git workflow policy, branch-role policy, promotion rules, sync policy,
  prune policy, project profiles, detection artifacts, AIDE Lite Git commands,
  golden tasks, tests, docs, or export-pack integration were added.
- Branch protection data remains unavailable without future GitHub API work.
- Q29 merge/land/promote helpers remain deferred.

## Recommended Next Action

Repair Q25 pack/local-state baseline, then implement Q27 commit discipline and
WorkUnit recovery. After Q27 reaches review with its required outputs present,
reopen Q28.
