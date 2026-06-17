# Repository Layout Recommendations

- task_id: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01
- report_only: true
- no_apply: true
- rationalization_prompt_generated: false

## Recommendations

1. Keep `.aide/reports` flat for now.

   The inventory found 365 flat check/accept report path references across 156
   files. A rewrite would affect core helpers, OKF/Reconciler/CapabilityManifest
   projections, queue task packets, task evidence, PLANS, IMPLEMENT, and
   DOCUMENTATION. Build a report index before proposing migration.

2. Keep `core/protocol` flat for now.

   The directory has 10 tracked files and still maps cleanly to the current
   protocol-helper layer. Do not split it into tiny packages until
   ConformanceProfile, PatchTransaction, AdapterManifest, or ContextPack creates
   real import pressure.

3. Treat duplicate names as authority boundaries, not errors.

   `.aide` and `core` duplicate names such as `protocol`, `knowledge`,
   `providers`, `gateway`, `compat`, `apply`, and `tests`. That can be correct:
   `.aide` owns policy/state/schemas/reports/evidence, while `core` owns helper
   implementation.

4. Classify tracked `.aide/tmp` files before cleanup.

   They appear to be WorkUnit CLI mutation fixture inputs. Do not rename or move
   them until a fate map determines whether they belong in fixtures,
   `.aide/examples`, or task-local evidence.

5. Do not create top-level `tools`, `tests`, `examples`, or `archive` yet.

   `.aide` already contains `tools`, `tests`, and `examples` subtrees, and the
   root authority policy marks top-level roots as add-only candidates. A design
   task must prove why existing roots cannot express the authority.

## Recommended Next Tasks

1. `AIDE-CHECK-REPO-LAYOUT-INVENTORY-01`
2. `AIDE-ACCEPT-REPO-LAYOUT-INVENTORY-01`
3. `AIDE-BUILD-REPORT-INDEX-01`
4. `AIDE-STRUCTURE-02-status-doc-sync`
5. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`

## Deferred Prompt

No rationalization or apply prompt was generated. Generate one only after the
layout inventory is checked and accepted.
