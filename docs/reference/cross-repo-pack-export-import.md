# Cross-Repo Pack Export / Import v0

## Purpose

Q21 creates the first portable AIDE Lite Pack. Q25 repairs its integrity and
safe import scope. Q31 makes the pack carry the portable Q27-Q30 governance
surface. Q34 adds portable changelog/release-note preview support while keeping
generated source previews out of target truth. Q35 adds portable GitHub
protection and CI advisory policy while keeping source advisory reports out of
target truth. Q36 adds portable deterministic intent-compilation policy,
schemas, examples, tests, golden tasks, and docs while keeping source-generated
latest intent packets out of target truth. Q37 adds portable repo-intelligence
policies, schemas, tests, golden tasks, and docs while keeping source-generated
`.aide/repo/*.json` and latest repo-intelligence Markdown out of target truth.
Q38 adds portable file-quality policies, schemas, tests, golden tasks, commands,
and docs while keeping source-generated file-quality ledgers and reports out of
target truth. Q39 adds portable refactor-control policies, schemas, tests,
golden tasks, commands, and docs while keeping source-generated refactor
readiness and example plans out of target truth. Q40 adds portable root
recycling policies, schemas, tests, golden tasks, commands, and docs while
keeping source-generated root inventories, classifications, plans, exceptions,
and risk summaries out of target truth. Q41 adds portable existing-tool
absorption policies, schemas, tests, golden tasks, commands, and docs while
keeping source-generated tool inventories, classifications, wrap plans, adapter
maps, and risk summaries out of target truth. The pack lets a target repository
receive AIDE Lite scripts, policies, prompts, templates, starter evals, and
no-call metadata without inheriting this AIDE repository's identity, queue
history, generated context, reports, local state, or secrets.

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
After Q35 it also includes portable commit-message policy, the opt-in commit
hook template, commit template, changelog policy/config/templates, changelog
preview/validate/status support, task resumption, WorkUnit and recovery policy,
generic Git workflow policy, branch roles, promotion/sync/prune policy, project
workflow profiles, dry-run Git helper policy, GitHub protection/branch
protection/CI gate advisory policies, intent compiler policy/schemas/examples,
repo intelligence policy/schemas/docs, file quality policy/schemas/docs,
refactor-control policy/schemas/docs, and governance golden tasks.
The documentation-only `.aide.local.example/secrets/README.md` file is allowed
as a safe example so Q18 local-state validation and target imports agree on the
example tree shape; real `secrets/**` paths remain ignored and forbidden.

Q25 keeps optional broad roots in the export pack for reviewed fixtures but
makes command import safe by default. Q31 safe import still skips broad `core/`
roots and non-reference `docs/` roots, but it allows portable
`docs/reference/**` governance docs because target repos need the imported
commit, recovery, Git workflow, and GitHub/CI advisory references.

The pack excludes source repo identity, source queue history, source memory,
generated context, reports, controller ledgers, latest route/cache/Gateway or
provider status reports, eval runs, AIDE-specific Git workflow detection
outputs, latest helper plans, AIDE-specific dev/main branch policy and plan
artifacts, generated changelog previews and preview JSON, latest changelog
reports, source-generated latest intent packets and WorkUnit drafts,
source-generated repo intelligence indexes and summaries, source-generated
file-quality ledgers and reports, source-generated refactor readiness and
example plans, `.aide.local/`, `.env`, raw prompts, raw responses, and provider
credentials.

Pack checksums cover payload and static pack docs. Mutable metadata files
`manifest.yaml`, `checksums.json`, and `export-report.md` are intentionally
excluded from the checksum map so validation does not become self-inconsistent.
Payload tampering still fails `pack-status`, and pack validation also fails if
a payload file exists in the pack without a checksum entry.

`pack-status` validates provenance separately from checksums. A clean manifest
must match the current Git commit. If the exporter runs while the source tree is
dirty, the manifest records `source_dirty_state: true`; `pack-status` reports
that as `DIRTY_SOURCE_RECORDED` rather than treating it as a hidden clean pass.
Missing provenance, malformed dirty-state metadata, or stale clean provenance
fail validation.

