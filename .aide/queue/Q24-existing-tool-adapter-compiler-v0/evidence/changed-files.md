# Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml`
- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/task.yaml`
- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/ExecPlan.md`
- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/prompt.md`
- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/status.yaml`
- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/evidence/**`

## Adapter Policy, Targets, Templates, And Catalogs

- `.aide/policies/adapters.yaml`
- `.aide/adapters/catalog.yaml`
- `.aide/adapters/targets.yaml`
- `.aide/adapters/templates/AGENTS.md.template`
- `.aide/adapters/templates/CLAUDE.md.template`
- `.aide/adapters/templates/aider.conf.yml.template`
- `.aide/adapters/templates/clinerules.template`
- `.aide/adapters/templates/continue-checks.template.md`
- `.aide/adapters/templates/cursor-rule.template.md`
- `.aide/adapters/templates/windsurf-rule.template.md`
- `.aide/commands/catalog.yaml`

## AIDE Lite Implementation And Tests

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_adapter_compiler.py`

## Generated Adapter Outputs

- `.aide/generated/adapters/AGENTS.md`
- `.aide/generated/adapters/CLAUDE.md`
- `.aide/generated/adapters/aider.conf.yml`
- `.aide/generated/adapters/clinerules`
- `.aide/generated/adapters/continue-checks/aide-token-survival.md`
- `.aide/generated/adapters/cursor-rules/aide-token-survival.mdc`
- `.aide/generated/adapters/windsurf-rules/aide-token-survival.md`
- `.aide/generated/adapters/manifest.json`
- `.aide/generated/adapters/drift-report.md`

## Managed Root Guidance

- `AGENTS.md`

Only the Q24 managed adapter section was refreshed. Manual content outside the
managed section was preserved.

## Portable Pack Refresh

- `.aide/export/aide-lite-pack-v0/**`

The pack was refreshed so future target repos receive adapter policy, target
definitions, and templates. Generated adapter preview outputs are not copied as
target truth.

## Prompt And Generated Context Artifacts

- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/context/latest-task-packet.md`

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/README.md`
- `docs/reference/existing-tool-adapter-compiler-v0.md`
- `docs/roadmap/queue-roadmap.md`
- `docs/roadmap/reboot-roadmap.md`

## Existing Baseline Drift Preserved

- `.aide/export/aide-lite-pack-v0/manifest.yaml`
- `.aide/export/aide-lite-pack-v0/checksums.json`

These generated pack files were already modified at Q24 start after a prior
export-pack refresh. Q24 intentionally refreshed them again to include adapter
templates and current portable docs.
