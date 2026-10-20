### Remaining risks and deliberate limits

- **POSIX coordination is cooperative:** descriptor/preimage checks do not contain arbitrary same-user or outer-client writers. The selected profile requires one mutation owner.
- **Uncertain rename gaps:** process termination can leave the original backup and private stage. Explicit reconciliation is required; tests establish preservation/refusal, not automatic recovery of every crash.
- **Rollback:** changed payload-path sets safely refuse automatic downgrade. Same-path rollback and verified detach/predecessor reinstall remain distinct supported observations.
- **Release remains separate:** no versioned Lite 1.2 archive, new published support profile or acquired-byte acceptance is established here. The current stable builder still emits Windows-only candidate metadata and needs its own bounded correction with historical identities preserved.
- **Broader work remains open:** outer-client containment, actual host/downstream daily use, full usage accounting, legacy native ports and separately delivered products retain their existing owners and gates. Unknown usage remains unknown.
- **Git effects can stop partially:** the controller retains actual ref/effect receipts and refuses blind retry; fresh contributor changes, protection or uncertain push results require reconciliation. Other refs and the important remote qualification checkpoint are preserved.

These limits do not block acceptance of the exact observed development lifecycle. [Integration effect](integration-effect.json), [report](../REPORT.md) and [governing review gates](../../../policies/review-gates.yaml) define the bounded remaining transaction.
