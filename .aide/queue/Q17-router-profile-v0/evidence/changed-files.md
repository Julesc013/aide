# Q17 Changed Files

## Queue Packet And Evidence

- `.aide/queue/index.yaml`
- `.aide/queue/Q17-router-profile-v0/task.yaml`
- `.aide/queue/Q17-router-profile-v0/ExecPlan.md`
- `.aide/queue/Q17-router-profile-v0/prompt.md`
- `.aide/queue/Q17-router-profile-v0/status.yaml`
- `.aide/queue/Q17-router-profile-v0/evidence/changed-files.md`
- `.aide/queue/Q17-router-profile-v0/evidence/validation.md`
- `.aide/queue/Q17-router-profile-v0/evidence/router-profile-report.md`
- `.aide/queue/Q17-router-profile-v0/evidence/route-decision-report.md`
- `.aide/queue/Q17-router-profile-v0/evidence/safety-boundary.md`
- `.aide/queue/Q17-router-profile-v0/evidence/remaining-risks.md`

## Routing Policy, Model Registry, And Artifacts

- `.aide/policies/routing.yaml`
- `.aide/models/README.md`
- `.aide/models/providers.yaml`
- `.aide/models/capabilities.yaml`
- `.aide/models/routes.yaml`
- `.aide/models/hard-floors.yaml`
- `.aide/models/fallback.yaml`
- `.aide/routing/README.md`
- `.aide/routing/route-decision.schema.json`
- `.aide/routing/latest-route-decision.json`
- `.aide/routing/latest-route-decision.md`
- `.aide/routing/examples/deterministic-estimate.json`
- `.aide/routing/examples/context-compiler.json`
- `.aide/routing/examples/evidence-review.json`
- `.aide/routing/examples/architecture-decision.json`
- `.aide/routing/examples/security-review.json`
- `.aide/routing/examples/self-modification.json`
- `.aide/routing/examples/golden-task-failure.json`

## AIDE Lite Implementation And Tests

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_router_profile.py`

## Generated Compact Context, Review, Ledger, And Controller Artifacts

- `.aide/context/repo-snapshot.json`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`
- `.aide/controller/outcome-ledger.jsonl`
- `.aide/controller/latest-outcome-report.md`
- `.aide/controller/latest-recommendations.md`

## Prompt, Memory, Catalog, And Root Documentation

- `.aide/commands/catalog.yaml`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/README.md`
- `docs/reference/aide-lite.md`
- `docs/reference/router-profile-v0.md`
- `docs/roadmap/queue-roadmap.md`

## Scope Notes

- Q17 did not edit provider adapters, Gateway, Runtime, Service, Commander, UI,
  Mobile, MCP/A2A, host/app implementation paths, secrets, `.env`,
  `.aide.local`, or raw prompt logs.
- `.aide/verification/latest-verification-report.md` and
  `.aide/evals/runs/latest-golden-tasks.*` were used during validation but were
  restored when command runs dirtied them outside Q17's allowed output set.
