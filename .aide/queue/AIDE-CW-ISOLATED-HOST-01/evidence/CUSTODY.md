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

## H2 source custody

The three H2 authored files and current raw evidence are preserved in
h2-source-evidence.zip; h2-custody.json lists exact member bytes/SHA256s and
raw-to-LF Git text projections. Original on-disk logs remain unstaged. A raw file
absent after checkout resolves to evidence/<its basename> in that packet.

The two superseded source/reproduction packets remain separate and immutable:
h2-before-root-alias-evidence.zip and h2-before-overlap-evidence.zip, each with its
matching custody map and 12 original members. Those are historical review states,
not additional passing qualification. The current packet also retains exact
original attack intent bytes copied read-only from their retained fixtures.
All H1 packets above remain unchanged. The next Python closure proposal carries
source-only authority and no new native image/profile/launch effect permission.

## H2 Python source packet

The current h2-python-evidence.zip and h2-python-custody.json preserve original
source, tests, the complete patch, independent review/probe scripts and results,
all helper output and initial mutation failure. The 4.9 MB validate outputs are
archive members only; raw working files remain retained and unstaged. Original
evidence paths referenced by the manifest/review resolve to ZIP members under
files/. Extract only a requested member into a separately owned evidence root;
do not overwrite current canonical documents to replay historical observations.

The map gives each original path, byte length and SHA256, plus raw-to-LF Git
projection bindings for selected human-readable evidence. Archived original bytes
remain authoritative for their recorded raw hashes. Source/dependency snapshots
and a copy of the unchanged pending-provider index are historical inputs, not
new queue authority or a staged canonical index change. The v1 baseline files
used by the independent differential oracle are under baseline/06f2546f/.
No private tool images, DLL loads, package grants or runtime activation occurred.
