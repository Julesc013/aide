# AIDE Lite Pack Local Install Notes

- bundle_id: aide-lite-pack-v0-49318d50472b17f6
- bundle_name: aide-lite-pack-v0
- source_pack: .aide/export/aide-lite-pack-v0
- pack_status: PASS
- publication_status: local_preview_no_publish
- apply_mode_available: true
- apply_mode_scope: bounded receipt-owned removal on Windows

## Default Workflow

1. Extract the archive into a review location.
2. Inspect `manifest.yaml`, `checksums.json`, `install.md`, and `files/**`.
3. From the extracted archive root, run the isolated dry-run and safe import commands from `install.md`.
4. Run target-local AIDE Lite validation after import.
5. On Windows, use `plan-removal --target <target-repo> --json`, then `apply-removal --target <target-repo> --expect-plan <plan_digest>` for receipt-owned removal.
6. Treat other lifecycle apply commands according to their separately documented boundaries.
7. `plan-removal` reports `apply_allowed: false` because that command is read-only; the separate `apply-removal` command accepts its exact digest on Windows.

## Preservation Rules

- Target `.aide/memory/**`, `.aide/queue/**`, evidence, golden tasks, generated reports, docs/canon, manual guidance, and existing tools are target state and must be preserved.
- `.aide.local/**`, `.env`, secrets, raw prompts, raw responses, and provider credentials are never install candidates.
- Windows `apply-removal` deletes only unchanged receipt-owned regular files and an exact generated whole-file `AGENTS.md` scaffold. A stale preview refuses before deletion; a change after removal begins returns `RECOVERY_REQUIRED` with the intent retained and earlier deletions possible.
- Authored `AGENTS.md` content remains intact; when other eligible files are removed, the runner and receipt remain and the command reports `PARTIAL_REMOVAL`.
- Authored `AGENTS.md` managed-section removal and non-Windows removal apply remain unavailable. An interrupted removal requires exact-intent reconciliation; a partial result retains the receipt and runner for further review.
- General install, repair, upgrade, and rollback apply have separate documented scopes; this removal command does not expand them.

## Publication Boundary

- This bundle is a local artifact, not an official GitHub Release.
- No Git tag, upload, branch mutation, active CI installation, target install, or provider/model/network call is performed by Q47.
