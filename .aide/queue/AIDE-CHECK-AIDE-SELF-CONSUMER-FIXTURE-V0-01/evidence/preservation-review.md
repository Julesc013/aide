# Preservation Review

The ownership map preserves target-owned examples:

- `.aide/memory/project-state.md`
- `.aide/queue/target-local-task/status.yaml`
- `.aide/evidence/target-local-proof.md`
- `.aide.local/cache/state.json`
- `AGENTS.md#manual-content`
- `README.md`

Automatic apply is blocked for:

- `project_owned`
- `project_overlay`
- `project_generated`
- `runtime_generated`
- `local_only`
- `evidence_only`
- `preserved_legacy`
- `unknown`
- `never_touch`

The target-owned preservation and uninstall scenarios both carry the preservation examples. This remains fixture proof only and does not authorize real target mutation.
