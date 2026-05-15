# Remaining Risks

- Q36-Q48, QCHECK-04, QFIX-04, QFIX-05, QFIX-06, and QFIX-07 remain
  `needs_review`; this is a policy review gate, not an active failure.
- Raw `.aide/scripts/tests` discovery passes but remains long at roughly
  9 minutes on this machine.
- Export pack provenance remains `DIRTY_SOURCE_RECORDED`, which is accepted by
  current pack-status but should be regenerated in a future clean release pass
  if exact source-commit provenance is required.
- Changelog preview reports 15 malformed historical commits; these are
  preserved history and not rewritten.
- Dominium has not yet been mutated or preflighted; Q49 must run from the
  Dominium repository with its own evidence.
