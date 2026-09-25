# Independent Windows staging-race reproduction

The independent reviewer `/root/owned_repair_integration_review` reproduced
the issue against the exact accepted source file in `e4697aaa`, source file
SHA-256 `7ad3469af3d57544226a9ec348713dd69136b8406353c643adbc4f43105d74f3`.
While `atomic_create_bytes_no_clobber` held its `tempfile.mkstemp`
descriptor, a same-user child opened the staging path and changed
`EXPECTED` to `ATTACKED`. The helper returned success and published
`ATTACKED` through its no-replace link. A later payload digest may detect
this only after altered bytes are visible; repair intent has no immediate
equivalent check.

Durable disposable proof outside the repository:

- `D:/Projects/AIDE/_review_scratch/owned-repair-stage-share-repro.py`,
  SHA-256 `e3f234b4ca4413ef1f8d86a6b66f150263a229f4741f638f2ce7cc5779637cc5`.
- `D:/Projects/AIDE/_review_scratch/owned-repair-stage-share-repro.log`,
  SHA-256 `ef232eeb817ad87120a24e6fc45064070f10b50d43013a545091b97dce37572c`.

The reviewer prototyped exclusive Windows `CreateFileW` staging with
`GENERIC_READ|GENERIC_WRITE|DELETE`, share mode `0`, `CREATE_NEW`, and
`FILE_ATTRIBUTE_NORMAL`. Its second writer was denied while the expected
bytes linked successfully. The fix must preserve that exclusion from stage
creation through publication, or an independently verified equivalent
handle-bound invariant. Both intent and managed payload require a regression.

The prior `ACCEPT_WITH_NOTES` is retained as historical review evidence but
is superseded for repair write safety. Dev `9a8b0870` contains the affected
source; main and public release remain untouched.
