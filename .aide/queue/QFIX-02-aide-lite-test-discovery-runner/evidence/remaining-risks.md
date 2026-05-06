# Remaining Risks

## Non-Canonical Old Command Still Fails

`py -3 -m unittest discover -s .aide/scripts/tests -t .` still fails by design.
It is an invalid command shape for the hidden `.aide` start directory under a
repo-root top-level import rule. QFIX-02 documents the replacement rather than
turning `.aide/` into a Python package namespace.

## QFIX-02 Review Gate

QFIX-02 stops at `needs_review`. Q21 should wait for review.

## Cross-Repo Export Deferred

Q21 Cross-Repo Pack Export / Import v0 is still future work. QFIX-02 only makes
the local AIDE Lite validation runner obvious and repeatable.

## Validation Scope

The canonical test command is standard-library/internal-check based. It does
not prove arbitrary coding-task quality, exact token counts, provider billing,
live routing, or cross-repo portability by itself.

## Existing Foundation Warnings

- Q00-Q03, Q05, and Q06 retain earlier review-gate/raw-status nuance.
- Generated managed-section manifest source fingerprint drift remains reported
  by Harness.
- Token ledger near-budget warnings remain non-blocking warnings.

## No-Call Boundary

No provider calls, model calls, outbound network calls, Gateway forwarding,
Runtime behavior, UI, local model setup, secrets, `.aide.local/` contents, raw
prompts, or raw responses were introduced.
