# D placement and transient scratch scan, 2026-09-28

Owner selected the shared `D:\Projects\AIDE\.aide.local\execution` roots for
scratch, retained output and control. Both existing ignored checkout configs
match the actual D volume and have config digest
`217a27d429c199879648dde2c943026d37ea6fc52d9d80d5add98ad21fed20f1`.
The D control handover retains the exact old E config. New D admissions did not
overlap the prior intensive E importer job. The finite limits and volume-bound
inspection are in that local handover receipt; no fallback pool was used.

The full importer attempt `7be365cdba6540bf874d51e24d5410d5`, bound to
source `e18f983b09378131c55d8a3ed7daed3521a243b9` and its 918-input
manifest, ended with runner `FileNotFoundError` while scanning a test-created
scratch fixture. The retained stderr records 99 completed `ok` cases, zero
completed failures, and an unfinished next case; this is **not** a passing full
suite. Peak memory was 240,074,752 bytes and peak scratch 28,741,135 bytes.
The runner retired scratch and released its reservation. Its 139,196-byte,
five-file retained result was copied from E to D with every file SHA-256
verified; the E original remains. D receipt SHA-256:
`4d83913b70e8d7955c4d02610b1813ed9d1f5d9ca633d301d0b3ac8f8a89b35c`.

The precise scan race was reproduced on D by job
`34da1cb2b95140ccb3f8799fe6350c99` (expected one-case error). Source
changes make only the **active scratch monitor** tolerate an entry or queued
directory disappearing during enumeration. Strict scans for canonical and
retained evidence still raise on a missing member, and link/reparse refusal
remains. The green one-case job `9ae8281eee8c4b63ba0b9fe1c921bf14` passed;
its receipt SHA-256 is
`2017793800a7133e4911a82e99010e132b3a1e28a90758ee2c43901aaf61dbf3`.

Affected bounded D suites passed:

- `test_managed_workspace.py`: 26 tests, no skips, job
  `68c1d0e679ae46a2af14257ec63a7b86`, peak memory 211,599,360 bytes,
  peak scratch 4,531 bytes, receipt SHA-256
  `39d4196eae31b533a32b70ca86d717db14d86049085d2e3865131b7f2ffeeaae`.
- `test_cache_local_state.py`: 9 tests, no skips, job
  `e5e51faf285b4ea4868fa59c11e9ec9e`, peak memory 208,842,752 bytes,
  peak scratch 1,690 bytes, receipt SHA-256
  `b7646b263d031fd73b5315b5131390256413fec69d2ec532f30bc0358ba6d54e`.

Both completed jobs retired scratch and released reservations. The actual
prior consumer with absent optional cache reports now says `missing` at WARN;
the source checkout with present reports says `exists` at PASS. No severity or
release acceptance changed. The D manifests bind 924 actual precommit source,
dependency and oracle inputs. This precommit evidence is **not** mislabeled as
a frozen source commit. Freeze this candidate, obtain narrow independent review
of the monitor change, then run the 110 importer cases in bounded partitions
from the reviewed source. Current package and delivered-byte qualification
remain open.
