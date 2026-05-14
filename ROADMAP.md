# AIDE Roadmap

## Scope And Limits

This roadmap is a phase-based engineering guide. It is not a calendar promise and it does not override governance, support law, or actual verification evidence.

## Completed Phases

- `P00`: governance, naming law, support law, capability doctrine, and root control-plane baseline
- `P01` through `P05`: inventory, matrices, host-family scaffolding, and source-backed ecosystem atlases for Microsoft, Apple, CodeWarrior, and broader legacy candidates
- `P06` through `P09`: shared-core architecture, environment or lab framework, evaluation and packaging framework, and first boot-slice specification plus rollout plan
- `P10`: shared-core boot-slice implementation with deterministic CLI bridge, fixtures, and tests
- `P11` through `P13`: first Microsoft, Apple, and CodeWarrior host-family proof waves
- `P14`: documentation normalization, roadmap, contributor guidance, maintenance automation baseline, and post-P13 audit reports
- `P15`: self-hosting filesystem queue scaffold and first Q00 task packet
- `Q01`: documentation split and canonical architecture records, pending review
- `Q02`: README-only structural skeleton for Core, Hosts, Bridges, and migration mapping, pending review
- `Q03`: declarative Profile/Contract v0 under `.aide/`, pending review
- `Q04`: minimal executable Harness v0 command surface, passed with notes
- `Q05`: generated artifacts v0 for managed sections, preview-only Claude guidance, manifest records, and drift checks, pending review
- `Q06`: Compatibility baseline for known v0 versions, no-op migration registry, replay metadata, upgrade gates, and deprecations; raw status remains pending review while review evidence records PASS_WITH_NOTES
- `Q07`: AIDE-side Dominium Bridge baseline for metadata, XStack boundary, overlays, target expectations, pinning, and structural Harness checks, passed with notes
- `Q08`: report-first self-hosting automation scaffold for self-checks, queue visibility, doctor next-step cleanup, and drift reporting, passed with notes
- `Q09` through `Q20`: token-survival foundation accepted with notes by QFIX-01, covering compact packets, AIDE Lite, context compiler, verifier, evidence review, estimated token ledger, golden tasks, advisory outcome/controller/routing, cache/local-state boundary, local/report-only Gateway skeleton, and offline provider metadata
- `QFIX-01`: Foundation Review Reconciliation, accepted with notes by QFIX-03
- `QFIX-02`: AIDE Lite Test Discovery and Runner Fix, accepted with notes by QFIX-03
- `Q21`: Cross-Repo Pack Export / Import v0, accepted with notes by QFIX-03 with local fixture imports only
- `Q24`: Existing Tool Adapter Compiler v0, accepted with notes by QFIX-03 with generated previews and safe managed `AGENTS.md` output only
- `Q22/Q23 target pilots`: Eureka and Dominium imports have been run in their sibling target repos and await target-repo review; they report large estimated task-packet reductions but do not yet prove adapter-output usage by every tool
- `Q25`: Importer Scope And State Truth Repair, accepted with notes by QFIX-03; pack-status passes and import defaults to safe scope
- `Q26`: Eureka Pilot Review And Handover, accepted with notes by QFIX-03 as AIDE-side handover evidence
- `Q27`: Commit Discipline And WorkUnit Recovery v0, accepted with notes by QFIX-03
- `Q28`: Git Workflow Policy v0, accepted with notes by QFIX-03 as report-only branch workflow governance
- `Q29`: Merge / Land / Promote Helper v0, accepted with notes by QFIX-03 as dry-run helper tooling with fixture-only mutation tests
- `Q30`: AIDE Dev/Main Policy Sync, accepted with notes by QFIX-03; live branch mutation remains separately gated
- `Q31`: Export Pack Sync for Git / Commit Workflow, accepted with notes by QFIX-03
- `Q34`: Changelog and Release Notes Generator v0, accepted with notes by QFIX-03 as preview-only release drafting
- `Q35`: GitHub Protection and CI Advisory v0, implemented as report-only branch-protection and CI gate planning with no GitHub API, workflow, branch, tag, release, provider, model, or network mutation
- `Q36`: Intent Compiler and Prompt Normalization v0, implemented for review as deterministic no-call prompt classification and WorkUnit draft generation with no raw prompt execution
- `Q37`: Repo Intelligence Index v0, implemented for review as deterministic file inventory, ownership, dependency, test, doc-link, generated-output, and orphan-candidate indexing with no file move, delete, refactor, migration, provider/model/network call, or target-repo mutation
- `Q38`: File Quality Ledger v0, implemented for review as deterministic advisory quality measurement over Q37 repo intelligence with no file move, delete, refactor, automatic repair, provider/model/network call, or target-repo mutation
- `Q39`: Refactor Control Plane v0, implemented for review as deterministic dry-run/no-apply refactor planning with move-map, salvage-map, path-alias, rollback-note, and migration-ledger schemas and no file move, delete, reference rewrite, migration apply, provider/model/network call, branch mutation, or target-repo mutation
- `Q40`: Root Recycling Framework v0, implemented for review as deterministic root inventory, root classification, per-file fate candidates, root risk summaries, exception records, and no-apply root plans with no root move, file delete, reference rewrite, tool absorption, provider/model/network call, branch mutation, or target-repo mutation
- `Q41`: Existing Tool Absorption v0, implemented for review as deterministic existing-tool inventory, capability classification, preservation fates, risk summaries, adapter maps, and no-execution wrap plans with no unknown tool execution, deletion, rename, migration, provider/model/network call, branch mutation, or target-repo mutation
- `Q42`: Move Map / Salvage Map / Path Alias v0, implemented for review as deterministic candidate map, alias, reference-rewrite, and draft migration-ledger planning with no file move, deletion, reference rewrite, alias/shim application, provider/model/network call, branch mutation, or target-repo mutation
- `Q43`: Install Plan Model v0, implemented for review as deterministic install observation, candidate install plans, dry-run reports, ownership ledgers, conflict reports, preservation reports, and verification plans with no install apply, overwrite, migration apply, file move/delete, reference rewrite, provider/model/network call, branch mutation, or target-repo mutation
- `Q44`: Repair / Doctor Model v0, implemented for review as deterministic repair observation, diagnosis, candidate repair plans, dry-run reports, doctor repair reports, and verification plans with no repair apply, overwrite, delete, migration apply, file move, reference rewrite, provider/model/network call, branch mutation, or target-repo mutation
- `Q45`: Upgrade Model v0, implemented for review as deterministic current-install observation, source-pack observation, compatibility comparison, candidate upgrade plans, dry-run reports, conflict reports, migration reports, and verification plans with no upgrade apply, overwrite, delete, migration apply, install/repair apply, file move, reference rewrite, provider/model/network call, branch mutation, or target-repo mutation
- `Q46`: Rollback / Uninstall Model v0, implemented for review as deterministic rollback and uninstall observation, preservation-first planning, dry-run reports, ownership-evidence gates, and verification plans with no rollback apply, uninstall apply, delete, overwrite, managed-section removal, file move, reference rewrite, provider/model/network call, branch mutation, or target-repo mutation

