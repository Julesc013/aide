# Adapter Compiler Report

## Summary

Q24 implements a deterministic, standard-library AIDE Lite adapter compiler for
existing coding-tool guidance. It compiles from repo-local AIDE policy,
prompts, context discipline, verification guidance, evidence workflow, and
local-state boundaries into concise tool-specific templates.

The compiler is not a runtime integration. It makes no provider calls, model
calls, network calls, Gateway forwarding calls, IDE extension calls, or tool API
calls.

## Policy

- Path: `.aide/policies/adapters.yaml`
- Status: implemented and awaiting review
- Operating mode:
  - `template_compiler_only`
  - `generated_or_preview_outputs`
  - `no_tool_runtime_calls`
  - `no_provider_calls`
- Generated outputs are downstream guidance, not canonical truth.
- Managed sections are required when root/tool files are written.
- Preview-only output is required when writing a real tool file would be risky.

## Targets

- Path: `.aide/adapters/targets.yaml`
- Rendered targets:
  - `codex_agents_md`: `AGENTS.md`, managed section, enabled by default.
  - `claude_code`: `CLAUDE.md`, preview only.
  - `aider`: `.aider.conf.yml`, preview only.
  - `cline`: `.clinerules`, preview only.
  - `continue`: `.continue/checks/aide-token-survival.md`, preview only.
  - `cursor`: `.cursor/rules/aide-token-survival.mdc`, preview only.
  - `windsurf`: `.windsurf/rules/aide-token-survival.md`, preview only.
  - `vscode_optional`: `.vscode/tasks.json`, preview-only target definition,
    disabled and not rendered in Q24.

## Templates

- `.aide/adapters/templates/AGENTS.md.template`
- `.aide/adapters/templates/CLAUDE.md.template`
- `.aide/adapters/templates/aider.conf.yml.template`
- `.aide/adapters/templates/clinerules.template`
- `.aide/adapters/templates/continue-checks.template.md`
- `.aide/adapters/templates/cursor-rule.template.md`
- `.aide/adapters/templates/windsurf-rule.template.md`

Each template is compact and directs the target tool toward:

- `.aide/context/latest-task-packet.md`;
- compact repo/path/line references instead of whole-history prompts;
- AIDE Lite validation commands;
- evidence and review gates;
- `.aide.local/` local-state boundaries;
- no secrets, raw prompts, raw responses, provider keys, or generated cache
  blobs in committed files.

## Commands

Implemented in `.aide/scripts/aide_lite.py`:

- `adapter list`
- `adapter render`
- `adapter preview`
- `adapter validate`
- `adapter drift`
- `adapter generate`
- `adapt` as a deterministic shortcut for the safe `AGENTS.md` managed section.

## Generated Outputs

- Manifest: `.aide/generated/adapters/manifest.json`
- Drift report: `.aide/generated/adapters/drift-report.md`
- Rendered output count: 7
- Root/tool files written: only the managed Q24 section in `AGENTS.md`
- Preview-only targets written to root/tool paths: none

## Limitations

- Q24 does not prove existing tools will read the generated guidance.
- Original Q24 implementation predated the real target-pilot evidence. A later
  post-pilot refresh inspected sibling repos read-only and found:
  - Eureka `EUREKA-AIDE-PILOT-01`: PASS import pilot, status `needs_review`,
    948 approximate-token task packet versus 68,647 approximate-token baseline.
  - Dominium `DOMINIUM-AIDE-PILOT-01`: PASS_WITH_WARNINGS import pilot, status
    `needs_review`, 1,087 approximate-token task packet versus 110,115
    approximate-token doctrine-heavy baseline.
- Those pilots prove target packet reduction, not that every generated adapter
  output has been used successfully by each external tool.
- Non-AGENTS outputs remain preview-only until reviewed target-repo policy
  allows writing them.
- No live tool, provider, model, network, Gateway, IDE extension, MCP/A2A,
  runtime, UI, Commander, or autonomous behavior is implemented.
