# Cross-Repo Pack Export / Import v0

## Purpose

Q21 creates the first portable AIDE Lite Pack. The pack lets a target
repository receive AIDE Lite scripts, policies, prompts, templates, starter
evals, and no-call metadata without inheriting this AIDE repository's identity,
queue history, generated context, reports, local state, or secrets.

Q21 exists before the Eureka and Dominium pilots because direct manual copying
would be unsafe and noisy. Target repositories need their own profile, memory,
snapshot, index, task packet, verifier reports, token reports, and evidence.

## Portable Pack

The committed pack lives at:

```text
.aide/export/aide-lite-pack-v0/
```

Run the exporter from this repository root:

```bash
py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0
```

The exporter writes:

- `manifest.yaml`
- `checksums.json`
- `README.md`
- `install.md`
- `import-policy.yaml`
- `export-report.md`
- `files/` with portable AIDE Lite content and target templates

The pack includes portable scripts, tests, token/context/verifier/review/ledger
policies, prompts, verification templates, target-neutral local-state examples,
starter golden tasks, no-call router/Gateway/provider metadata, and docs.

The pack excludes source repo identity, source queue history, source memory,
generated context, reports, controller ledgers, latest route/cache/Gateway or
provider status reports, eval runs, `.aide.local/`, `.env`, raw prompts, raw
responses, and provider credentials.

## Import Dry Run

Use dry-run before writing to a target repository:

```bash
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --dry-run
```

Dry-run validates the manifest and checksums, reports copy operations and
conflicts, and writes nothing.

## Import

Use the same pack path without `--dry-run` to import:

```bash
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo>
```

The importer copies portable files into the target, creates target-specific
profile and memory placeholders from templates when absent, preserves manual
`AGENTS.md` content through a managed portable section, and ensures
`.aide.local/` is ignored.

The importer does not create actual `.aide.local/`, does not overwrite existing
target files without reporting conflicts, and does not call providers, models,
network services, or Gateway forwarding paths.

## Target Initialization

After import, the target repository must generate its own local artifacts:

```bash
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py pack --task "<target task>"
```

Target maintainers must replace placeholder profile and memory text with
target-specific facts before treating the pack as project-aware.

## Boundary

The portable pack is metadata and tooling, not proof that AIDE reduces tokens in
the target. Q22 Eureka Import Pilot and Q23 Dominium Import Pilot must measure:

- prompt-size reduction from compact task/context/review packets
- quality preservation through verifier and golden tasks
- local-state and secret safety
- target-specific usefulness

The Existing Tool Adapter Compiler remains deferred until those pilots prove
the pack is useful outside this repository.
