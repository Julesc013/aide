# Adapter Compiler State

## Policy

Path: `.aide/policies/adapters.yaml`

The policy exists and declares:

- template compiler only
- generated or preview outputs
- no tool runtime calls
- no provider calls
- no model calls
- no network calls
- managed sections required for real target writes
- generated outputs are not canonical truth

## Targets

Path: `.aide/adapters/targets.yaml`

| Target | Output | Mode | Default | Risk |
| --- | --- | --- | --- | --- |
| Codex / AGENTS | `AGENTS.md` | managed section | enabled | low |
| Claude Code | `CLAUDE.md` | preview-only | enabled | medium |
| Aider | `.aider.conf.yml` | preview-only | enabled | medium |
| Cline | `.clinerules` | preview-only | enabled | medium |
| Continue | `.continue/checks/aide-token-survival.md` | preview-only | enabled | medium |
| Cursor | `.cursor/rules/aide-token-survival.mdc` | preview-only | enabled | medium |
| Windsurf | `.windsurf/rules/aide-token-survival.md` | preview-only | enabled | medium |
| VS Code optional | `.vscode/tasks.json` | preview-only | disabled | medium |

## Templates

Templates exist for:

- `AGENTS.md.template`
- `CLAUDE.md.template`
- `aider.conf.yml.template`
- `clinerules.template`
- `continue-checks.template.md`
- `cursor-rule.template.md`
- `windsurf-rule.template.md`

No VS Code template was rendered in Q24 because the target is disabled.

## Generated Outputs

Generated preview/managed outputs exist under `.aide/generated/adapters/`.

Approximate sizes:

| Output | Chars | Lines |
| --- | ---: | ---: |
| `AGENTS.md` preview | 1,325 | 19 |
| `CLAUDE.md` preview | 1,173 | 17 |
| `aider.conf.yml` preview | 962 | 13 |
| `clinerules` preview | 1,007 | 14 |
| Continue preview | 1,018 | 15 |
| Cursor preview | 1,071 | 17 |
| Windsurf preview | 999 | 14 |

This is compact enough for adapter guidance. The manifest and drift report are
longer because they are audit metadata, not tool guidance.

## Command Results

- `adapter list`: PASS
- `adapter render`: PASS
- `adapter validate`: PASS
- `adapter drift`: PASS
- `adapt`: Q24 evidence says deterministic and preserves manual content.

## Drift State

Latest drift report:

- Codex/AGENTS managed section: current.
- Claude/Aider/Cline/Continue/Cursor/Windsurf: preview-only, target files absent.

At checkpoint start, the generated adapter manifest showed Codex as drifted.
Running `adapter render` refreshed it to current. This is acceptable generated
artifact drift, but it reinforces that generated adapter outputs are not
canonical truth.

## Safety Assessment

Adapter guidance is safe for handover as preview/managed guidance:

- It points tools at `.aide/context/latest-task-packet.md`.
- It discourages long chat history and full-repo dumps.
- It requires evidence and review gates.
- It preserves `.aide.local/`.
- It warns against secrets, raw prompts, and raw responses.
- It does not implement any runtime integration.

Adapter guidance is not enforceable by itself. Existing tools must actually
read and honor it.