## Near-Term Phases

- run Q47 AIDE Lite Release Bundle v0 after Q46 so the portable bundle can carry install, repair, upgrade, rollback, and uninstall planning support without exporting source-generated target truth
- run Q32 Eureka Sync From Canonical AIDE Pack so Eureka receives the canonical portable governance surface and regenerates its own target-local reports
- run Q33 Dominium Sync From Canonical AIDE Pack after Eureka sync evidence is recorded
- continue Q32/Q33 target sync in the target repositories when explicitly run there
- review Q21 and Q24 while preserving the no-call/no-forwarding boundary
- generate future implementation prompts from compact task packets instead of long chat history
- deepen the existing native reference lanes where current proofs are blocked or only report-first
- bring archival or historical environments under tighter control-plane tracking and actual lab evidence
- tighten host-lane docs, matrix posture, and eval reports as implementation moves
- add lightweight maintenance support and repo audit discipline without jumping straight to CI

## Self-Hosting Reboot Queue

The reboot queue is defined in [docs/roadmap/reboot-roadmap.md](docs/roadmap/reboot-roadmap.md) and summarized in [docs/roadmap/queue-roadmap.md](docs/roadmap/queue-roadmap.md). It starts with Q00 baseline freeze and continues through documentation split, structural skeleton, profile contract, harness, generated artifacts, compatibility baseline, Dominium Bridge baseline, self-hosting automation, and token survival. Q02 adds skeleton directories only; the structural migration map lives at [docs/reference/structural-migration-map.md](docs/reference/structural-migration-map.md). Q03 adds the declarative Profile/Contract v0 and source-of-truth references. Q04 adds minimal executable Harness validation and reporting. Q05 adds generated artifact v0 markers, managed sections, preview-only Claude guidance, and drift checks. Q06 adds Compatibility baseline records and Harness checks without real migrations. Q07 adds AIDE-side Dominium Bridge metadata and structural Harness checks without modifying the Dominium repo or generating real Dominium outputs. Q08 adds report-first self-check automation without external workers, generated-artifact refresh, or autonomous service behavior. Q09-Q20 are accepted with notes as the token-survival foundation: compact packets, AIDE Lite, context compiler, verifier, evidence review, estimated token ledger, deterministic local golden tasks, advisory outcome and routing signals, cache/local-state boundary, local/report-only Gateway skeleton, and offline provider metadata. QFIX-01 reconciles that status truth. QFIX-02 establishes `py -3 .aide/scripts/aide_lite.py test` as the canonical AIDE Lite validation command and documents the old `-t .` unittest form as non-canonical. Q21 creates the portable AIDE Lite Pack and validates fixture imports before real target pilots. Q22/Q23 target imports have now run in Eureka and Dominium and await target-repo review. Q24 compiles compact existing-tool guidance as generated previews plus a safe AGENTS managed section. Q25 repairs pack integrity, default import scope, provenance reporting, and state-truth guidance. Q26 reviews the Eureka pilot evidence read-only. Q27 adds structured commit discipline, changelog preview, task resumption, WorkUnit idempotency, and recovery policy. Q28 adds branch workflow policy and report-only detection. Q29 adds dry-run-first Git helper plans and tests mutating land/promote/prune behavior only in temporary fixture repositories. Q30 records the AIDE-specific `main`/`dev` policy and confirms live `dev` setup remains a future explicit operator action, not an implicit branch mutation. Q31 exports the generic Q27-Q30 governance surface through the portable pack while keeping AIDE-specific live branch reports out of target truth. Q34 turns structured commits into preview-only changelog and release-note drafts while keeping release publishing, tags, and GitHub Releases deferred. Q35 adds report-only GitHub protection and CI advisory plans while keeping active GitHub settings, workflow files, tags, releases, and branch mutation deferred. Q36 adds a deterministic no-call intent compiler so raw prompts become reviewable intent packets and WorkUnit drafts before any implementation work begins. Q37 adds deterministic repo intelligence indexes so future quality and refactor phases can cite file inventory, ownership, dependencies, tests, docs, generated outputs, and conservative orphan candidates without moving or deleting files. Q38 adds deterministic advisory quality reports so future refactor planning can use visible warnings instead of broad cleanup prompts. Q39 adds a deterministic no-apply refactor control plane so later root recycling, tool absorption, move maps, salvage maps, path aliases, install, upgrade, and rollback phases can plan structural changes before applying them. Q40 adds a deterministic no-apply root recycling framework so root cleanup starts with root inventory, file fate candidates, risks, exceptions, and review-gated plans rather than root moves or deletion. Q41 adds deterministic existing-tool absorption planning so repositories with XStack, AuditX, RepoX, TestX, project validators, scripts, CI wrappers, or command catalogs can preserve and map those systems before any future wrapper execution or migration. Q42 adds candidate move, salvage, path-alias, reference-rewrite, and draft migration-ledger plans so future install and migration phases can reason about paths without applying changes. Q43 adds deterministic install observe/plan/dry-run outputs, ownership ledgers, conflict reports, preservation reports, and verification plans so target installs are preservation-first and reviewable before any future apply phase. Q44 adds deterministic repair observe/diagnose/plan/dry-run outputs, repair class gates, doctor repair reports, and verification plans so broken, partial, stale, or inconsistent AIDE installs can be diagnosed without applying repairs. Q45 adds deterministic upgrade observe/compare/plan/dry-run outputs, compatibility reporting, conflict reporting, migration gates, and verification plans so target updates are preservation-first. Q46 adds deterministic rollback and uninstall observe/plan/dry-run outputs, ownership-evidence gates, and preservation boundaries so removal and recovery are reviewable without deleting files or removing target state.

