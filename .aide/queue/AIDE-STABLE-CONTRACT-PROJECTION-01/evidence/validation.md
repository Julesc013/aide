# Exact projection and dev validation, 2026-09-25

## Reviewed objects

- Accepted contract source `d38e5839fe102fd4b38dc29971877753ccb6e2ec`,
  tree `cee0ddf6800b3cb29cf192ae5ac6e9f0da684457`; independent source
  `ACCEPT` report SHA-256
  `882d9a18ff1d94dec626e4ae646f27fa74bcadadc125cfe1d43c49280940c38e`.
- Frozen projection and metadata candidate
  `2defcad541d02cd33fabf75e20c48dfd091ffabe`, tree
  `14b13c209a4aaae7842fc7a58ce18b614005bae2`, ten commits after base
  `a32535a2675f191ae3515f39501658e91ef41103`.
- Independent exact artifact `ACCEPT_WITH_NOTES` and conditional dev-effect GO:
  `D:/Projects/AIDE/_review_scratch/stable-contract-projection-2defcad5-independent-effect-review.md`,
  SHA-256 `531744866cca3d9ee5dfc67ce27b99a77535bf24e4f6fce50806beabc30ca52e`.
  Notes are classified in that report and remain release obligations.

## Machine and consumer results

- Clean-source six-command generation and release validation: all exit 0;
  exact logs/hashes in `projection-8365aa61.md`.
- ZIP SHA-256 `8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`;
  tar.gz SHA-256 `11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c`.
  Independent review checked 833 equal safe members, 830 embedded checksums,
  nine asset hashes and seven release-core checksums.
- Extracted ZIP/tar canary: 25 commands, 20 success and five expected
  refusals, 833 equal members; summary SHA-256
  `047092b4695bbf72353ad8b5d4b30511c77c7cef6c312bc0b2101026853188fc`.
  Its V2/V3 update packs were disposable synthetic fixtures.
- First post-projection release replay exited 0 but changed 18 metadata
  files; that **failed** the zero-diff gate and is retained in
  `postcommit-convergence.md`. After commit `2defcad5`, the second four
  release commands exited 0 and changed **zero tracked or untracked files**.
  External receipt:
  `D:/Projects/AIDE/_review_scratch/stable-contract-projection-2defcad5-replay2-commands.txt`.
- On committed `2defcad5`, `pack-status` exit 0,
  `PASS_SOURCE_ANCESTOR`/boundary PASS, log SHA-256
  `17eb7a713285498d636c31fd8f0e50e9b1a632f16f230bd1f2db48a19f2bb673`;
  `validate` exit 0/PASS, log SHA-256
  `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789`;
  `doctor` exit 0/PASS, log SHA-256
  `fb45d4dced82b6048379b3e312071343c31700223ae72e3110082aaab7603887`.
- Q47 release tests 18/18 PASS, log SHA-256
  `48609afb07fda07f6226553591a1b40abbcda7801da750d93218bf2bfe1799c7`;
  Q48 draft tests 11/11 PASS, log SHA-256
  `a71f17cb9cffa80112019a920b68ec1a487ced9ece3625323a6ed23669459d09`.
  `commit check --range dev..HEAD` on exact candidate passed 10 commits,
  log SHA-256 `d00c612481a71995e9922a09cb9b8376c593aade04c3d3a756814601c079def8`.
  `git diff --check` and clean candidate status passed.

## Effect observation

Fresh pre-effect Windows/GitHub identity, one `dev` worktree, clean primary
and candidate, no shared Git lock/operation marker, exact tree/ancestry,
review/manifest/archive hashes, and four base ref reads passed. Local
fast-forward and normal push each exited 0. Local `dev`, `origin/dev`,
`git ls-remote`, and GitHub API all then returned full `2defcad5`, tree
`14b13c20`; primary was clean. External exact effect log SHA-256
`324fe2eae0e7d9d8d4e42bce602e6fd43ae1f9928358413e8081abc68155fb6d`.
This is dev source/local-preview integration, not stable release acceptance.
