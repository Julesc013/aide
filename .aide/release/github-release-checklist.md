# GitHub Release Publication Checklist

- checklist_id: aide-lite-pack-v0-github-draft-71501c6bb30bb19a-checklist
- source_commit: 71501c6bb30bb19a6f7cb0056ba0f009d39a9b40
- no_publish: true

## Checks
- [source repo state] branch checked: recorded (not-recorded-in-pack)
- [source repo state] source commit recorded: recorded (71501c6bb30bb19a6f7cb0056ba0f009d39a9b40)
- [source repo state] dirty state recorded: recorded (false)
- [source repo state] tag not created yet: pass (tag_created=false)
- [validation gates] release validate: required (.aide/release/dist/release-validation.md)
- [validation gates] draft validate: required (.aide/release/github-release-draft-validation.md)
- [artifact gates] zip exists: pass (.aide/release/dist/aide-lite-pack-v0.zip)
- [artifact gates] tar.gz exists: pass (.aide/release/dist/aide-lite-pack-v0.tar.gz)
- [artifact gates] checksums exist: pass (.aide/release/dist/aide-lite-pack-v0.checksums.json)
- [artifact gates] manifest exists: pass (.aide/release/dist/manifest.yaml)
- [artifact gates] install notes exist: pass (.aide/release/dist/install.md)
- [security gates] no local state or secret assets: required (targeted secret scan)
- [target install caveats] target install readiness not claimed: pass (Q49/Q50/Q54/Q55 remain future work)

## Blockers
- none

## Warnings
- none

## Manual Review Required
- review release body
- review suggested tag
- review asset list
- review known risks
- review target install caveats
- decide whether this is pre-release/draft/stable
- decide whether to publish
