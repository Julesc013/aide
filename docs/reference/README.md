# AIDE Reference Documents

## Purpose

This family holds operational references, maps, and user or developer guides that do not belong to a narrower implementation, governance, host, or research tree.

## Current References

- [Self-Bootstrap Guide](self-bootstrap.md): how the filesystem queue was created and how Q00 prompts work.
- [Repository Census](repo-census.md): Q00 top-level repository map and reboot classification.
- [Documentation Migration Map](documentation-migration-map.md): old/current documentation areas mapped to Q01 documentation families.
- [Structural Migration Map](structural-migration-map.md): Q02 map from bootstrap-era physical locations to target skeleton conceptual homes.
- [Terminology](terminology.md): canonical reboot vocabulary.
- [Command Reference](command-reference.md): current and future command-reference posture.
- [Generated Artifacts](generated-artifacts.md): future generated-output reference posture.
- [Token Survival Core](token-survival-core.md): Q09/Q10 compact packet, token estimate, and evidence-review operating guide.
- [AIDE Lite](aide-lite.md): Q10 no-install helper command, determinism, drift, and selftest guide.
- [Context Compiler v0](context-compiler-v0.md): Q11 repo-map, test-map, context-index, exact-ref, and context-packet guide.
- [Verifier v0](verifier-v0.md): Q12 mechanical verification guide for evidence packets, task packets, diff scope, file refs, secret safety, and compact reports.
- [Evidence Review Workflow](evidence-review-workflow.md): Q13 compact review-packet guide for evidence-only GPT-5.5 or human review.
- [Token Ledger](token-ledger.md): Q14 estimated token ledger, baseline comparison, budget status, regression warning, and no-raw-prompt storage guide.
- [Golden Tasks v0](golden-tasks-v0.md): Q15 deterministic local golden-task quality gates and eval list/run/report workflow.
- [Outcome Controller v0](outcome-controller-v0.md): Q16 advisory outcome ledger, local signal readers, recommendation rules, and self-optimization safety boundary.
- [Router Profile v0](router-profile-v0.md): Q17 advisory route classes, hard floors, model/provider metadata, route decisions, and no-live-call safety boundary.
- [Cache and Local State Boundary](cache-local-state-boundary.md): Q18 `.aide.local/` boundary, cache-key metadata, cache reports, and no-secret runtime-state guide.
- [Gateway Skeleton](gateway-skeleton.md): Q19 local/report-only Gateway policy, architecture, status endpoints, AIDE Lite commands, and provider-forwarding deferrals.
- [Provider Adapter v0](provider-adapter-v0.md): Q20 offline provider-adapter contracts, provider catalog, capability metadata, no-call commands, and credential boundary guide.
- [Cross-Repo Pack Export / Import v0](cross-repo-pack-export-import.md): Q21/Q25/Q31 portable AIDE Lite Pack workflow, governance include/exclude boundary, fixture import validation, and target initialization guide.
- [Existing Tool Adapter Compiler v0](existing-tool-adapter-compiler-v0.md): Q24 compact guidance compiler for Codex, Claude Code, Aider, Cline, Continue, Cursor, and Windsurf preview or managed outputs.
- [Commit Discipline](commit-discipline.md): Q27 structured commit format, checker commands, hook template, and changelog-ready body rules.
- [WorkUnit Idempotency](workunit-idempotency.md): Q27 task no-op, resumption, recovery, and evidence-first behavior.
- [Changelog Preview](changelog-preview.md): Q27 deterministic changelog and release-note preview workflow.
- [Git Workflow Policy](git-workflow-policy.md): Q28 branch model, report-only detection, sync policy, and future helper boundary.
- [Branch Roles](branch-roles.md): Q28 canonical, integration, task, review, release, hotfix, deploy, and unknown role semantics.
- [Promotion Policy](promotion-policy.md): Q28 task-to-dev and dev-to-main gates plus prune and release-line boundaries.
- [Git Helper Workflow](git-helper-workflow.md): Q29 dry-run-first `git plan/sync/land/promote/prune` helpers, fixture-only mutation tests, and live-repo safety boundaries.
- [AIDE Dev/Main Workflow](aide-dev-main-workflow.md): Q30 AIDE-specific branch posture, current missing-`dev` plan, promotion gates, and no-live-mutation boundary.
- [Intent Compiler](intent-compiler.md): Q36 deterministic prompt normalization, task/risk/size classes, latest intent packet workflow, and no-raw-prompt-execution boundary.
- [Repo Intelligence Index](repo-intelligence-index.md): Q37 deterministic file inventory, ownership/dependency/test/doc maps, generated-output boundaries, conservative orphan candidates, and no-move/no-delete command workflow.
- [File Quality Ledger](file-quality-ledger.md): Q38 deterministic advisory file quality records, warning/candidate language, generated reports, and no-fix/no-delete boundary.
- [Refactor Control Plane](refactor-control-plane.md): Q39 dry-run/no-apply refactor planning, move/salvage/path-alias schemas, migration ledger records, and root-recycling inputs.
- [Root Recycling Framework](root-recycling-framework.md): Q40 deterministic root inventory, root classification, file fates, root risks, exceptions, and no-apply root plans.
- [Tool Absorption](tool-absorption.md): Q41 deterministic existing-tool inventory, capability classification, preservation fates, and no-execution wrap planning.
- [Move/Salvage/Path Aliases](move-salvage-path-aliases.md): Q42 candidate move maps, salvage maps, path alias plans, reference rewrite plans, and draft migration ledgers.
- [AIDE Install Model](aide-install-model.md): Q43 install observe/plan/dry-run lifecycle, preservation rules, ownership ledgers, and conflict reports.
- [AIDE Repair / Doctor Model](aide-repair-model.md): Q44 repair observe/diagnose/plan/dry-run lifecycle, repair classes, hard blockers, and advisory doctor reports.
- [AIDE Upgrade Model](aide-upgrade-model.md): Q45 upgrade observe/compare/plan/dry-run lifecycle, compatibility categories, preservation rules, and migration gates.
- [AIDE Rollback / Uninstall Model](aide-rollback-uninstall.md): Q46 rollback and uninstall observe/plan/dry-run lifecycle, ownership evidence requirements, preservation boundaries, and no blanket `.aide` deletion.

## Queue Guide

The canonical queue guide remains [.aide/queue/README.md](../../.aide/queue/README.md). Reference docs may summarize it, but `.aide/queue/` remains the source of truth.
