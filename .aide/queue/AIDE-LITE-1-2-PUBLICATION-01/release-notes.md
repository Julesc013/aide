**Shared Lite lifecycle on four qualified modern profiles.** Adopt AIDE in a new or existing Git project, preserve project-owned policy and tools, customize managed content, and preview updates or removal before applying an exact plan.

### Changes

- **Portable lifecycle:** shared Windows, Linux and macOS filesystem bindings beneath the existing ownership and recovery mechanisms.
- **Upgrade and exit:** qualification against the actual published 1.1.0 package covers customization, direct edits, conflicts and recorded resolutions, interrupted imports, owned repair and removal.
- **Ownership repair:** re-observe live filesystem state before the existing ownership decision; retain the false-refusal regression and original failed attempts.
- **Release profiles:** explicit environment, command and limitation records; one maintained source tree with platform bindings.

### Qualified profiles

All profiles are **T3 Limited Support / L1 companion**, using **CPython 3.14.8**. This table describes the tested environments; it does not promise every OS release or Python minor version.

| Environment | Architecture | Public forms |
| --- | --- | --- |
| Windows 10, build 19045 | AMD64 | 56 |
| Windows Server 2025, build 26100 | AMD64 | 49 ordinary forms |
| Linux, kernel `7.0.0-1017-azure` | x86_64 | 49 ordinary forms |
| Darwin `24.6.0` / macOS 15 runner | arm64 | 49 ordinary forms |

The seven managed-job forms remain unqualified on each additional profile. Windows/Linux have fresh archive runs; macOS retains independently accepted behavioral evidence across the verified metadata-only archive change. The [qualification report](https://github.com/Julesc013/aide/blob/main/.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md) preserves exact tuples, subjects, failures, applicability proofs and replay results.

### Downloads

- **Portable package - ZIP:** `aide-lite-v1.2.0.zip`
- **Portable package - TAR.GZ:** `aide-lite-v1.2.0.tar.gz`
- **Release manifest:** `aide-lite-v1.2.0.manifest.json`
- **SHA-256 checksums:** `aide-lite-v1.2.0.SHA256SUMS.txt`

Download one portable package and the checksums, verify it, extract outside the development checkout, and follow its `install.md`. Use Python 3 on the qualified profile. GitHub's automatic **Source code** downloads are repository snapshots, not the portable install package.

### Limits and compatibility

- POSIX ownership is cooperative. Outer editor/shell read/write containment and OS network isolation are not established by this release.
- Changed-owned-path rollback and customized-overlay downgrade retain documented manual-recovery requirements. Preserve project work, backups and recovery evidence before exit; removal is not blanket `.aide` deletion.
- Native DOS/FreeDOS, Windows 9x, older NT, OS/2, BSD/Solaris/SunOS ports and IDE extensions remain staged work. Companion participation does not qualify those native ports.
- Live-model productivity, whole-task efficiency and autonomous cross-project delivery remain separate qualification obligations.

**Provenance:** the tag identifies the reviewed publication/documentation checkpoint; the manifest identifies immutable payload source `158a5cdcac7afecbc180a6324ea02e46617d1bc9`. Historical preparation wording inside the frozen package is qualified by the current release evidence. Lite 1.0.0 and 1.1.0 assets and tags remain preserved.
