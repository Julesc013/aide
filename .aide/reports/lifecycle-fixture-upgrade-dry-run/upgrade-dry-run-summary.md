# Lifecycle Fixture Upgrade Dry-Run Summary

Task: `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`

Result: `PASS_WITH_WARNINGS`

Review gate: `needs_review`

Upgrade scenarios checked: 3

- `upgrade-v2`: PASS_WITH_WARNINGS, path PASS, managed PASS, hash PASS, mutation PASS, expected report present
- `upgrade-manual-preserved`: PASS_WITH_WARNINGS, path PASS, managed PASS, hash PASS, mutation PASS, expected report absent
- `drift-detected`: BLOCKED, path PASS, managed PASS, hash PASS, mutation PASS, expected report present

Warnings:

- upgrade-manual-preserved: static expected report ref absent

Defects:

- none

No upgrade apply implementation or execution occurred. No lifecycle apply execution occurred. No scoped transaction apply against fixture targets occurred. No fixture target mutation through apply, active repo apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply occurred.

Capability labels remain `upgrade-dry-run-checked`, `upgrade-report-checked`, `fixture-upgrade-planned`, `dry-run-planned`, `report-backed`, `schema-validated`, `locally-validated`, and `review-gated`; upgrade apply and lifecycle apply remain planned-only.
