# Q31 Portable Boundary Report

## Included Portable Classes

- Commit message policy, checker support, commit template, and hook template.
- Changelog preview command support and reference docs.
- Task resumption, WorkUnit idempotency, and recovery policies.
- Generic Git workflow, branch-role, promotion, sync, and prune policies.
- Dry-run Git helper policy and command docs.
- Project workflow profiles for AIDE, Eureka, Dominium, website/static-site,
  native-client, connector-heavy, data-snapshot, and unknown repos.
- Governance golden tasks and relevant AIDE Lite tests.
- Portable `docs/reference/**` docs needed by target repos.

## Excluded Source-Specific Classes

- `.aide/git/workflow-detection.json`
- `.aide/git/workflow-detection.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`
- `.aide/git/aide-branch-policy.yaml`
- `.aide/git/aide-dev-main-plan.json`
- `.aide/git/aide-dev-main-plan.md`
- `.aide/changelog/*.preview.md`
- `.aide/changelog/changelog.preview.json`
- `.aide/changelog/malformed-commits.md`
- `.aide/queue/**`
- `.aide/context/latest-*.md`
- generated reports/status outputs
- `.aide.local/**`
- `.env`
- `secrets/**`
- raw prompts and raw responses

## Boundary Proof

- `export-pack`: PASS, boundary PASS.
- `pack-status`: PASS, boundary PASS, 0 boundary violations.
- `eval run`: PASS, `export_pack_excludes_source_branch_state_golden`
  passed 37/37 checks.
- Q31 fixture import tests verify imported targets receive governance files
  without receiving AIDE-specific generated branch reports or helper plans.

## Target-State Rule

Target repositories must regenerate their own branch detection, helper plan,
snapshot, index, task packet, review packet, eval reports, and evidence after
import. AIDE-generated reports are source outputs, not target truth.
