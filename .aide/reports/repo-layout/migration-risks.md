# Repository Layout Migration Risks

- task_id: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01
- report_only: true
- no_apply: true

## High-Risk Areas

### `.aide/reports`

Risk: high.

Reason: 102 top-level files, 52 directories, mixed `-check`, `-accept`, and
`-acceptance` suffixes, plus 365 hardcoded flat check/accept path references
across 156 files.

Required before movement:

- report index;
- no-apply reference map;
- compatibility plan for historical evidence paths;
- queue/evidence reference sweep;
- OKF and core helper path sweep;
- validation that old evidence remains inspectable.

### `.aide/tmp`

Risk: medium.

Reason: tracked files exist under temporary-looking paths, but they appear to be
fixture-like WorkUnit CLI mutation inputs.

Required before movement:

- fate classification;
- fixture/evidence/example ownership decision;
- reference sweep;
- rollback or alias plan if paths are consumed by tests.

### `core/runtime`, `core/sdk`, `core/control`

Risk: medium.

Reason: stubs exist before full runtime or SDK authorization. They should not
grow by accident during Track B.

Required before expansion:

- explicit Track A or architecture queue authority;
- capability boundary;
- validation plan.

### Duplicate Names Across `.aide` And `core`

Risk: medium.

Reason: `protocol`, `knowledge`, `providers`, `gateway`, `compat`, `apply`, and
`tests` appear in both `.aide` and `core`.

Required before movement:

- source/state/helper authority matrix;
- import and path reference scan;
- no-apply move map if consolidation is proposed.

## Validation Plan For Future Migration

Any future rationalization task should run:

```powershell
git status --short --branch
py -3 .aide/scripts/aide_lite.py repo inventory
py -3 .aide/scripts/aide_lite.py repo validate
py -3 .aide/scripts/aide_lite.py roots inventory
py -3 .aide/scripts/aide_lite.py roots classify
py -3 .aide/scripts/aide_lite.py roots validate
py -3 .aide/scripts/aide_lite.py refactor map
py -3 .aide/scripts/aide_lite.py refactor validate-map
rg ".aide/reports/"
rg ".aide/protocol|core/protocol"
py -3 .aide/scripts/aide_lite.py task inspect --task-id <TASK-ID>
py -3 .aide/scripts/aide_lite.py task evidence --task-id <TASK-ID>
git diff --check
```

## No-Apply Rule

This risk report does not authorize movement, deletion, rewrite, aliasing,
shimming, root creation, report restructuring, or rationalization apply work.
