# Scoped changes

- Source: `.aide/scripts/aide_lite.py` and
  `.aide/scripts/tests/test_export_import.py`.
- Consumer guidance: `docs/reference/cross-repo-pack-export-import.md`.
- Task control: this WorkUnit, `.aide/queue/index.yaml`, `PLANS.md`,
  `IMPLEMENT.md`.
- Deterministic local outputs: five changelog preview records, five portable
  export records, and the current generator's derived `.aide/release/**` files.

No `.github/**`, target repository, hosted settings, credential, main, tag,
upload, or published Release was changed. Final candidate is a descendant of
remote dev `3bdeb220cb31dfc3177faa6836f5e86c8071d1ef`; dev is not changed
by this task branch yet.
