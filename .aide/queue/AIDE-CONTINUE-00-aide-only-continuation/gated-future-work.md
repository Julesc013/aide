# Gated Future Work

| Category | Status | Ungate Condition |
|---|---|---|
| Target repo work | gated | Explicit target-local queue packet after AIDE Task OS records and reviewed pack evidence. |
| Target sync | gated | Reviewed source pack plus explicit target preflight authorization. |
| Transactional apply | gated | X-OS report-only layer, transaction safety policy, pre/post image hashes, rollback semantics, and validation evidence. |
| Branch/worktree apply | gated | Branch provenance records, transaction safety, and no-remote-push defaults. |
| Merge/push/promotion | gated | Current T0/T1/T2/T3 evidence, review packet, capability overclaim checks, branch provenance, and explicit promotion authorization. |
| Release publication | gated | Clean release bundle, CI/release gates, manual publication review, and explicit tag/upload authorization. |
| GitHub API mutation | gated | Future reviewed queue item that authorizes apply behavior and records dry-run/advisory evidence first. |
| Gateway/provider/model runtime | gated | Credential/redaction policy, no-call router proof, usage ledger, and explicit live-call authorization. |
| Install/repair/upgrade/rollback/uninstall apply | gated | Transaction engine, ownership ledger, preservation ledger, rollback records, fixture torture tests, and explicit apply phase. |
