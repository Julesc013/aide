# Uninstall Dry-Run Design

This WorkUnit reviews uninstall planning as static fixture evidence. It does not execute uninstall or delete files.

## Scenario Classes

- `uninstall-manual-preserved`: report-only plan for removing AIDE-owned generated content while preserving manual content.
- `broad-delete-blocked`: report-only blocked scenario proving broad delete requests are blocked before mutation.

## Required Properties

- Fixture-only target class.
- Explicit paths.
- Protected roots listed.
- Broad-delete stop conditions present.
- Manual content preservation recorded.
- No uninstall execution.
- No lifecycle apply.
- No scoped transaction apply against fixture targets.
- No target repo mutation.
