# Reconciliation Report

## Stale State Found

The QCHECK audit found a working but unreviewed Q09-Q20 token-survival
foundation:

- Q09-Q20 existed, ran locally, and had evidence, but remained `needs_review`.
- `.aide/profile.yaml` still described Q09 as current focus.
- `scripts/aide self-check` still recommended Q09 review.
- Q18 `task.yaml` said `running` while status/index said `needs_review`.
- `.aide/scripts/tests` standard unittest discovery failed, even though direct
  test-file execution passed.

## Reconciled In This Step

- Q09-Q20 received task-local `evidence/review.md` files with
  `PASS_WITH_NOTES` decisions.
- Q09-Q20 `status.yaml` files now use `status: passed` and
  `review_gate.status: passed_with_notes`.
- `.aide/queue/index.yaml` now marks Q09-Q20 as `passed`.
- Q18 task/status/index drift is fixed.

## Intentionally Preserved Warnings

- Token estimates remain chars/4 approximations, not provider billing truth.
- Golden tasks prove AIDE substrate behavior, not arbitrary coding-task quality.
- Gateway and provider surfaces remain local/report-only or offline metadata.
- QFIX-02 owns `.aide/scripts/tests` discovery and runner cleanup.
- Generated manifest source fingerprint drift remains reported by Harness.

## Current Trusted Baseline

After Q09-Q20 reconciliation, the trusted token-survival foundation includes:

- AIDE Lite compact packet helper
- Context compiler metadata packets
- Verifier v0
- Evidence review packets
- Estimated token ledger and savings report
- Golden tasks v0
- Advisory outcome controller
- Advisory router profile
- Cache/local-state boundary
- Local/report-only Gateway skeleton
- Offline provider-adapter metadata

This is still pre-product and no-call. It is a foundation for QFIX-02 and
future Q21+ cross-repo use, not live provider/runtime readiness.

## Why QFIX-02 Is Next

The main remaining operational defect is test discovery. Future agents should
be able to run one predictable validation command without knowing that direct
test-file execution works while `unittest discover -s .aide/scripts/tests -t .`
fails. QFIX-02 should repair that before Q21 export/import work.
