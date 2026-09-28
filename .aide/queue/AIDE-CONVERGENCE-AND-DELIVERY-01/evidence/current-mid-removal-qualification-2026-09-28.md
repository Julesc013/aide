# Current frozen-asset mid-removal qualification

- Frozen asset: `.aide/release/stable/aide-lite-v1.0.0.zip`, SHA-256
  `a762c816295a90e09db97ce7e56443272ce19fd5aa581ffccdb6081e1a75836a`,
  matching the source-bound release-effect manifest. The archive and product
  source were not changed.
- Canary source commit `800d67911546312d66267ae8418fbc30d738db58`,
  tree `4be4d25f17f2c4ecd24e872be9722b08de1b5fa3`. Its test script input
  SHA-256 is `fa0c54511323d873289b6f50dda71eff973637f6740768e9ce997b47573b1110`.
- AIDE-managed D job `539db05c6c2c4c389a42b6d2e8ce186f` exited 0,
  quiescent, scratch absent and reservation released. Manifest digest:
  `6f33c77381d25291d3b4c192bf485c06f80d20b9f5f792101d12a8498c4e615d`.
  Retained receipt SHA-256:
  `27a28b607ac61eacf8ab555c0a808b8ae32bfac60d3c7c5f8a01fb34e0595f10`.
  Retained result JSON SHA-256:
  `ae49c8bae8ce8bcd5d89470574f2b61e58c253554bcff1dde926ae3f592982d8`.
  Peak job memory was 246,206,464 bytes; peak scratch was 8,357,969 bytes.
- The canary inspected and extracted 835 archive members into its owned
  scratch, installed 812 managed files into an authored brownfield project
  through the delivered CLI, and obtained an exact removal plan. A child
  process exited **77** immediately after unlinking the receipt-owned
  `.aide.local.example/README.md`. That file was absent; removal intent and
  import receipt remained; authored and project-owned bytes were unchanged.
  A fresh delivered CLI process resumed the same plan to **DETACHED**. Final
  checks found no receipt-owned files or removal state, and preserved authored
  `AGENTS.md` and project-owned bytes.
- The first job `041b0300374e44748acb8acd6c8b13cc` exited 1 before
  installation because the initial harness passed unsupported `--json` to
  `import-pack`. It is retained as a harness failure, with scratch retired and
  reservation released. Commit `800d6791` corrected only the harness parser.
- This is one local Windows brownfield deletion point from exact frozen bytes.
  It does not prove every deletion point, hostile concurrency, non-Windows
  behavior, publication or consumers of downloaded assets.

Independent reviewer `/root/stable_effect_review` accepted the exact canary
commit/tree as **additional local Windows delivered-byte mid-removal evidence
only**. The reviewer independently checked the ZIP, receipt, and retained
result hashes, job exit, scratch retirement, and substantive recovery oracle.
The reviewed effect is the local ZIP and one forced exit after the first
receipt-owned file unlink. The review does not establish arbitrary crash
timings, remote download, or full release acceptance. The archive extractor
is only qualified here for the known SHA-bound ZIP, not arbitrary input.
