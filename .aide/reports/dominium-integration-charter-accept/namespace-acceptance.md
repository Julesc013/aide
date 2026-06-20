# Namespace Acceptance

Namespaces remain owner-scoped:

- AIDE owns `aide://` references.
- Dominium owns command, service, document, refusal, and diagnostic IDs.
- Domino owns capability and process IDs.
- Workbench owns host, workspace, view, and action IDs.
- Bridge mappings are future bridge-owned records.
- Artifact, evidence, and event refs remain producer/domain-owned.

File paths are not stable identity. Unknown required IDs fail closed.
