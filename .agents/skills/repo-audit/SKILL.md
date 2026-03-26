---
name: aide-repo-audit
description: Use when performing a structured AIDE repository-state review for documentation coherence, inventory or matrix drift, host-lane freshness, maintenance hygiene, or explicit blocked and deferred status checks.
---

## Scope

- `evals/reports/**`
- `scripts/maintenance/**`
- root control-plane coherence review
- repo-state audit work spanning docs, matrices, manifests, and reports

## Trigger

- when a prompt asks for an audit, repo-state review, consistency check, or phase summary
- when cross-document or cross-matrix drift must be identified explicitly
- when blocked, deferred, committed, and candidate posture must be reviewed together

## Do Not Use

- Do not use this skill for ordinary implementation work with no audit component.
- Do not use this skill as a substitute for running concrete verification commands.
