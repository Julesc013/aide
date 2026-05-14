# Q37 Export Pack Sync

## Exported Q37 Support

The `aide-lite-pack-v0` export now includes portable Q37 support:

- `.aide/policies/repo-intelligence.yaml`
- `.aide/policies/file-classification.yaml`
- `.aide/policies/ownership-map.yaml`
- `.aide/policies/dependency-map.yaml`
- `.aide/policies/test-map.yaml`
- `.aide/policies/doc-link-map.yaml`
- `.aide/repo/file-inventory.schema.json`
- `.aide/repo/ownership-map.schema.json`
- `.aide/repo/dependency-map.schema.json`
- `.aide/repo/test-map.schema.json`
- `.aide/repo/doc-link-map.schema.json`
- `.aide/repo/repo-intelligence-summary.schema.json`
- `.aide/repo/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q37_repo_intelligence.py`
- Q37 golden tasks and catalog entries
- `docs/reference/repo-intelligence-index.md`

## Excluded Source Truth

The export boundary excludes source-generated repo intelligence outputs:

- `.aide/repo/file-inventory.json`
- `.aide/repo/ownership-map.json`
- `.aide/repo/dependency-map.json`
- `.aide/repo/test-map.json`
- `.aide/repo/doc-link-map.json`
- `.aide/repo/generated-map.json`
- `.aide/repo/orphan-candidates.json`
- `.aide/repo/latest-repo-intelligence.md`

Target repositories must run `repo inventory`, `repo validate`, and
`repo status` locally after import.

## Validation

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid,
  boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
