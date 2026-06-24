# State Safety Review

The source result records:

- before revision equals after revision
- `workspace_state_unchanged`: `true`
- `mutation_observation`: `none_detected_within_probe_coverage`

Declared probe coverage is Git revision, porcelain status, tracked tree digest,
and selected command digests. The check preserves the limitation that ignored
files, external databases, and files outside the workspace are not proven.
