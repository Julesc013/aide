# Boundary Confirmation

Allowed paths used:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic status/validation report refreshes

Protected paths preserved:

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- release roots
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply implementation files
- rollback/uninstall implementation files
- scoped transaction executor implementation files
- managed-section implementation files
- rollback record files
- generated lifecycle fixture plans
- static fixture target files
- `core/**`

Forbidden operations preserved:

- install apply
- upgrade apply
- lifecycle repair apply
- rollback apply
- rollback execution
- uninstall apply
- uninstall execution
- lifecycle apply
- scoped transaction apply against fixture targets
- fixture target mutation through apply
- active repo scoped apply mutation
- target repo mutation
- branch/worktree mutation
- merge
- push
- promotion
- release publication
- GitHub mutation
- provider/model calls
- Gateway calls
- network calls
- broad active-repo apply

Required boundary wording:

- rollback-record-reviewed
- rollback-compatible
- rollback record
- inverse operation
- precondition
- stop condition
- manual preservation
- protected path
- dry-run
- report-only
- managed section
- preimage
- postimage
- active repo
- target repo
- review gate
- needs_review
- production-ready and release-ready remain prohibited claims

Capability reality result:

- review-gated rollback-compatible record checkpoint only
- no production-ready or release-ready claim
