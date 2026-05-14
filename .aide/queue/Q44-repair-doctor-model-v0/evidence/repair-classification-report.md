# Repair Classification Report

## Repair Classes

The repair class policy defines missing/stale portable artifacts, generated
packet problems, managed-section issues, target memory/queue gaps, golden task
catalog issues, pack checksum/provenance issues, source-state contamination,
tracked local state, secret-like files, unsupported schemas, ambiguous
ownership, target-specific conflicts, and unknown issues.

Each class records detection hints, risk class, preserve-by-default posture,
future apply gate, validation requirement, evidence requirement, and rollback
note requirement for any later apply phase.

## Current Diagnosis

Latest diagnosis: `.aide/repair/latest-repair-diagnosis.json`.

- total diagnoses: 11
- blockers: 0
- class counts:
  - `missing_portable_file`: 8
  - `stale_command_catalog`: 1
  - `stale_golden_task_catalog`: 1
  - `stale_pack_provenance`: 1
- severity counts:
  - `warning`: 10
  - `info`: 1

## Current Candidate Paths

- `.aide/commands/catalog.yaml`: stale command catalog candidate.
- `.aide/evals/golden-tasks/catalog.yaml`: stale golden task catalog candidate.
- `.aide/export/aide-lite-pack-v0/manifest.yaml`: stale pack provenance candidate.
- `.aide/import-policy.template.yaml`: missing portable template candidate.
- `.aide/import-report.template.md`: missing portable template candidate.
- `.aide/memory/decisions.template.md`: missing portable template candidate.
- `.aide/memory/open-risks.template.md`: missing portable template candidate.
- `.aide/memory/project-state.template.md`: missing portable template candidate.
- `.aide/profile.template.yaml`: missing portable template candidate.
- `.aide/queue/README.template.md`: missing portable template candidate.
- `AGENTS.md.template`: missing portable template candidate.

## Preservation Summary

All current items are candidate future repairs only. Q44 does not restore,
refresh, overwrite, delete, migrate, or quarantine anything. Target-specific
memory, queue, evidence, generated reports, local state, and manual content
remain preservation-first.
