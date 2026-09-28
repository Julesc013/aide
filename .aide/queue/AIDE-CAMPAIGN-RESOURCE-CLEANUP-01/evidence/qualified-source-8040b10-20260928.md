# Frozen runner source and partitioned importer qualification

Candidate `8040b10a5d2c894e4f78b234d6fb55ed9403d391`, tree
`8d1e7e3b91137a5b6f9b55d186044537f446056f`, parent `e18f983b09378131c55d8a3ed7daed3521a243b9`.
The checkout stayed clean throughout both importer partitions.

Independent reviewer `/root/transient_scan_review` returned
**ACCEPT_WITH_NOTES** for bounded source continuation and integration. The
controller-transcribed external record is
`D:\Projects\AIDE\.aide.local\execution\control\reviews\transient-scan-8040b10-review.md`,
SHA-256 `0b0b1919e17ba4a43b3605293702536132808860e966d96e9b6d23c769a57d1c`.
The reviewer ran read-only Git/source checks, no tests. Their test-strength
note asks for deterministic queued-directory and `os.scandir` race coverage;
it is a follow-up, not a blocking source finding. It does not accept a release.

The frozen `test_export_import.py` defines 110 test methods. A deterministic
AST/name partition assigned each method exactly once: A–M 54, O–Z 56. Both
jobs used the same reviewed commit/tree, Python executable digest and shared D
config digest `217a27d429c199879648dde2c943026d37ea6fc52d9d80d5add98ad21fed20f1`.
The manifests bind 925 source/dependency/oracle inputs. No source file changed
while either job ran.

| Partition | Manifest SHA-256 | Job | Result | Receipt SHA-256 |
| --- | --- | --- | --- | --- |
| A–M, 54 cases | `e9aabd2d998523990e6bf8b8bab87c6e7cbdaf4f4328b9cce428fd4b9a69168f` | `690f26f2e69e45fc84413bdb9c9b3097` | 54 passed, 0 skipped; 2,589.603 s | `d9292c448dadb280e886777234bb5e5f4336315fedfc07a5412e891957f0690b` |
| O–Z, 56 cases | `e56cbc5e52786cc880914bb8c8c4c4bbaa91c79556f559f955d9f0787d9f143b` | `673c9cc6696a42739d9734679c0868ad` | 56 passed, 0 skipped; 3,218.922 s | `44895fc4fe59a7206562695746e2a4c66ab021a96f6934a4f7ebc17459185c79` |

Both jobs exited zero, retired scratch, released reservations and retained
bounded logs. Their respective peak memory was 247,599,104 and 242,806,784
bytes; peak scratch was 20,669,481 and 35,783,220 bytes. This is 110/110
source cases through **two disjoint processes**, not a single-process run.
The earlier E attempt that stopped after 99 completed cases remains an
incomplete historical attempt; its failure and custody are recorded separately.

Next: record the exact source qualification in the partial-recovery WorkUnit,
fast-forward only if current dev ancestry and remote state permit it, then
regenerate current pack/release outputs with the accepted generator under D
canonical-output reservations. Delivered new/brownfield consumers and final
release gates remain open. Do not use stale preview archives for acceptance.