## Import Dry Run

Use dry-run before writing to a target repository:

```bash
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --dry-run
```

Dry-run validates checksums, reports exact planned writes, reports skipped
optional broad roots, reports conflicts, and writes nothing.

## Import

Use the same pack path without `--dry-run` to import:

```bash
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo>
```

The default importer mode is `safe`. It copies portable `.aide/` files,
`.aide.local.example/`, target templates, managed `AGENTS.md` guidance, and
`.gitignore` local-state rules. It creates target-specific profile and memory
placeholders from templates when absent, preserves manual `AGENTS.md` content,
and ensures `.aide.local/` is ignored.

Use `--mode full` only in a reviewed local fixture when optional broad roots
such as `core/` and `docs/` are intentionally selected. Target pilots should
normally use safe mode and then generate target-local snapshot/index/pack
artifacts.

The importer does not create actual `.aide.local/`, does not overwrite existing
target files without reporting conflicts, and does not call providers, models,
network services, or Gateway forwarding paths.

## Target Initialization

After import, the target repository must generate its own local artifacts:

```bash
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py repo inventory
py -3 .aide/scripts/aide_lite.py repo validate
py -3 .aide/scripts/aide_lite.py repo status
py -3 .aide/scripts/aide_lite.py quality ledger
py -3 .aide/scripts/aide_lite.py quality validate
py -3 .aide/scripts/aide_lite.py quality status
py -3 .aide/scripts/aide_lite.py refactor status
py -3 .aide/scripts/aide_lite.py refactor plan
py -3 .aide/scripts/aide_lite.py refactor validate
py -3 .aide/scripts/aide_lite.py pack --task "<target task>"
```

Target maintainers must replace placeholder profile and memory text with
target-specific facts before treating the pack as project-aware.

After Q34, target maintainers can also validate the imported governance surface:

```bash
py -3 .aide/scripts/aide_lite.py commit template
py -3 .aide/scripts/aide_lite.py commit check --message-file <message-file>
py -3 .aide/scripts/aide_lite.py changelog preview
py -3 .aide/scripts/aide_lite.py changelog validate
py -3 .aide/scripts/aide_lite.py task inspect
py -3 .aide/scripts/aide_lite.py git policy
py -3 .aide/scripts/aide_lite.py git detect
py -3 .aide/scripts/aide_lite.py git plan
py -3 .aide/scripts/aide_lite.py intent compile --prompt "<target task>"
py -3 .aide/scripts/aide_lite.py intent validate
py -3 .aide/scripts/aide_lite.py repo explain-file .aide/scripts/aide_lite.py
py -3 .aide/scripts/aide_lite.py refactor dry-run
```

The hook template is imported under `.aide/hooks/commit-msg`, but it is not
installed into `.git/hooks`. Hook installation remains an explicit target-repo
operator action through `commit install-hook`.

## Boundary

The portable pack is metadata and tooling, not proof that AIDE reduces tokens in
the target. Q22 Eureka Import Pilot and Q23 Dominium Import Pilot must measure:

- prompt-size reduction from compact task/context/review packets
- quality preservation through verifier and golden tasks
- local-state and secret safety
- target-specific usefulness

The Existing Tool Adapter Compiler remains deferred until those pilots prove
the pack is useful outside this repository.

Q22 and Q23 produced initial Eureka and Dominium token-reduction evidence. Q25
repairs pack integrity and import scope before Q26 performs the Eureka handover
review. Q31 makes the canonical pack ready for Q32 Eureka sync and Q33 Dominium
sync; Q34 extends the pack with release draft previews; Q37 extends the pack
with repo intelligence support; Q38 extends it with advisory file-quality
ledger support; Q39 extends it with no-apply refactor-control planning support;
Q40 extends it with no-apply root recycling framework support; Q41 extends it
with no-execution existing-tool absorption support.
Those target phases must regenerate their own branch detection, helper plans,
repo intelligence indexes, file-quality ledgers, refactor readiness plans, root
inventories, root classifications, root plans, context packets, review packets,
and evidence locally; they must not reuse AIDE's generated source-repo reports
as target truth.
