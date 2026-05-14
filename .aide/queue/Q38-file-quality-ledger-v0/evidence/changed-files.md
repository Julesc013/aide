# Q38 Changed Files

## Queue And Evidence

- `.aide/queue/Q38-file-quality-ledger-v0/**` records the Q38 task packet,
  restartable ExecPlan, status, prompt copy, and review evidence.
- `.aide/queue/index.yaml` registers Q38 and marks it ready for review.

## Policies And Schemas

- `.aide/policies/file-quality.yaml` defines the advisory quality ledger policy.
- `.aide/policies/docs-consistency.yaml` defines stale-link and missing-doc
  warning rules.
- `.aide/policies/module-quality.yaml` defines large-file, mixed-purpose, and
  dependency-count heuristics.
- `.aide/policies/reuse-modularity.yaml` defines duplicate and repeated helper
  candidate heuristics.
- `.aide/quality/*.schema.json` and
  `.aide/reports/file-quality-ledger.schema.json` define the lightweight
  output shapes.

## AIDE Lite Commands

- `.aide/scripts/aide_lite.py` adds `quality ledger`, `quality validate`,
  `quality status`, `quality explain-file`, `quality docs`, `quality tests`,
  `quality modules`, and `quality reuse`.
- The same script now references the quality ledger from repo status,
  repo explain-file, intent refs, task packets, golden tasks, validation, and
  export-pack boundaries.
- `.aide/scripts/tests/test_q38_file_quality.py` covers Q38 ledger behavior,
  warnings, generated/evidence handling, local-state hard flags, and
  no-mutation behavior.

## Generated Quality Reports

- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`
- `.aide/reports/module-quality-report.md`
- `.aide/reports/docs-consistency-report.md`
- `.aide/reports/test-coverage-map.md`
- `.aide/reports/reuse-modularity-report.md`

## Golden Tasks

- `.aide/evals/golden-tasks/file_quality_policy_golden/**`
- `.aide/evals/golden-tasks/file_quality_ledger_schema_golden/**`
- `.aide/evals/golden-tasks/quality_ledger_generation_golden/**`
- `.aide/evals/golden-tasks/docs_consistency_report_golden/**`
- `.aide/evals/golden-tasks/test_coverage_map_golden/**`
- `.aide/evals/golden-tasks/reuse_modularity_report_golden/**`
- `.aide/evals/golden-tasks/quality_no_delete_recommendation_golden/**`
- `.aide/evals/golden-tasks/catalog.yaml`

## Documentation And Context

- `docs/reference/file-quality-ledger.md` documents Q38 usage and limits.
- `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`,
  `DOCUMENTATION.md`, `AGENTS.md`,
  `docs/reference/repo-intelligence-index.md`, and
  `docs/reference/cross-repo-pack-export-import.md` were updated compactly.
- `.aide/commands/catalog.yaml` documents the quality command surface.
- `.aide/context/latest-task-packet.md` was regenerated for
  Q39 Refactor Control Plane v0.
- `.aide/context/latest-review-packet.md` was regenerated for Q38 review.

## Export Pack

- `.aide/export/aide-lite-pack-v0/**` was regenerated to include portable Q38
  policies, schemas, docs, tests, golden tasks, and the updated AIDE Lite
  script.
- Source-generated quality reports are intentionally not exported as target
  truth.
