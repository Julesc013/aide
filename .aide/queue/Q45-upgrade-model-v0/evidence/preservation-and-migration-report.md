# Preservation And Migration Report

## Preservation Rules

Q45 preserves target-specific state by default, including:

- target `.aide/memory/**`
- target `.aide/queue/**`
- target `.aide/context/latest-*`
- target `.aide/reports/**`
- target `.aide/evals/golden-tasks/**` target-specific tasks
- target `.aide/git/latest-*`
- target `.aide/repo/file-inventory.json`
- target `.aide/roots/latest-*`
- target `.aide/tools/latest-*`
- target `.aide/install/latest-*`
- target `.aide/repair/latest-*`
- target `.aide/upgrade/latest-*`
- manual `AGENTS.md` content outside managed sections
- target docs, doctrine, and existing tools
- `.aide.local/**`, `.env`, secrets, raw prompts, and raw responses

## Current Plan Findings

- preserved paths in plan: 865
- required migration candidates: 8
- optional migration candidates: 201
- source-generated exclusions: 8
- automatic migrations: false

## Mandatory Migration Gate

Mandatory migrations are only planned when old or copied state is unsafe, unsupported, validation-blocking, ambiguity-creating, source-state contamination, command-blocking, or conflicting with canonical AIDE ownership. Q45 does not apply those migrations.

## Optional Migration Gate

Optional migrations are deferred for compatible legacy naming, compatible policy drift, target-local extensions, or generated packets that can be regenerated later.
