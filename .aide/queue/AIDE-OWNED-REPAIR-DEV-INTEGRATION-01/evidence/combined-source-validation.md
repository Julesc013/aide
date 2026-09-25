# Combined owned repair source validation

The precommit merge uses base `5dfa75e632b09f732a8150376db6840bcf149ed3`,
admission `d40c18ccc7442a57b474d0f4a18db44016ca899a`, and reviewed repair
closeout `cdb3bd04f1ae20f4e58529f7132c376fcbdc48c6`. The source reviewed
independently was `45c5ce91132a00012dcf15e4ca38aa007afb8359`, tree
`b119a52d6aa85cf5acbcb627d860e2bf09810159`. The merged staged tree
before this evidence update was `4d87e9ad1d0acf0c0510ec13cf9de6a29fb69bef`.
Both CLI commands, both test streams, queue records, and later dev generator
were preserved. No old generated export/release outputs were staged.

| Check | Result | External log SHA-256 |
|---|---|---|
| Combined `test_export_import.py` | PASS, 42 tests, 618.355s | `38c588fdb9832cded4184c430b55fa5ab1037045d3e6f42f62533d1c7511461f` |
| Q47 release bundle | PASS, 18 tests | `fe2db0c01e683ae89257d27d3807c21a8262e320ae82050df557dc43d045edce` |
| Q48 release draft | PASS, 11 tests | `c5f5b6b6403e8611c5d1f85d7bc580e546b45a3e6fb0ffd03063ad5cbc19361c` |
| Q31 export governance | PASS, 6 tests | `0c430487b313c3ec3fa1cf9ae793954b21f2b8b35195a0278c86e74433277664` |
| Q34 changelog release | PASS, 11 tests | `76450222949863ca2868e01368560048356932a9748168afa64242b22ab75884` |
| Canonical validate | PASS | `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789` |
| Canonical doctor | PASS | `39b60ae17063c2a82dd16d576ad43c990abe7a4bb9054acf8e66fa223f37d0fb` |
| Repair source commit range | PASS, four structured messages | `24dc252e3bb6eb9d7b9b85b66be3911aa8d9b3ee5ac97da7b5f673a88a0d6d1e` |

All source logs are preserved under `D:/Projects/AIDE/_review_scratch/` with
`owned-repair-combined-` prefixes. The six tracked changelog previews
rewritten by Q34 tests were restored to the clean premerge HEAD after the test.
Python compilation, staged diff whitespace, conflict-marker, and unmerged-path
checks passed. The merge commit, current-source export, local release bytes,
extracted consumers, postcommit replay, and independent combined review remain
pending. This evidence qualifies source behavior only.
