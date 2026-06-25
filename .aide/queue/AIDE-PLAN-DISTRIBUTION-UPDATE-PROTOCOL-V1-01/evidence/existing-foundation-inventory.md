# Existing Foundation Inventory

The v1 plan reuses the existing lifecycle and release foundations.

## Q43 Install

- Status command: `py -3 .aide/scripts/aide_lite.py install status`
- Observed: observation, plan, and dry-run present.
- Counts: operations 462; conflicts 458.
- Boundary: `no_apply: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py install validate` returned
  `PASS`.

## Q44 Repair / Doctor

- Status command: `py -3 .aide/scripts/aide_lite.py repair status`
- Observed: observation, diagnosis, plan, and dry-run present.
- Counts: operations 11; conflicts 0.
- Boundary: `no_apply: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py repair validate` returned
  `PASS`.

## Q45 Upgrade

- Status command: `py -3 .aide/scripts/aide_lite.py upgrade status`
- Observed: current observation, source observation, comparison, plan, and
  dry-run present.
- Counts: planned_updates 5; planned_skips 8; planned_preservations 209;
  planned_conflicts 209.
- Boundary: `no_apply: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py upgrade validate` returned
  `PASS`.

## Q46 Rollback

- Status command: `py -3 .aide/scripts/aide_lite.py rollback status`
- Observed: observation, plan, and dry-run present.
- Counts: future_actions 5; preservations 224; blockers 0.
- Boundary: `no_apply: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py rollback validate` returned
  `PASS`.

## Q46 Uninstall

- Status command: `py -3 .aide/scripts/aide_lite.py uninstall status`
- Observed: observation, plan, and dry-run present.
- Counts: future_removal_candidates 233; preservations 885;
  unknown_ownership_count 672; blockers 0.
- Boundary: `no_apply: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py uninstall validate` returned
  `PASS`.

## Q47 Release Bundle

- Status command: `py -3 .aide/scripts/aide_lite.py release status`
- Observed: bundle `aide-lite-pack-v0-2b2a00f7c4628311`.
- Counts: artifact_count 11.
- Boundary: `no_publish: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py release validate` returned
  `PASS`.

## Q48 Release Draft

- Status command: `py -3 .aide/scripts/aide_lite.py release draft-status`
- Observed: draft `aide-lite-pack-v0-github-draft-2b2a00f7c4628311`.
- Counts: asset_count 12.
- Boundary: `publication_status: local_draft_no_publish`; `no_publish: true`.
- Validation: `py -3 .aide/scripts/aide_lite.py release draft-validate`
  returned `PASS`.
