# Remaining Risks

## QFIX-02 Test Discovery

`py -3 -m unittest discover -s .aide/scripts/tests -t .` still fails because
the hidden `.aide` start directory is not importable under normal unittest
discovery. Direct AIDE Lite selftest passes, but future agents need the standard
discovery command repaired next.

## Substrate-Level Quality Only

Q09-Q20 are accepted with notes as the token-survival foundation. The verifier,
review packets, golden tasks, outcome controller, router, cache boundary,
Gateway skeleton, and provider metadata preserve AIDE substrate quality, but
they do not prove arbitrary coding-task correctness.

## Measurement Limits

Token accounting remains approximate (`chars/4`) and does not represent exact
tokenizer output, provider billing, cached-token billing, or real API usage
accounting.

## Cross-Repo Use Not Proven Yet

Q21 export/import and Eureka/Dominium pilots have not run. The current foundation
is local to this repo until those phases prove that compact AIDE packets and
policies can travel safely.

## No-Call Boundaries Remain

Gateway and provider surfaces are accepted only as local/report-only skeletons
and offline metadata. They still do not authorize provider calls, model calls,
Gateway forwarding, local model setup, runtime behavior, UI, MCP/A2A, or
autonomous execution.

## Legacy And Generated-State Warnings

- Q00-Q03, Q05, and Q06 retain earlier review-gate/raw-status nuance outside
  QFIX-01 scope.
- Generated managed-section manifest source fingerprint drift remains reported
  by Harness.
- Token ledger contains near-budget warnings for a small number of evidence or
  cache-report surfaces.

## Review Gate

QFIX-01 itself stops at `needs_review`. Future work should not proceed to Q21
until QFIX-01 is reviewed and QFIX-02 repairs test discovery.
