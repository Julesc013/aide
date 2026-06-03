# Command Surface Review

- result: PASS_WITH_WARNINGS
- command_mode: report_only_and_fixture_only
- active_repo_apply_command_found: false

## Commands

| Command | Result | Boundary |
| --- | --- | --- |
| `managed-section status` | supported | report-only |
| `managed-section validate` | supported | report-only |
| `managed-section fixture-plan` | supported | fixture-only |
| `managed-section fixture-verify` | supported | fixture-only |

## Boundary Findings

- Commands write deterministic source-side reports.
- Fixture commands use fixture roots and do not patch active repository files as product behavior.
- No command was found for active repository managed-section apply.
- No command was found for install, repair, upgrade, rollback, uninstall, branch/worktree, target, release, GitHub, provider/model, network, or Gateway behavior.
