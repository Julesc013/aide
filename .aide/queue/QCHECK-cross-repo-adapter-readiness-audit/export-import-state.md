# Export / Import State

## Pack Presence

- Pack path: `.aide/export/aide-lite-pack-v0/`.
- Manifest: present.
- Checksums: present.
- Install docs: present.
- Import policy: present.
- Export report: present.
- Payload root: present.

Final `py -3 .aide/scripts/aide_lite.py pack-status` result:

- checksums valid: false
- boundary result: PASS
- checksum problems: 1
- boundary violations: 0

The reported checksum problem is `manifest.yaml`.

## Current Export Command Result

`py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` was run
as an audit validation command. It passed with:

- included files: 122
- checksum count: 126
- boundary result: PASS
- provider/model calls: none
- network calls: none

Because the command was run after report commands had temporarily dirtied
non-canonical generated files, the refreshed generated pack output was restored
instead of committed. This avoids committing an audit-run dirty-state pack.

## Include / Exclude Boundary

Included classes:

- scripts and AIDE Lite tests
- policies
- prompts
- context templates/config
- verification templates
- eval starter tasks
- adapter templates and targets
- docs and install instructions
- local/report-only Gateway and offline provider metadata
- target-neutral profile/memory templates

Excluded classes:

- source repo identity
- source repo queue history
- source repo memory
- generated context
- generated reports
- route decisions
- cache-key reports
- Gateway status reports
- provider status reports
- eval runs
- outcome ledgers
- local state
- secrets
- raw prompts
- raw responses

Boundary check detail:

- `.aide/export/aide-lite-pack-v0/files/.aide/queue/` contains only
  `README.template.md`, not source queue history.
- `.aide/context/latest-*`, `repo-map.*`, `.aide/reports/**`,
  `.aide/cache/latest-*`, `.aide/routing/latest-*`, `.aide/controller/**`,
  `.aide/gateway/latest-*`, `.aide/providers/latest-*`, `.aide.local`, and
  `.env` are not exported.

## Fixture Import

Q21 fixture evidence records:

- dry-run: PASS, 116 operations, 0 conflicts, 0 writes.
- import: PASS, 116 operations, 0 conflicts, 116 writes.
- target doctor/snapshot/index/pack/estimate: PASS.
- manual `AGENTS.md` content preserved.
- target memory generated from templates.
- `.aide.local/` ignored and not created.

Fixture warning: target doctor reports missing Q09-Q20 queue status files
because the pack correctly does not copy AIDE self-hosting queue history.

## Real Target Import Lessons

Eureka and Dominium both used the Q21 importer for dry-run, then performed
manual manifest/policy-guided imports. The reason was the same in both pilots:
direct importer apply would copy all pack `files/` roots, including broader
`core/**` and docs/reference surfaces outside the target prompt's allowed
paths.

This does not invalidate Q21, but it does mean "direct importer is ready for
serious target handoff" is not yet proven. The next repair should add a
target-scoped mode, include/exclude switches, or a safer default apply policy.

## Integrity And Provenance Warning

The committed pack manifest currently records:

- source commit: `3753164387c85e8f34011ac5f69f8dc8ecc332bd`
- source dirty state: `true`

AIDE HEAD during this audit is:

- `36dcb5cc9907f0e69d615d99ab2b0a1dcb17a2d0`

The pack boundary passes, but committed checksum validation fails on
`manifest.yaml`, and the dirty provenance is not acceptable for broad handover.
Regenerate from a clean HEAD in a repair phase, then rerun `validate`,
`pack-status`, and a fixture import smoke.
