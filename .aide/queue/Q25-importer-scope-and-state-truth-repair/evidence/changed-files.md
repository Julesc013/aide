# Changed Files

## Queue Packet And Evidence

- `.aide/queue/index.yaml`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/task.yaml`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/ExecPlan.md`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/prompt.md`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/status.yaml`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/**`

## Pack Integrity And Importer Scope

- `.gitignore`
- `.aide.local.example/secrets/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/policies/export-import.yaml`
- `.aide/import/README.md`
- `.aide/export/aide-lite-pack-v0/**`

Repeated Q25 revalidation added an explicit export-pack provenance guard in
`.aide/scripts/aide_lite.py` and exported it into
`.aide/export/aide-lite-pack-v0/files/.aide/scripts/aide_lite.py`. The matching
tests now cover stale clean manifest failure and explicit dirty manifest
acceptance.

## State Truth

- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `docs/roadmap/reboot-roadmap.md`
- `docs/roadmap/queue-roadmap.md`

## Generated Handoff Packet

- `.aide/context/latest-task-packet.md`
