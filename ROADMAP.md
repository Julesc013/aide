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
- `Q09`: state reconciliation and token-survival core for compact packets, approximate token estimates, evidence review, and no-history guidance, awaiting review
- `Q10`: AIDE Lite hardening for deterministic pack/adapt/validate/estimate/snapshot/selftest behavior, awaiting review
- `Q11`: Context Compiler v0 for deterministic repo-map, test-map, context-index, latest-context-packet, and exact refs, awaiting review

## Near-Term Phases

- review Q11 Context Compiler v0 evidence before Q12 Verifier v0
- generate future implementation prompts from compact task packets instead of long chat history
- deepen the existing native reference lanes where current proofs are blocked or only report-first
- bring archival or historical environments under tighter control-plane tracking and actual lab evidence
- tighten host-lane docs, matrix posture, and eval reports as implementation moves
- add lightweight maintenance support and repo audit discipline without jumping straight to CI

## Self-Hosting Reboot Queue

The reboot queue is defined in [docs/roadmap/reboot-roadmap.md](docs/roadmap/reboot-roadmap.md) and summarized in [docs/roadmap/queue-roadmap.md](docs/roadmap/queue-roadmap.md). It starts with Q00 baseline freeze and continues through documentation split, structural skeleton, profile contract, harness, generated artifacts, compatibility baseline, Dominium Bridge baseline, self-hosting automation, and token survival. Q02 adds skeleton directories only; the structural migration map lives at [docs/reference/structural-migration-map.md](docs/reference/structural-migration-map.md). Q03 adds the declarative Profile/Contract v0 and source-of-truth references. Q04 adds minimal executable Harness validation and reporting. Q05 adds generated artifact v0 markers, managed sections, preview-only Claude guidance, and drift checks. Q06 adds Compatibility baseline records and Harness checks without real migrations. Q07 adds AIDE-side Dominium Bridge metadata and structural Harness checks without modifying the Dominium repo or generating real Dominium outputs. Q08 adds report-first self-check automation without external workers, generated-artifact refresh, or autonomous service behavior. Q09 adds repo-only token-survival packets and evidence-review discipline without Gateway or provider work. Q10 hardens AIDE Lite so compact packet generation, adapter updates, validation, snapshots, estimates, and selftests are repeatable. Q11 adds deterministic context compilation through repo-map, test-map, context-index, latest-context-packet, and exact refs before Q12 verifier work.

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
