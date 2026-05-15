# GitHub Release Publication Checklist

- checklist_id: aide-lite-pack-v0-github-draft-2b2a00f7c4628311-checklist
- source_commit: 2b2a00f7c462831170dc8de21834e1e5ec91708d
- no_publish: true

## Checks
- [source repo state] branch checked: recorded (main)
- [source repo state] source commit recorded: recorded (2b2a00f7c462831170dc8de21834e1e5ec91708d)
- [source repo state] dirty state recorded: recorded (true)
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
