# Remaining Risks

- The backend's proposed capability label must be relabeled before acceptance.
- The AIDE implementation currently treats any parsed Dominium command JSON as
  enough to mark command and service boundaries as reached. This invocation is
  independently corroborated by Dominium source, but generic process
  infrastructure should use adapter-specific boundary evidence.
- The backend source contains a temporary local Dominium checkout fallback. That
  is acceptable for the current bridge proof but must not move into generic
  process infrastructure.
- Dominium aggregate validation remains unavailable for this target and is
  Dominium-owned work, not an AIDE repair.
