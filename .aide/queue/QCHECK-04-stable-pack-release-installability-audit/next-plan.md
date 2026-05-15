# Next Plan

## Decision

Next: `Q49 - Dominium Fresh Install Preflight`.

Parallel allowed after QCHECK-04 review: `Q54 - Eureka Fresh Upgrade Preflight`.

Recommended order:

1. Dominium Q49.
2. Dominium Q50-Q53.
3. Eureka Q54-Q61.

Parallel Dominium Q49 and Eureka Q54 can be considered only if the operator accepts the warnings in this audit and keeps both tasks preflight-only.

## Why Q49 Is Next

Q47 and Q48 made the pack locally downloadable, checksum-backed, and draft-release-ready without publication. QCHECK-04 confirms the local bundle can be safely used for preflight with no-apply lifecycle models and target-state preservation. Dominium is the next planned fresh-install target and should validate the handoff before any broader publication or upgrade claim.

## Q49 Acceptance Guardrails

- Do not mutate Dominium outside Q49 allowed preflight artifacts.
- Do not install by raw copy.
- Preserve Dominium target-specific state.
- Treat local state/secrets/unsupported schemas as blockers/manual review.
- Run install/repair/upgrade/rollback/uninstall dry-run validation only.
- Record whether Dominium is installable from the local Q47 bundle.
