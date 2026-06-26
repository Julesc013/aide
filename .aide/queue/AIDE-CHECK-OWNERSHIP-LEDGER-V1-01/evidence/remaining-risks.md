# Remaining Risks

Five material risks block acceptance and downstream InstallRecord work:

- File-entry records are too compact for the requested install/update ownership
  truth boundary.
- Managed-section records lack marker/preimage/surrounding-content semantics.
- Q43 ownership migration has no helper, CLI surface, or fixtures.
- Collision/conflict behavior is not fail-closed.
- Fixture coverage does not directly exercise required downstream cases.

The next repair should close these findings without adding apply behavior or
starting InstallRecord.
