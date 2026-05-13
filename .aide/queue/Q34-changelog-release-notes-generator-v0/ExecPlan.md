# Q34 ExecPlan: Changelog and Release Notes Generator v0

## Objective

Make structured AIDE commits operational by generating deterministic preview-only changelog and release-note drafts from local Git history.

## Scope

- Add Q34 queue evidence and keep status at a review gate.
- Add changelog policy, config, templates, preview outputs, and malformed-commit reporting.
- Harden AIDE Lite changelog parsing, preview generation, validation, and status commands.
- Add deterministic tests and golden tasks for changelog and release-note behavior.
- Export portable changelog support while excluding generated source-repo previews from target truth.
- Update compact documentation and prepare the Q35 task packet.

## Non-Goals

- No release publishing, tag creation, GitHub Release creation, branch mutation, provider/model calls, network calls, or history rewrite.
- No product runtime, Gateway, host, Commander, mobile, installer, CI, or GitHub protection implementation.

## Dependencies

- Q27 commit discipline is present and `commit check` works.
- Q31 export pack synchronization is present and `pack-status` passes with recorded dirty-source provenance.
- Existing Q28-Q30 Git workflow tooling remains report-only.

## Execution Steps

1. Record baseline repo state and validation.
2. Add queue packet, policy, config, and templates.
3. Extend AIDE Lite changelog parser/generator commands and shared parser helpers.
4. Add tests and golden tasks.
5. Update docs and export/import policy.
6. Regenerate changelog previews, export pack, Q35 compact task packet, and evidence.
7. Run validation and stop at `needs_review`.

## Validation Plan

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 .aide/scripts/aide_lite.py eval run`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~10..HEAD`
- `py -3 .aide/scripts/aide_lite.py changelog preview`
- `py -3 .aide/scripts/aide_lite.py changelog validate`
- `py -3 .aide/scripts/aide_lite.py changelog status`
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
- `py -3 .aide/scripts/aide_lite.py pack-status`

## Progress

- [x] Baseline repository state inspected.
- [x] Baseline validation run before edits.
- [x] Q34 packet committed.
- [x] Changelog generator implemented.
- [x] Tests and golden tasks pass.
- [x] Documentation and export pack updated.
- [x] Evidence complete and status set to `needs_review`.

## Review Gate

Q34 stops at review. Preview artifacts are drafts only and are not official release notes.
