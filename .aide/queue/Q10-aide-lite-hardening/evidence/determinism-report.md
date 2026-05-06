# Q10 Determinism Report

## Adapter Determinism

- First Q10 `adapt` replaced the legacy Q09 token-survival managed section in `AGENTS.md`.
- Final `adapt` run: PASS, action `unchanged`, before status `current`, after status `current`.
- Final second `adapt` run: PASS, action `unchanged`, before status `current`, after status `current`.
- Manual `AGENTS.md` operating law and the separate Q05 self-hosting summary managed section were preserved.

## Snapshot Determinism

- Final validation `snapshot` run before evidence finalization: PASS.
- Snapshot output path: `.aide/context/repo-snapshot.json`.
- Summary observed during Q10 finalization: 581 files. Aggregate byte and approximate-token totals change when evidence files are edited, so the snapshot was refreshed again after evidence updates.
- Records are sorted by repo-relative path.
- Records include `path`, `size`, `mtime`, `sha256`, `extension`, and `type`.
- Snapshot excludes ignored paths such as `.git/**`, `.env`, `.aide.local/**`, caches, `node_modules/**`, `dist/**`, `build/**`, archives, and binary/media patterns.
- Snapshot stores no raw file contents.

## Packet Determinism

- Final `pack --task "Implement Q11 Context Compiler v0"` run: PASS, action `unchanged`.
- Packet output path: `.aide/context/latest-task-packet.md`.
- Packet size: 2,566 chars, 91 lines, 642 approximate tokens.
- Packet budget status: PASS.
- Packet references project memory, decisions, open risks, repo snapshot, compact task template, and token-budget policy instead of inlining source files.

## Intentionally Volatile Or Non-Canonical Outputs

- `.aide/context/repo-snapshot.json` contains file mtimes and hashes; it is deterministic for a fixed repo state but will change when files change.
- `.aide/context/latest-task-packet.md` is a latest generated packet, not canonical project law.
- `.aide/generated/manifest.yaml` is generated through Harness compile/write and remains a non-canonical generated artifact.
- Q10 evidence files are task-local review evidence and intentionally record command outcomes.
