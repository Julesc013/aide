# Validation Results

Commands executed on 2026-06-25:

- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01` -> PASS, status `needs_review`, classification `complete`, `missing_evidence: 0`.
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01` -> PASS, 13 evidence files, no missing evidence.
- `py -3 .aide\scripts\aide_lite.py install status` -> PASS, operations 462, conflicts 458, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py install validate` -> PASS, `target_mutation: false`, `overwrite_allowed_default: false`, `migration_automatic: false`.
- `py -3 .aide\scripts\aide_lite.py repair status` -> PASS, operations 11, conflicts 0, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py repair validate` -> PASS, `target_mutation: false`, `overwrite_allowed_default: false`, `delete_allowed_default: false`, `migration_automatic: false`.
- `py -3 .aide\scripts\aide_lite.py upgrade status` -> PASS, planned updates 5, skips 8, preservations 209, conflicts 209, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py upgrade validate` -> PASS, `target_mutation: false`, `overwrite_allowed_default: false`, `delete_allowed_default: false`, `migration_automatic: false`.
- `py -3 .aide\scripts\aide_lite.py upgrade compatibility` -> PASS, unsupported count 8, unknown count 0, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py rollback status` -> PASS, future actions 5, preservations 224, blockers 0, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py rollback validate` -> PASS, `target_mutation: false`, managed section removal disabled by default.
- `py -3 .aide\scripts\aide_lite.py uninstall status` -> PASS, future removal candidates 233, preservations 885, unknown ownership count 672, blockers 0, `no_apply: true`.
- `py -3 .aide\scripts\aide_lite.py uninstall validate` -> PASS, blanket `.aide` deletion forbidden and apply disabled.
- `py -3 .aide\scripts\aide_lite.py release status` -> PASS, bundle `aide-lite-pack-v0-2b2a00f7c4628311`, validation `PASS`, `no_publish: true`.
- `py -3 .aide\scripts\aide_lite.py release validate` -> PASS, tag creation, GitHub Release creation, and upload all false.
- `py -3 .aide\scripts\aide_lite.py release draft-status` -> PASS, draft `aide-lite-pack-v0-github-draft-2b2a00f7c4628311`, publication status `local_draft_no_publish`.
- `py -3 .aide\scripts\aide_lite.py release draft-validate` -> PASS, no tag, no GitHub Release, no upload, no network API call.

Final broad validation, diff checks, leak scans, and commit-policy checks are
recorded after this evidence update in the working terminal session and in the
commit record.
