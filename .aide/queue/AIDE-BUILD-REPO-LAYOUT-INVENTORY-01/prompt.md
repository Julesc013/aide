# Prompt: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01

Proceed with Track B only.

Build a report-only repository layout inventory for the current AIDE repo.
Start from live `.aide/queue/` truth and the existing root authority contract.

Inspect:

- current `.aide` immediate subtrees;
- current `core` immediate subtrees;
- duplicate naming across root, `.aide`, and `core`;
- `.aide/reports` top-level file and directory shape;
- build/check/accept report suffix inconsistencies;
- hardcoded flat report path assumptions in code, docs, queue evidence, and
  planning logs.

Write:

- `.aide/reports/repo-layout/inventory.json`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.json`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`

Do not generate a rationalization/apply prompt until the design is reviewed.
Do not move, delete, rename, rewrite, create roots, restructure `.aide/reports`,
edit generated OKF pages, promote generated outputs, mutate branches, mutate
target repos, call providers/models/network services, or implement Track A
protocol features.

Stop at `needs_review`.
