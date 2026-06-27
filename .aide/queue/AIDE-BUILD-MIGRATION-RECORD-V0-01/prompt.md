# Prompt: AIDE-BUILD-MIGRATION-RECORD-V0-01

Create and process `AIDE-BUILD-MIGRATION-RECORD-V0-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

Authority:

- Build only.
- Do not perform migration apply.
- Do not perform install/update/rollback/uninstall apply.
- Do not mutate target repositories.
- Do not create releases, tags, uploads, or GitHub Releases.
- Do not call provider/model/network services.

Build objective:

Build MigrationRecord v0 as a no-apply protocol/helper/projection/validation slice after accepted InstallRecord v0.
