# Trust And Authorization Contract v0 Check Report

- result: PASS_WITH_WARNINGS
- checked_capability: trust_and_authorization_contract_v0
- material_finding_count: 0
- missing_evidence: 0
- assertion_count: 12
- recommended_next_task: AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

The check verified stable `aide://` refs, no embedded credential or secret-like
values, exact implementation digest binding, authority-record separation, scope
and delegation fail-closed coverage, runtime and transaction approval
separation, complete refusal-code coverage, schema/projection alignment,
deterministic projection bytes, and truthful projection-only boundaries.
