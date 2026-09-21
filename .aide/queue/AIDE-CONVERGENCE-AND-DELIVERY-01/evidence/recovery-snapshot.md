# Recovery Snapshot

- Source HEAD: `2a44f17eb7232757133df549ac6fc519d535e71b`
- Source status SHA-256: `739962744b5e3a98d2c6c2acecd0d8ae355f8db4a4419a3ecfd13481b6f4a87b`
- History bundle SHA-256: `5bd12a5e7678a67216e1ebba99ba5fba2b2286a29cbb0ae6b995b8b157dcf1f1`
- Tracked dirty paths preserved: 25
- Untracked files preserved: 714
- Ignored task-evidence files preserved: 82
- Restore result: PASS
- Restored status byte-identical: true

The recovery payload is private external custody and is not committed. Ignored
non-task evidence was not copied. Other Codex processes were observed, so the
stable before/after snapshot does not claim process quiescence. The stale
`aide-screensave-pack` directory was unavailable; its detached commit is present
in the verified bundle.
