# A2A Agent Card Contract Repair Report

`AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` repairs the eight material findings from `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`.

## Repaired

- External A2A version pins are explicit: specification `1.0.0`, protocol `1.0`.
- The official AgentCard fixture contains only A2A 1.0 fields.
- `supportedInterfaces` contains one non-live `.invalid` HTTPS JSON-RPC fixture interface.
- Top-level legacy `url` is absent.
- `provider` is omitted from the default fixture.
- Legacy extended-card fields and unsupported `stateTransitionHistory` are absent.
- Official `skills` is empty.
- Four candidate skills remain in outer AIDE metadata with `implemented: false` and `callable: false`.

## Boundary

No endpoint, discovery publication, registration, authentication, authorization, task delegation, worker, provider/model/network call, host integration, runtime, PatchTransaction apply, branch/worktree automation, GitHub mutation, release, promotion, or target mutation was implemented.
