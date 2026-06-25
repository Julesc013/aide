# Delegation And Revocation

Delegation v0 is narrowing-only:

- no transitive delegation unless explicit;
- no scope widening;
- no capability widening;
- no expiry beyond source grant;
- revocation propagates through the recorded chain.

`RevocationRecord` records affected grants, admissions, delegations, authority,
reason, effective time, superseding refs, and evidence refs. This build does
not implement live revocation propagation.
