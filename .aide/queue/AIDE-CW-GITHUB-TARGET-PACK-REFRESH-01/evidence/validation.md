# Local artifact qualification

Date: 2026-09-24 AEST. All command logs are retained outside the repository
under `D:\Projects\AIDE\_review_scratch\combined-*.log`.

- Changelog preview, validate, and status: PASS. Preview source `4deeed08`,
  50 commits in the window, zero malformed; preview-only and no publication.
- Export-pack: PASS from committed preview checkpoint `66ef462c`; 826 included
  files, boundary PASS. The only tracked export delta is `manifest.yaml` source
  commit `66ef462c2b1bf2e022bf7f575ff83299814ecd6b`.
- Pack-status: checksums PASS, provenance PASS before artifact commit, then
  `PASS_SOURCE_ANCESTOR` after artifact checkpoint `cda504b9`; boundary PASS.
- Release bundle, validate, draft, and draft-validate: PASS from source `66ef`.
  Local bundle id `aide-lite-pack-v0-66ef462c2b1bf2e0`.
- Independent final-byte check: nine asset records match file SHA-256 and byte
  size; seven checksum index records match files; zero mismatches.
- ZIP: SHA-256 `4b9e458fe4a3c5f67f862de9c443ea195f74df7dd0bd2d0b69a4406562fdb5d8`.
- tar.gz: SHA-256 `65fc3f78f719244695a80914e73d535269d486a754e61b7b0a102969705f9589`.
- Precommit second complete generator cycle: 44 tracked release paths compared,
  zero changed.
- First post-artifact-commit complete cycle: all four commands PASS, 18 of 44
  release paths changed as provenance projected to `PASS_SOURCE_ANCESTOR`.
- Second post-artifact-commit complete cycle: all four commands PASS, zero of
  44 release paths changed.
- Canonical validate and doctor: PASS before artifact commit and after the
  source-ancestor projection. Release status, assets, manifest, checksums,
  provenance, and `release clean --dry-run`: exit zero; clean deleted zero.
- Projection commit `d4bd4938fa4324f6dd8818ba4ce5ae38041bb897`
  replayed all four generators from a clean tree; all passed and zero of 44
  tracked release files changed.
- Final pack-status: checksum PASS, provenance `PASS_SOURCE_ANCESTOR`, boundary
  PASS. Canonical validate, doctor, release validate, and draft-validate: PASS.
  Independent asset checks still report nine plus seven exact matches.
- Direct current-byte ZIP fresh-project and tar.gz brownfield consumers both
  passed dry-run, `APPLIED`, idempotent `NO_CHANGES`, and target-local doctor.
  Brownfield owner memory, queue, and documentation files kept exact bytes;
  manual `AGENTS.md` text stayed intact before one AIDE managed section.
- The first canary script used an overly strict whole-file `AGENTS.md` equality
  oracle and stopped after the fresh-project pass. The inspected brownfield
  file retained the owner text. The corrected preservation oracle reran both
  archives successfully. This was a canary assertion correction, not a product
  source change.
- Exact external receipt:
  `D:\Projects\AIDE\_review_scratch\combined-consumers-a9a8b295a871\receipt.json`;
  repository copy: `combined-consumer-receipt.json`; both SHA-256
  `208498a897238d78d302bfc8c6b0f9e2c71d46863515f6f9b89cebaf8c9f78d6`.
- Final task-to-dev integration and remote observation remain pending.
