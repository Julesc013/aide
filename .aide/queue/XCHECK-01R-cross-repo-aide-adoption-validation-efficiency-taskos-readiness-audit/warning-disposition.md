# Warning Disposition

| Warning | Classification | Disposition |
|---|---|---|
| AIDE Q36-Q48 remain `needs_review` | `assigned_next` | Human review required before acceptance/publication claims |
| QCHECK/QFIX packets remain `needs_review` | `assigned_next` | Review gate retained by policy |
| AIDE pack/release source commit is `2b2a00f...`, behind current HEAD | `assigned_next` | Future clean release-pack regeneration |
| AIDE raw unittest discovery is long, about 9 minutes in QFIX-07 | `deferred_non_blocking` | Address through X-TEST tiering/telemetry |
| Source AIDE lacks canonical test tiers | `assigned_next` | `X-TEST-00` |
| Source AIDE lacks async test telemetry summary | `assigned_next` | `X-TEST-02` after X-TEST-00 |
| Source AIDE lacks Task OS v0 schemas/policies | `assigned_next` | `X-OS-00` after X-TEST-00 |
| Dominium earlier AIDE baseline commit durability warnings | `expected_target_specific` | Later target work exists; do not repair from source audit |
| Dominium full CTest/full-gate debt | `blocking` | Blocks Dominium product/promotion work |
| Dominium POST-CONVERGE-11/12 product boot/projection blocked by RepoX | `blocking` | Run target RepoX/test-tier work before product boot |
| Dominium target-local Task OS/capability work not canonical AIDE source | `expected_target_specific` | Use as evidence only |
| Eureka Q58 AIDE eval WARN/FAIL and later full-suite ambiguity | `assigned_next` | `X-TEST-01` target validation tiering |
| Eureka `dev` is six commits ahead of `main` by local refs | `assigned_next` | Target branch provenance must be handled by target task |
| Eureka product proof is fixture/local only | `fixture_only` | Do not claim live/production support |
| Target adoption from prior AIDE pack | `assigned_next` | Future sync only after reviewed source pack |

Counts:

- harmless: 0
- fixture_only: 1
- expected_target_specific: 2
- expected_generated_state: 0
- deferred_non_blocking: 1
- assigned_next: 9
- blocking: 2
- unknown_needs_review: 0
