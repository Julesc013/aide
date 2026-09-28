# One-use API-set query controller source candidate

The task-owned controller and injected tests are
`h2_api_query_effect.py` and `h2_api_query_effect_tests.py`. The exact source,
test, reviewed adapter and retained inventory hashes are in
`h2-api-query-controller-source-manifest.json`, SHA-256
`04363b33bc55a41e0896497bf82d0a396ed12051699475d5eed667b368b7d025`.
Base task checkpoint: `214f74d2a7f07c3344ed0b29b17d41df41c11c38`.

The controller requires an exact 180-name retained inventory, source and
inventory hashes, a bounded `ApiSetQueryPlan`, OS build and fresh expiry. Its
exclusive request file is created in the approved shared D control root
before native backend construction. It fsyncs a reservation and each exact
pre-call intent, refuses a changed journal identity, writes a bounded result
to the managed retained output, and leaves the one-use control journal for
reconciliation. A consumed request ID cannot be replayed by this controller.

The first managed injected run, job `483fb0f3d4a243bfb09808b4d92dc74d`,
exited 1 because one test expected numeric order while the accepted plan sorts
names lexicographically. The test oracle was corrected. Later five-case job
`23215f8e96d147d780e52125b6d90b08` passed; the final seven-case source
job `b694c2accc0941fa9dc7f92a7f2c0281` passed in 12.443s with zero
failures, peak memory 28,844,032 bytes, scratch retired and reservation
released. Cases cover exact 180 calls and durable intents, no replay, bad
source/inventory/expiry/shape, unflushed reservation, wrong OS build,
mid-query refusal, unusable output and existing output preservation. All APIs were injected;
no actual `NativeApiSetQueryApi` was constructed.

Independent source review is pending. The future effect must freeze a fresh
request ID, 180-name list, current source and OS identities, a short expiry,
exact managed job/config hashes, and the D control/output paths. One admitted
effect may run only after an independent effect review. The controller runs as
a trusted ordinary maintainer process; this source does not establish
adversarial same-user journal protection, private host-byte provenance,
restricted loader behavior or worker activation. A completed query is only
one dependency of those later qualifications.
