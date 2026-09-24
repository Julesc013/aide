# Target-Policy Source Checkpoint

## Exact Source

- `core/runtime/integration_broker/github_target_policy.py` SHA-256:
  `ed2d5e6ae5a03c3e53e5e019ca972c67132367ec404807bb6dc035b515e37bd6`.
- `core/runtime/integration_broker/github_checks.py` SHA-256:
  `e13c1e2a77ad214d8edadfba9a2369cfa0f883cba526d5301db2ad77e3dcef05`.
- `core/runtime/integration_broker/pr_observation.py` SHA-256:
  `ac37b9990a1c8b92e3285a77195c77968614407d9c99147e8dc191372d5c2e39`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py` SHA-256:
  `40ff3189bcbabd1a021dda0e1784fa67deed4d00c6d2758c148ba49e4b480201`.
- `.aide/scripts/tests/test_continuous_worker_pr_observation.py` SHA-256:
  `6b35b1b3dffe501cdd0f840abaf9fc6e0ef0c336623724f7e4a6dcecb4cc5ece`.
- `.aide/scripts/tests/test_continuous_worker_provider_bridge.py` SHA-256:
  `7cf1e4c67bf9b4e17d0cae8113f5eaa15ff91f39af5cf2d9a3f55145ae815ac5`.

## Exact Review Inputs

- Desired policy SHA-256:
  `c516b0e8f655870dd3123ce6a175a2108dbe76a8d8a4e4cfda7be90fbfb05ff9`.
- Current observation SHA-256:
  `020650ae5932c672313248a4be57011b1e75046fed19e0c15e99cad095f9f75b`.
- Blocked review plan SHA-256:
  `54a18d662e6bc397eba1d6ae7dd66c99a29e42e47a1dfd8b741e0165590d7bbb`.
- Policy digest:
  `c79b62b9fc888aa50600334e3b7108addc91f543b4ea7e3e4505d0a8aef636c9`.
- Observation digest:
  `a1261592a0d53ac3ded981a19e32b0b323f085da45cf041893c76078b767c86a`.
- Plan digest:
  `a754af93595c26612edc13d52456e0d7ef64b07120e639001a05a91b1b3d3655`.

## Result

The implementation and local fixtures pass. The live plan is `blocked`, has
zero operations, and is not authorized for apply. Exact broker principal and
workflow/check identities are unresolved. No workflow, setting, credential,
branch, pull request, merge, tag, release, or hosted race was changed or run.

Both independent `REQUEST_CHANGES` rounds are retained. This follow-up
checkpoint binds repository id `1192621212`, explicit effective-rule and
classic-protection records, a complete `update` rule body, distinct
owner/broker identities, and exact local workflow/check run provenance. It
does not emit the unavailable required-workflow operation or claim exact source
binding as server-enforced. A superseding independent review remains required
before any effect packet.
