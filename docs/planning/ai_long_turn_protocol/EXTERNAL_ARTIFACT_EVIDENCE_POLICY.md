# External Artifact Evidence Policy

Manual or external artifacts must remain distinct from repo-local planning
language.

## Evidence States

- `lead`: a possible source or artifact.
- `collected`: an artifact or summary has been returned.
- `reviewed`: a human or approved process checked it.
- `verified`: validation proved the artifact supports the claim.
- `rejected`: the artifact does not support the claim or cannot be trusted.

Do not collapse these states.

## Required Fields

Returned evidence should identify:

- source or owner
- collection date
- artifact identity
- hash or stable locator when available
- reviewer
- validation command or method
- remaining uncertainty

## Stop Conditions

Stop when evidence is absent, stale, unverifiable, outside the allowlist, or
requires secrets, protected assets, target mutation, provider/model calls,
Gateway calls, or network behavior not authorized by the WorkUnit.
