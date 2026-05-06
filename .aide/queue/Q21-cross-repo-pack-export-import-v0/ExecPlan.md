# Q21 Cross-Repo Pack Export / Import v0 ExecPlan

This is the living execution record for
`Q21-cross-repo-pack-export-import-v0`.

## Goal

Create a deterministic AIDE Lite Pack export/import workflow that can be
validated in local fixture repositories before real Eureka or Dominium pilots.

## Scope

- Define `.aide/policies/export-import.yaml`.
- Add `.aide/import/` target-neutral templates and import policy.
- Generate `.aide/export/aide-lite-pack-v0/` from allowed portable inputs.
- Extend AIDE Lite with `export-pack` and `import-pack` dry-run/import commands.
- Validate boundary rules against source-specific queue, memory, generated
  context, reports, latest status artifacts, local state, secrets, raw prompts,
  and raw responses.
- Add fixture tests that import into temporary target repos and run imported
  AIDE Lite smoke commands.
- Update docs and task-local evidence.

## Non-Goals

- No real Eureka or Dominium repo mutation.
- No provider/model/network calls.
- No Gateway forwarding, Runtime, UI, Commander, MCP/A2A, or autonomous loop.
- No existing-tool adapter compiler.
- No exact tokenizer or provider billing integration.

## Validation Intent

Run baseline Harness/AIDE Lite/unit tests, export the pack, dry-run and apply an
import into local fixtures, run imported target doctor/snapshot/pack where
feasible, run export/import unit tests, run diff checks, and scan for secrets.

## Progress

- 2026-05-07: Baseline started from clean tree at
  `997cfe5c52e0bc5e9075ab3bca417bd7ba231867`.
- 2026-05-07: Confirmed QFIX-01/QFIX-02 outputs exist. QFIX-02 remains
  `needs_review` by design but its canonical `aide_lite.py test` command
  passes.
- 2026-05-07: Added Q21 queue packet scaffold and index entry.
- 2026-05-07: Added export/import policy and target-neutral import templates.

## Decisions

- The portable pack must contain templates for target identity and memory, not
  AIDE's own `.aide/profile.yaml`, `.aide/queue/`, or `.aide/memory/*.md`.
- Import validation must use local temporary fixtures only.

## Recovery Notes

All generated export files can be regenerated with:

```text
py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0
```

Fixture imports should be rerun in temporary directories rather than committed
target repos.
