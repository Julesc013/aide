# Remaining Risks

- Q29 is not implemented.
- Q29 status is `blocked`, not `needs_review`.
- Q27 is blocked and its required commit discipline and WorkUnit recovery
  outputs are absent.
- Q28 is blocked and its required Git workflow policy and report-only detection
  outputs are absent.
- Current AIDE Lite validation fails before Q29.
- Current export pack checksum validation fails before Q29.
- The available `python3` is Python 3.9.13 and cannot run existing tests that
  require `Path.write_text(..., newline=...)`.
- No Git helper policy, helper commands, helper plan, fixture tests, docs,
  golden tasks, or export-pack integration were added.
- GitHub branch protection, CI checks, remote push behavior, and release
  automation remain future work.

## Recommended Next Action

Repair Q25 pack/local-state baseline, implement Q27, then implement Q28. Reopen
Q29 after Q28 reaches review with required outputs present.
