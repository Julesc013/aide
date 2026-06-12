# Remaining Risks

## Non-Blocking

1. PyYAML is unavailable in this environment.
   - Severity: low.
   - Mitigation: stdlib structural YAML checks, queue task inspection, task
     evidence validation, repo validation, and focused tests passed.

2. Full JSON Schema Draft 2020-12 validation remains deferred.
   - Severity: low for the current minimal envelope slice.
   - Mitigation: the local subset validator covers the currently required
     public envelope fields and records its limitations explicitly.

3. SemVer compatibility semantics are helper-enforced rather than fully encoded
   in the minimal schema subset.
   - Severity: low for the current slice.
   - Mitigation: keep this explicit until a full schema engine or richer schema
     validator is intentionally introduced.

4. Initial lightweight scan commands produced syntax failures or false positives
   before corrected/refined scans were run.
   - Severity: low.
   - Mitigation: final refined scans passed, and the failed attempts are
     recorded in the check report.

## Blocking

None.
