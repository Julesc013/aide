# Root Authority Map Evidence

## Sources

- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.md`
- `docs/planning/repository-structure/current-truth-and-root-authority-audit.md`
- `docs/reference/source-of-truth.md`
- `docs/reference/repo-intelligence-index.md`
- `docs/reference/root-recycling-framework.md`
- `docs/reference/refactor-control-plane.md`
- `docs/reference/move-salvage-path-aliases.md`

## Contract Outputs

- `.aide/policies/root-authority.yaml`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/root-authority-contracts.json`
- `.aide/reports/root-authority-contracts.md`
- `docs/planning/repository-structure/root-authority-contracts.md`
- `docs/planning/repository-structure/track-b-follow-up-prompts.md`

## Decision

The contract keeps the current top-level root model closed. Existing roots are
classified by authority, canonicality, risk, and mutation posture. Unresolved
roots are not moved; they are routed to follow-up Track B review tasks.

## Follow-Up Routing

1. `AIDE-STRUCTURE-02-status-doc-sync`
2. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`
3. `AIDE-STRUCTURE-04-dot-tool-roots-interop-policy`
4. `AIDE-STRUCTURE-05-tools-tests-examples-root-plan`
