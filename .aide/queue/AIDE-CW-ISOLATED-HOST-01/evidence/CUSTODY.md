# H1 original-byte custody

Current scope is the exact native host mechanism/local-endpoint probe. The host
WorkUnit remains running/PENDING; no private toolchain/model/credential-host or
operational qualification is implied. Earlier failures remain failures.

| Packet | Original result | Map | Members |
| --- | --- | --- | --- |
| h1-first-attempt-evidence.zip | FAIL, pending connect | h1-first-attempt-custody.json | 53 |
| h1-network-attempt-evidence.zip | FAIL, timeout-only | h1-network-attempt-custody.json | 40 |
| h1-diagnostic-attempt-evidence.zip | FAIL, NETISO_NONE | h1-diagnostic-attempt-custody.json | 43 |
| h1-interface-attempt-evidence.zip | PASS, exact native conjunction | h1-interface-attempt-custody.json | 69 |

Every map pins archive SHA256, exact member paths, lengths and raw SHA256 values.
The fourth packet references and preserves the preceding three. Repeated member
names across packets represent explicitly different historical snapshots; use
the map belonging to the named packet. No archive is silently rewritten.

Current source8 is under source/<repository-path> in the fourth packet. Exact
native binary, reservation, receipt, stdout/stderr and scratch proof are under
owned/. Source/effect/review manifests and raw test/helper logs are under evidence/.
Checkpoint document bytes are under checkpoint-docs/. Current text files beside
these ZIPs are navigation projections; Git text normalization cannot replace raw
archive hashes. If a cited raw file is absent after checkout, resolve the exact
named member through its packet map. Original on-disk evidence remains unstaged.

The fourth receipt retains network10060 as timeout, with diagnostic0/2 meaning
missing internetClient, both same-listener controls and the remaining actual
identity/access facts. The first three overall FAIL results are not relabeled.
All consumed effect manifests refuse replay; retained objects/profiles have no
automatic deletion authority. The source-manifest qualification text records
its pre-effect freeze; validation.md and actual result review give later truth.

Next source-only design: h2-private-toolchain-proposal.md and its read-only local
input inventory. No additional isolation/runtime/credential effects have run.
