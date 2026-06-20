# Registry, Fixture, And Conformance Review

Registry projection checks found the projected diagnostic and refusal records match native records for the projected subset, but the build does not explicitly disclose diagnostic/refusal truncation in the omission summary.

Negative fixtures are not independently replayable as standalone invalid payloads or deterministic patches. They contain production-generated metadata, expected error text, and invalid payload hashes, but not the invalid payload or a replayable mutation description.

Conformance results are not independently evidenced per expectation. All 20 expectations point to the aggregate validation report, so individual expectations such as no-network, no-worker, event correlation, evidence linkage, compatibility, and unsupported-operation refusal are overstated as independently proven by the build.
