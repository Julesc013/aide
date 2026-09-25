# Combined removal artifact checkpoint

Date: 2026-09-25. Status: accepted local artifact for bounded dev integration
qualification; not dev, main, native/hosted, or stable-release acceptance.

## Frozen source and outputs

- Source commit `49318d50472b17f648c2f29e998239b9c446cf14`, tree
  `c89e391e607ccb536162cf3f1a6880f1aa4235a7`, clean at generation.
- ZIP SHA-256 `e7e14b8e112ddcd762022c26b59deaa3aff1b49f69950fc2f4751e7fedf3e8c8`.
- Tar SHA-256 `06852530d459271184022d17a11f514a8402351354683cae49899678100f0699`.
- Archive `install.md` SHA-256
  `bd959bc85ddc36c2f870bb3cec5d6bfa3f5c182ed0f57239937a03a32d7fce53`;
  release sidecar `install.md` SHA-256
  `8bf5e95ded5572a4bf2b7b5f61bc171d51b0a7103d27a8e6285b8ce41df93b19`.
- Export, changelog preview, release bundle/validate, draft/draft-validate,
  pack-status, and canonical `validate` all returned PASS. Generated records
  retain local preview/no-publish status.

## Independent review chain

- `00966855` local artifacts: REQUEST_CHANGES for contradictory generated
  install guides. External review SHA-256
  `441859e99ce3654aa06ef934e2c1bee889ca9467e3c70444a475c2c46f40abf5`.
- `597b5bcd` guide source: REQUEST_CHANGES for planner marker and recovery
  ambiguity. External review SHA-256
  `f7fd10bed7066d9ddcd1e69eec46fb742acf9379a99f5946cfe329ec594482d7`.
- `49318d50` corrective source delta: ACCEPT for artifact construction.
  External review SHA-256
  `e07a9b508737cc67c8e1d221ee1481298566c202e28af9d7a1909d2711145eb8`.
- Exact new local artifacts: ACCEPT_WITH_NOTES for bounded dev integration
  qualification. External review
  `D:/Projects/AIDE/_review_scratch/removal-combined-49318d50-artifact-review.md`,
  SHA-256 `82bfa83747b962348c5f8d9afb53edc038f07eae6fefe739aa640076e4749c71`.
  Its reviewer independently checked 833 equal regular ZIP/tar members,
  source parity, all checksum layers, provenance, corrected guides, Q31/Q47
  logs, and all 27 consumer command-record hashes.

## Tests and consumers

- The `00966855` combined source passed 67/67 importer tests before the later
  guide-only source changes. Its retained log SHA-256 is
  `98a0c187a67472cf6abce69acfac54715ea5ad1e19038ae04aea4c71134ec08b`.
  A new full importer run against `49318d50` is active and not yet an outcome.
- Exact-source generated-guide regression 1/1 PASS; Q31 6/6 PASS, log SHA-256
  `a5457474dc8563b1b6cda93036eb199c51528d4dac2a6e0c57e81f6f554315d9`;
  Q47 18/18 PASS, log SHA-256
  `f0f7f0d4dcddb3b052a912c614512b7f6081d4e9e61dea00414172b6835844aa`.
- Exact ZIP/tar external canary: 27 delivered CLI commands, exit 0, PASS for
  fresh DETACHED, authored brownfield PARTIAL_REMOVAL, changed-path refusal,
  one-delete interruption resume, and receipt-boundary recovery. Verdict
  `D:/Projects/AIDE/_review_scratch/removal-combined-consumer-prep/run-49318d50-20260925/qualification-verdict.json`,
  SHA-256 `0ae1a590ef13ce6f8cabb491e149d54e9b1165194ecfbd08fe079fc98348f528`.
  Invocation log SHA-256
  `c3e6a37979f24cb4abbe1dbe01f816f05ece9be1423f4150b1208b36d922aad4`.

## Remaining gates and limitations

The generated artifact projection needs an exact commit and post-commit replay,
then an independent exact dev effect review. Removal apply is Windows-only.
Authored `AGENTS.md` managed-section removal is not implemented; partial apply
retains that file, runner, and receipt. Effect-time edits and interruption
used deterministic same-process/API injection rather than a hostile OS process.
No OS-level offline trace or native-host/hosted qualification is established.
