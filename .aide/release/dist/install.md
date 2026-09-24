# AIDE Lite Pack Local Install Notes

- bundle_id: aide-lite-pack-v0-0c98e175bab91513
- bundle_name: aide-lite-pack-v0
- source_pack: .aide/export/aide-lite-pack-v0
- pack_status: PASS
- publication_status: local_preview_no_publish
- apply_mode_available: false

## Default Workflow

1. Extract the archive into a review location.
2. Inspect `manifest.yaml`, `checksums.json`, `install.md`, and `files/**`.
3. From the extracted archive root, run the isolated dry-run and safe import commands from `install.md`.
4. Run target-local AIDE Lite validation after import.
5. Use install, repair, upgrade, rollback, and uninstall commands in observe/plan/dry-run mode only.

## Preservation Rules

- Target `.aide/memory/**`, `.aide/queue/**`, evidence, golden tasks, generated reports, docs/canon, manual guidance, and existing tools are target state and must be preserved.
- `.aide.local/**`, `.env`, secrets, raw prompts, raw responses, and provider credentials are never install candidates.
- Upgrade, repair, rollback, and uninstall are planning models only until a future reviewed apply phase exists.

## Publication Boundary

- This bundle is a local artifact, not an official GitHub Release.
- No Git tag, upload, branch mutation, active CI installation, target install, or provider/model/network call is performed by Q47.
