# Root Authority Contracts Report

- task_id: AIDE-STRUCTURE-01-root-authority-contracts
- generated_at: 2026-06-18
- source_commit: 1865e3ab3eda
- dependency: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit
- implementation_class: contract_and_policy_docs_only
- file_moves: false
- file_deletes: false
- reference_rewrites: false
- path_aliases_or_shims: false
- new_top_level_roots: false
- generated_output_source_truth_promotion: false
- branch_mutation: false
- target_repo_mutation: false

## Outputs

- `.aide/policies/root-authority.yaml`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `docs/planning/repository-structure/root-authority-contracts.md`
- `docs/planning/repository-structure/track-b-follow-up-prompts.md`

## Root Authority Map

The root authority map is now expressed in
`.aide/policies/root-authority.yaml` and explained in
`governance/root-authority.md` and `docs/reference/repository-layout.md`.

The map preserves the Track B audit conclusion: AIDE needs root contracts and
follow-up no-apply planning before filesystem migration.

## Overlap Findings

1. `.aide` mixes canonical records with generated evidence and projections.
2. `core` and `.aide/protocol` split implementation helpers from schema truth.
3. `governance` and `.aide/policies` split human law from machine policy.
4. `docs` and `.aide/knowledge/okf` explain state but do not override queue or
   protocol truth.
5. `shared`, `platforms`, `research`, and `specs` need a fate map before any
   movement.
6. `.agents` and `.codex` need a dot-tool interop policy before expansion.
7. `tools`, `tests`, `examples`, and `archive` remain add-only candidates, not
   implied roots.

## Follow-Up Queue

Recommended next Track B tasks:

1. `AIDE-STRUCTURE-02-status-doc-sync`
2. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`
3. `AIDE-STRUCTURE-04-dot-tool-roots-interop-policy`
4. `AIDE-STRUCTURE-05-tools-tests-examples-root-plan`

## Boundary

This report is evidence for a review gate. It does not authorize structural
apply behavior, Track A protocol feature implementation, CapabilityManifest
acceptance, ConformanceProfile work, patch transactions, adapters, interop
exports, ContextPack v2, worker execution, Workbench, Commander, Service,
legacy bridges, provider/model calls, network calls, target-repo mutation,
branch mutation, release work, or production readiness claims.
