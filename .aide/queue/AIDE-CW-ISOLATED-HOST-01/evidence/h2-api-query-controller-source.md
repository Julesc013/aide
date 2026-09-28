# One-use API-set query controller source candidate

The task-owned controller and injected tests are
`h2_api_query_effect.py` and `h2_api_query_effect_tests.py`. The exact source,
test, reviewed adapter and retained inventory hashes are in
`h2-api-query-controller-source-manifest.json`, SHA-256
`3f5683ff85fd9fc440a74db9b07dd365f53de0a0256c8134799550144d359122`.
Base task checkpoint: `cb87591fe374caa45aa07d2dfbc0e72cdb4bc694`.

The controller requires an exact 180-name retained inventory, source and
inventory hashes, a bounded `ApiSetQueryPlan`, OS build and fresh expiry. Its
exclusive request file is created in the approved shared D control root
before native backend construction. It fsyncs a reservation and each exact
pre-call intent, refuses a changed journal identity, writes a bounded result
to the managed retained output, and leaves the one-use control journal for
reconciliation. A consumed request ID cannot be replayed by this controller.
The repaired controller reserves the exact final output name before backend
construction, stages a bounded result under a nonfinal name, fsyncs a terminal
PASS bound to its digest, then publishes and verifies the final result. A
failed publication retains the stage for reconciliation without native replay.

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

Independent `/root/native_os_build_review` returned REQUEST_CHANGES on
`cb87591f`: occupied output was discovered after the queries and success could
be published before a durable terminal PASS. Its exact verdict is preserved in
`h2-api-query-controller-review-cb87591f.md` and external D control custody.
The external review custody copy has SHA-256
`68e1a5a252c33b36b66229d92ac5d1d8a7e4aacc783f4b03fc4be74df93b5282`.
The repair has ten injected cases passing locally, including occupied-output
zero calls, short staged write, terminal fsync failure and publication
reconciliation. A managed postcommit run and independent rereview are pending.
The future effect must freeze a fresh
request ID, 180-name list, current source and OS identities, a short expiry,
exact managed job/config hashes, and the D control/output paths. One admitted
effect may run only after an independent effect review. The controller runs as
a trusted ordinary maintainer process; this source does not establish
adversarial same-user journal protection, private host-byte provenance,
restricted loader behavior or worker activation. A completed query is only
one dependency of those later qualifications.
