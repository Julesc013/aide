# Prompt

Perform the acceptance review for `AIDE-ACCEPT-CONTRACT-ENVELOPE-01`.

Review:

- `AIDE-BUILD-CONTRACT-ENVELOPE-01`
- `AIDE-CHECK-CONTRACT-ENVELOPE-01`
- `AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01`
- `AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01`

Accept only the minimal contract envelope capability if validation proves:

- schema runtime loading is real
- minimal schema subset validation is real
- helper/schema alignment is real
- lifecycle fixture report compatibility is preserved
- projections are additive
- unknown optional fields are tolerated
- unknown required capabilities fail closed
- no forbidden operation or unsupported readiness capability is introduced

Do not build EvidencePacket, WorkUnit, TestJob, Test Broker, Service,
Commander, provider, branch/worktree, target apply, active apply, rollback
execution, release, promotion, network, Gateway, GitHub, or model/provider
behavior.

Stop at `needs_review`.
