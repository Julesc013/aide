# Export Pack Sync

Q35 portable files should be included in the AIDE Lite pack:

- `.aide/policies/github-protection.yaml`
- `.aide/policies/ci-gates.yaml`
- `.aide/policies/branch-protection.yaml`
- `.aide/github/README.md`
- `docs/reference/github-protection-ci-advisory.md`
- updated `.aide/scripts/aide_lite.py`
- Q35 tests and golden tasks

Generated source-specific `.aide/github/*.json` and `.md` advisory outputs are
excluded from target truth.

Validation:

- `export-pack --name aide-lite-pack-v0`: PASS, 220 portable files.
- `pack-status`: PASS, checksums valid, boundary PASS.
- `github_export_inclusion_golden`: PASS, 21/21 checks.
