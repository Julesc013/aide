# Remaining Risks

- Q36-Q48, QCHECK-04, and QFIX-06 remain review-gated as `needs_review`; this remediation does not self-approve them.
- Raw `.aide/scripts/tests` discovery now passes, but it is still expensive at roughly 8.5 minutes on this machine.
- Export pack provenance records `DIRTY_SOURCE_RECORDED` because pack/release artifacts were regenerated before this remediation commit.
- Changelog preview still reports legacy malformed commit messages from older history; this is classified as historical/generated evidence, not a QFIX-06 blocker.
- Q49 Dominium work was not started and should not start until the operator accepts the checkpoint/remediation review gates.
- No public release was created; Q47/Q48 remain local bundle/draft only.
