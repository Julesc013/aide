# Q41 Export Pack Sync

Export command:

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Exported Portable Q41 Files

- `.aide/policies/tool-absorption.yaml`
- `.aide/policies/tool-inventory.yaml`
- `.aide/policies/tool-fates.yaml`
- `.aide/policies/tool-wrapping.yaml`
- `.aide/policies/tool-risk.yaml`
- `.aide/policies/tool-capabilities.yaml`
- `.aide/tools/*.schema.json`
- `.aide/tools/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q41_tool_absorption.py`
- `.aide/evals/golden-tasks/tool_*`
- `docs/reference/tool-absorption.md`

## Export Boundary

The export pack does not export source-generated Q41 tool inventories or plans
as target truth:

- `.aide/tools/latest-tool-inventory.*`
- `.aide/tools/latest-tool-classification.*`
- `.aide/tools/latest-tool-wrap-plan.*`
- `.aide/tools/latest-tool-adapter-map.*`
- `.aide/tools/tool-risk-summary.md`

Target repositories must generate their own tool inventories and wrap plans
after importing the portable support.
