# Q37 Changed Files

## Queue Packet And Evidence

- `.aide/queue/Q37-repo-intelligence-index-v0/task.yaml`
- `.aide/queue/Q37-repo-intelligence-index-v0/ExecPlan.md`
- `.aide/queue/Q37-repo-intelligence-index-v0/prompt.md`
- `.aide/queue/Q37-repo-intelligence-index-v0/status.yaml`
- `.aide/queue/Q37-repo-intelligence-index-v0/evidence/*.md`
- `.aide/queue/index.yaml`

## Policies And Schemas

- `.aide/policies/repo-intelligence.yaml`
- `.aide/policies/file-classification.yaml`
- `.aide/policies/ownership-map.yaml`
- `.aide/policies/dependency-map.yaml`
- `.aide/policies/test-map.yaml`
- `.aide/policies/doc-link-map.yaml`
- `.aide/repo/*.schema.json`
- `.aide/repo/README.md`

## Command And Tests

- `.aide/scripts/aide_lite.py`: added `repo inventory`, `repo classify`,
  `repo validate`, `repo status`, `repo explain-file`, `repo docs`,
  `repo tests`, and `repo deps`.
- `.aide/scripts/tests/test_q37_repo_intelligence.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/evals/golden-tasks/repo_*_golden/**`
- `.aide/evals/golden-tasks/file_classification_policy_golden/**`

## Generated Repo Intelligence

- `.aide/repo/file-inventory.json`
- `.aide/repo/ownership-map.json`
- `.aide/repo/dependency-map.json`
- `.aide/repo/test-map.json`
- `.aide/repo/doc-link-map.json`
- `.aide/repo/generated-map.json`
- `.aide/repo/orphan-candidates.json`
- `.aide/repo/latest-repo-intelligence.md`

## Documentation And Context

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `.aide/commands/catalog.yaml`
- `docs/reference/repo-intelligence-index.md`
- `docs/reference/intent-compiler.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `docs/reference/README.md`
- `.aide/context/latest-task-packet.md`

## Export Pack

- `.aide/export/aide-lite-pack-v0/**`: regenerated to include portable Q37
  policies, schemas, docs, tests, and golden tasks while excluding
  source-generated `.aide/repo/*.json` outputs.
