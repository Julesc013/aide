# Protocol And OKF Review

The Reconciler read OKF, ReferenceID, and EventRecord reports as source evidence.

Findings recorded:

- `stale_generated_report`: OKF build/validation reports still recommend `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`, while the accepted OKF gate recommends `AIDE-BUILD-RECONCILER-REPORTS-01`.
- `source_hash_gap`: OKF concept pages contain source hashes for `.aide/queue/index.yaml` from an earlier projection.

These are reported as drift only. The task does not refresh OKF pages or mutate protocol reports.
