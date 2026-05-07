# Adapter Compiler State

## Presence

- Policy: `.aide/policies/adapters.yaml`
- Targets: `.aide/adapters/targets.yaml`
- Templates: `.aide/adapters/templates/**`
- Generated outputs: `.aide/generated/adapters/**`
- Manifest: `.aide/generated/adapters/manifest.json`
- Drift report: `.aide/generated/adapters/drift-report.md`
- Reference doc: `docs/reference/existing-tool-adapter-compiler-v0.md`
- Queue evidence: `.aide/queue/Q24-existing-tool-adapter-compiler-v0/**`

## Targets

| Target | Output | Mode | Status |
| --- | --- | --- | --- |
| Codex / AGENTS | `AGENTS.md` | managed section | current |
| Claude Code | `CLAUDE.md` | preview only | target absent |
| Aider | `.aider.conf.yml` | preview only | target absent |
| Cline | `.clinerules` | preview only | target absent |
| Continue | `.continue/checks/aide-token-survival.md` | preview only | target absent |
| Cursor | `.cursor/rules/aide-token-survival.mdc` | preview only | target absent |
| Windsurf | `.windsurf/rules/aide-token-survival.md` | preview only | target absent |
| VS Code optional | `.vscode/tasks.json` | preview only, disabled | not rendered |

## Command Results

- `adapter list`: PASS.
- `adapter render`: PASS, outputs unchanged.
- `adapter preview`: PASS, writes none.
- `adapter validate`: PASS.
- `adapter drift`: PASS.
- `adapt`: PASS, `AGENTS.md` unchanged/current.
- second `adapt`: PASS, unchanged/current.

No provider/model/network calls were made.

## Safety

- Generated outputs are non-canonical.
- Manual content outside managed sections is preserved.
- Preview-only targets are not written.
- Drift is reported, not fixed automatically.
- Root/tool writes are limited to the safe Q24 managed section in `AGENTS.md`.
- Adapter validation checks for compact task-packet guidance, evidence/review
  guidance, no full-history/full-repo prompting, and no secret-like values.

## Conciseness

| Generated Preview | Chars | Approx Tokens |
| --- | ---: | ---: |
| `.aide/generated/adapters/AGENTS.md` | 1,325 | 332 |
| `.aide/generated/adapters/CLAUDE.md` | 1,173 | 294 |
| `.aide/generated/adapters/aider.conf.yml` | 962 | 241 |
| `.aide/generated/adapters/clinerules` | 1,007 | 252 |
| `.aide/generated/adapters/continue-checks/aide-token-survival.md` | 1,018 | 255 |
| `.aide/generated/adapters/cursor-rules/aide-token-survival.mdc` | 1,071 | 268 |
| `.aide/generated/adapters/windsurf-rules/aide-token-survival.md` | 999 | 250 |

The previews are compact enough to avoid becoming another prompt-bloat source.

## Export-Pack Inclusion

The exported pack includes:

- `.aide/policies/adapters.yaml`
- `.aide/adapters/targets.yaml`
- `.aide/adapters/templates/**`
- adapter compiler tests
- adapter compiler reference docs

It does not export generated adapter previews as target truth.

## Limitations

- No actual IDE extension or tool plugin exists.
- No tool runtime API integration exists.
- Existing tools may ignore guidance unless configured by humans/agents.
- Q24 target-pilot evidence proves packet reduction in Eureka/Dominium, not
  adapter-output usage by every tool.