The staged view for later candidates lives in [docs/roadmap/staged-expansion-roadmap.md](docs/roadmap/staged-expansion-roadmap.md). Later tracks such as Runtime, CLI or Service surfaces, Commander, Mobile, IDE Hosts, Pack/Skill/Workflow IR, GStack/reference imports, provider adapters, app surfaces, and broader release automation remain deferred until queue evidence supports them.

## Medium-Term Phases

- add richer embedded or local-service execution paths where the current `cli-bridge` proof is only a first step
- expand verification from structural and smoke evidence toward stronger workflow-aware coverage
- mature packaging manifests, release-shape evidence, and release-readiness audits
- decide which candidate legacy families are strong enough for promotion into committed host work

## Long-Horizon Phases

- advance selected host lanes toward `L3` and `L4` where the host surface genuinely supports it
- broaden committed host-family coverage beyond the current Microsoft, Apple, and CodeWarrior set
- improve environment reproducibility for archival lanes that depend on preserved toolchains or media
- move from proof-oriented host work toward durable release posture where verification and packaging evidence justify it

## Committed Work Versus Candidate Work

Committed work today:

- shared-core boot slice
- Microsoft Visual Studio and Visual Studio for Mac lanes
- Apple Xcode lanes
- CodeWarrior lanes
- environment, evaluation, packaging, and maintenance control-plane work

Candidate or future research work today:

- broader legacy families tracked in `inventory/legacy-ide-families.yaml`
- deeper packaging automation
- broader release automation
- additional native interop surfaces and richer execution modes not yet implemented

## Major Unresolved Or Blocker Themes

- missing reproducible native environments for several archival or native reference lanes
- embedded or native interop paths that are still blocked while `cli-bridge` proofs exist
- limited packaging and release evidence for actual shipping posture
- environment acquisition and preservation costs for historical hosts
- later-era contract ambiguity inside some legacy umbrellas

## Roadmap Discipline

- Promote work only when research, manifests, matrices, and verification evidence support it.
- Keep blocked and deferred work explicit.
- Do not turn candidate families into implied commitments.
- Prefer phase completion evidence over breadth claims.
