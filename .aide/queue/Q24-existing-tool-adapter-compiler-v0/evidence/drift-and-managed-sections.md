# Drift And Managed Sections

## Managed Section

The Q24 managed section marker is:

```text
<!-- AIDE-GENERATED:BEGIN section=aide-token-survival-adapter target=codex_agents_md generator=aide-adapter-compiler-v0 generator_version=q24.existing-tool-adapter-compiler.v0 manual=outside-only generated_outputs_not_canonical=true -->
```

The matching end marker is:

```text
<!-- AIDE-GENERATED:END section=aide-token-survival-adapter -->
```

Manual root `AGENTS.md` content outside this section is preserved.

## Drift Status

Latest drift report path:

- `.aide/generated/adapters/drift-report.md`

Latest rendered status:

| Target | Mode | Status |
| --- | --- | --- |
| `codex_agents_md` | `managed_section` | `current` |
| `claude_code` | `preview_only` | `preview_only` |
| `aider` | `preview_only` | `preview_only` |
| `cline` | `preview_only` | `preview_only` |
| `continue` | `preview_only` | `preview_only` |
| `cursor` | `preview_only` | `preview_only` |
| `windsurf` | `preview_only` | `preview_only` |

## Drift Behavior Tested

The Q24 adapter tests cover:

- missing target file detection;
- current managed-section detection;
- drifted managed-section detection;
- deterministic `adapt` behavior;
- manual content preservation outside managed sections;
- preview-only targets not being written by `adapter generate`.

## Preview-Only Rationale

Real tool files are intentionally preview-only unless a reviewed policy says a
target repo may write them. This avoids destructive changes to existing Claude,
Aider, Cline, Continue, Cursor, Windsurf, or VS Code guidance.
