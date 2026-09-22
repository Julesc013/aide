# Target-Policy Source Checkpoint

## Exact Source

- `core/runtime/integration_broker/github_target_policy.py` SHA-256:
  `75e61dbb5ce4f085b885da08616f9a19bf667ae1d4c50cfd834ecbf21fcca2d2`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py` SHA-256:
  `3ff68a757329e91564b8e69adf7a3b47d13d208d91973eaaf4fd0dda18860236`.

## Exact Review Inputs

- Desired policy SHA-256:
  `245a8d871301b255d9cbc0abfa3e7fde2e8ccfea0e7f0b88e01ebcbe149e8146`.
- Current observation SHA-256:
  `020650ae5932c672313248a4be57011b1e75046fed19e0c15e99cad095f9f75b`.
- Blocked review plan SHA-256:
  `a0aec7f8c4db5191167a662bbc2ca66a742c2ed498f80cfd2e1ea9a36c95773c`.
- Policy digest:
  `0c3c1ce858c4e70e0070074f66db31873c7a1f4b9aa820066f760678ed35ba89`.
- Observation digest:
  `a1261592a0d53ac3ded981a19e32b0b323f085da45cf041893c76078b767c86a`.
- Plan digest:
  `762da6e0de4359fcc1316529e9f715f075bac0e37f42e7a9ec2127f3b5469336`.

## Result

The implementation and local fixtures pass. The live plan is `blocked`, has
zero operations, and is not authorized for apply. Exact broker principal and
workflow/check identities are unresolved. No workflow, setting, credential,
branch, pull request, merge, tag, release, or hosted race was changed or run.

The first independent review is retained and requested changes. This repair
checkpoint binds repository id `1192621212`, explicit effective-rule and
classic-protection records, GitHub's exact `workflows` rule, a complete `update`
rule body, and distinct owner/broker identities. A superseding independent
review remains required before any effect packet.
