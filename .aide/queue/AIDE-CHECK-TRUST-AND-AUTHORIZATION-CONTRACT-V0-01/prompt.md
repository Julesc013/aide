# AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

Independent check-only.

Verify:

- stable AIDE refs;
- no embedded credentials;
- exact-digest admission;
- declaration/conformance/admission separation;
- policy/grant separation;
- no scope widening;
- delegation bounded;
- revocation propagation;
- expiry fail-closed;
- use-budget consistency;
- runtime approval distinct from transaction approval;
- unknown required feature fail-closed;
- schema/helper/projection alignment;
- deterministic serialization;
- complete negative fixtures;
- no enforcement runtime overclaim;
- no IAM/OIDC/secret implementation;
- focused and broad validation;
- scrubbed reports/evidence.

If findings remain, recommend exactly:

```text
AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-REPAIR-01
```

If pass, recommend exactly:

```text
AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```

Do not repair implementation in this task. Stop at `needs_review`.
