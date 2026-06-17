# Source Artifact Traceability Review

Status: `PASS_WITH_WARNINGS`

The Reconciler reports include source artifact references for the queue, accepted OKF outputs, protocol reports, ReferenceID/EventRecord projections, and evidence reports.

The traceability warning is the expected `source_hash_gap` finding: OKF source hashes for `.aide/queue/index.yaml` are stale. This check records that warning without refreshing OKF pages or mutating source artifacts.
