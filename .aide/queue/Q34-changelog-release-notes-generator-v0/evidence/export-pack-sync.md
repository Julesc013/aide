# Export Pack Sync

Status: complete for review.

- changelog policy export: present at `files/.aide/policies/changelog.yaml`
- changelog config/templates export: present under `files/.aide/changelog/`
- Q34 test export: present at `files/.aide/scripts/tests/test_q34_changelog_release.py`
- Q34 golden task export: present for release-note preview, malformed commit reporting, and JSON shape
- generated preview exclusion: confirmed; source-generated preview Markdown/JSON, malformed report, and latest changelog report are not exported as target truth
- `export-pack --name aide-lite-pack-v0`: PASS
- `pack-status`: PASS, checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`

Targets importing the pack receive generator capability and templates, then must generate their own local previews.
