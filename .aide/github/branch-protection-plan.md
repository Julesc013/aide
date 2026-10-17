# AIDE GitHub Branch Protection Plan

- schema_version: aide.github-branch-protection-plan.v0
- generated_by: aide-lite
- repo_id: Julesc013/aide
- current_branch: task/aide-git-defaults-01
- current_branch_role: task
- github_api_mutation: false
- branch_protection_applied: false
- workflow_file_written: false
- preview_only: true
- remote_protection_observed: false
- policy_issues: []

## Branch Targets

- main: role=canonical; present=true; protection=false; choice=project_optional; force_push=false; deletion=false
- dev: role=integration; present=true; protection=false; choice=normally_unprotected; force_push=false; deletion=false
- release/*: role=release; present=false; protection=true; choice=project_policy; force_push=false; deletion=false
- hotfix/*: role=hotfix; present=false; protection=true; choice=project_policy; force_push=false; deletion=false
- gh-pages: role=deploy; present=false; protection=true; choice=project_policy; force_push=false; deletion=false

## Required Status Checks

- aide-validate
- aide-lite-validate
- aide-lite-test
- aide-lite-eval
- commit-check
- changelog-validate
- git-policy
- github-validate
- pack-status
- secret-scan

## Boundary

This is an advisory plan. Q35 does not call GitHub APIs, create branch
protection rules, write `.github/workflows`, push branches, create tags, or
publish releases.
Project-owned protection choices come from `.aide/policies/branch-protection.yaml`.
Existing remote protection is preserved; optional or disabled hosting protection
does not bypass validation, review, no-force-push or persistent-branch retention.
