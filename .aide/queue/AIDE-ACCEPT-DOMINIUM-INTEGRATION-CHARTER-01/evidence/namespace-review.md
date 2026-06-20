# Namespace Review

Accepted namespace ownership:

- `aide://` references remain AIDE-owned.
- Dominium command, service, document, refusal, and diagnostic IDs remain Dominium-owned.
- Domino capability and process IDs remain Domino-owned.
- Workbench host, workspace, view, and action IDs remain Workbench-owned.
- Bridge mapping IDs are future bridge-owned mapping records.
- Artifact, evidence, and event refs remain producer/domain-owned with AIDE references.

Identity is not a file path. Silent remapping is forbidden. Unknown required IDs fail closed.
