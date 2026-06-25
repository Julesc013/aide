# Next Task Prompt

```text
Create and process
AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01.

Repo truth outranks this prompt. This is an independent check-only task.
Do not repair implementation.

Verify:

- stable AIDE refs;
- no embedded credentials or secret values;
- exact-digest admission;
- installation/declaration/conformance/admission/authorization separation;
- policy/grant separation;
- no scope widening;
- delegation boundedness;
- revocation propagation modeling;
- expiry fail-closed;
- use-budget consistency;
- runtime approval distinct from transaction approval;
- unknown required feature fail-closed;
- schema/helper/projection alignment;
- deterministic serialization;
- complete negative fixtures and refusal-code coverage;
- no enforcement runtime overclaim;
- no IAM/OIDC/secret implementation;
- focused and broad validation;
- scrubbed reports/evidence.

If findings remain, recommend exactly:
AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-REPAIR-01.

If the check passes, recommend exactly:
AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01.

Stop at needs_review with complete evidence.
```
