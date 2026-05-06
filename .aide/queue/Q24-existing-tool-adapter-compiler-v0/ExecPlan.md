# Q24 Existing Tool Adapter Compiler v0 ExecPlan

## Purpose

Create the first deterministic adapter compiler that renders compact AIDE
token-survival guidance for existing tools: Codex/AGENTS, Claude Code, Aider,
Cline, Continue, Cursor, Windsurf, and optional VS Code task previews.

## Scope

Q24 is a template compiler and managed/preview-output phase only. It must not
call tools, providers, models, networks, Gateway forwarding, IDE extensions, or
external repositories.

## Current Plan

1. Inspect QFIX-01, QFIX-02, Q21, current adapter metadata, root guidance, and
   baseline validation.
2. Add the Q24 queue packet and evidence skeleton.
3. Add `.aide/policies/adapters.yaml`, adapter target definitions, and concise
   tool-specific templates.
4. Extend AIDE Lite with `adapter list/render/preview/validate/drift/generate`
   and align `adapt` with safe managed-section generation.
5. Render preview artifacts under `.aide/generated/adapters/` and include
   adapter templates in the portable export pack.
6. Add deterministic unittest coverage for rendering, drift, managed-section
   preservation, preview-only behavior, and export-pack inclusion.
7. Update documentation and evidence, regenerate the next task packet, run
   validation, and stop at review.

## Validation Intent

- Harness validate/doctor/self-check.
- AIDE Lite doctor/validate/test/selftest.
- Adapter command smoke: list, render, preview, validate, drift, generate/adapt.
- Export-pack refresh and pack-status validation.
- Unit tests for AIDE Lite, Harness, Compatibility, Gateway, and Providers.
- `git diff --check`, `.aide.local/` ignore check, and targeted secret scan.

## Known Constraints

- Q22/Q23 real pilot evidence is absent in this repository at Q24 start.
- Generated adapter outputs are downstream guidance, not canonical truth.
- Preview-only target files must not be written destructively.
- Root `AGENTS.md` may be updated only through managed sections that preserve
  manual content outside the section.

## Review Gate

Q24 must end with `status: needs_review` so a human or later review phase can
validate adapter scope, generated outputs, drift behavior, and documentation.

## Progress Notes

- Baseline inspection and validation completed on 2026-05-07.
- Q24 policy, target catalog, templates, adapter commands, generated previews,
  export-pack template inclusion, and tests are implemented.
- `AGENTS.md` was updated only through the Q24 managed section.
- Claude Code, Aider, Cline, Continue, Cursor, Windsurf, and VS Code targets
  remain preview-only or disabled according to `.aide/adapters/targets.yaml`.
- Q22/Q23 real target-pilot evidence remains absent from this AIDE repo and is
  recorded as a limitation rather than treated as implemented proof.
