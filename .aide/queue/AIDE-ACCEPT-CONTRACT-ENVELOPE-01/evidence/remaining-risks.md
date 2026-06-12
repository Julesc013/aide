# Remaining Risks

## Non-Blocking

1. PyYAML is unavailable in this environment.
   - Severity: low.
   - Mitigation: stdlib structural YAML checks, task inspection/evidence
     validation, repo validation, and tests passed.

2. Full JSON Schema Draft 2020-12 validation remains deferred.
   - Severity: low for this accepted minimal slice.
   - Mitigation: local subset validation covers the current required envelope
     fields and records limitations explicitly.

3. Minimal envelope is `v1alpha1`, not a full public protocol stability claim.
   - Severity: low.
   - Mitigation: keep explicit non-capabilities and compatibility metadata in
     follow-up EvidencePacket work.

## Blocking

None.
