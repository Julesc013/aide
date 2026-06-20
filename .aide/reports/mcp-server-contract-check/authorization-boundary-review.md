# Authorization Boundary Review

The contract distinguishes MCP transport authorization expectations from AIDE
operation authorization.

Authorization remains not implemented:

- no OAuth flow
- no client registration
- no token issuance, parsing, or storage
- no credential resolution
- no authorization server discovery
- no PolicyDecision or CapabilityGrant fabrication

Future endpoint access would not replace AIDE policy, grant, admission, and
evidence checks.
