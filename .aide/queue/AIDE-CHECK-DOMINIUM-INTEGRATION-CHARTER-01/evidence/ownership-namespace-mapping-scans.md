# Ownership, Namespace, And Mapping Scans

Result: PASS.

- Semantic owners remain separated: AIDE owns generic coordination/protocol/governance envelopes; Dominium owns product/domain semantics; Domino owns deterministic execution; Workbench owns presentation, context capture, approval interaction, and apply requests.
- No shared concept is jointly authoritative without a composition rule.
- Namespace owners are unique and fail closed for unknown IDs.
- `object-mapping.json` rows contain required fields for semantic owner, identity owner, source object, target reference, projection direction, allowed/forbidden transformations, version responsibility, evidence behavior, refusal behavior, and lifecycle relationship.
- Refusal mappings preserve owner, stable reason code, retryability, human action, mapped target shape, and evidence/event behavior.
