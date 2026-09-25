# Stable Lite contract artifact projection from clean source

## Source and command identity

Clean source `8365aa61b7cad51d542f88434e50bc33c5aac8fe`, tree
`38ee70fe857b951f45a3af3ed84bfa6210417534`, descends from exact
independently accepted contract source `d38e5839` and current
`dev@a32535a2`. `git status --porcelain=v1` was empty before generation.
The source CLI SHA-256 remained
`163d8e38bb3ad1f2d8ca2c29c9a946b733b1246c5bf55dfac647b7b693796b57`.

The six commands below ran serially via `py -3 -B .aide/scripts/aide_lite.py`
from the clean source; each exited 0. External log prefix:
`D:/Projects/AIDE/_review_scratch/stable-contract-projection-8365aa61-`.
The exact command/exit/log-hash receipt is external
`stable-contract-projection-8365aa61-commands.txt`.

| Command | Log SHA-256 |
| --- | --- |
| `export-pack` | `83151ebceb58573bc4f203f7f074c592a537726ef5c308e024f06e6363cb5a0d` |
| `changelog preview` | `c5654e323cc5c17a83bbef6cb11c5d05af096bc84ec92474f814b100ee2adc5c` |
| `release bundle` | `d26ec14f98a8a359121a2db16a1208d012406c5f4ecef2bcf08e1aa58a6e6fe8` |
| `release validate` | `8e0f105a0248c91c957c90ebcd1acf09012fa479f088fc3fb3f0fe78f6352a07` |
| `release draft` | `d8c9c7b0dd2a75cb3514f6a4f8d282c03b8f286da9db9ba61781fc31c8ba117d` |
| `release draft-validate` | `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de` |

## Local preview bytes and current gates

- ZIP SHA-256 `8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`.
- tar.gz SHA-256 `11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c`.
- `release-provenance.json` identifies source `8365aa61`,
  `dirty_state: false`, `preview_only: true`, `no_publish: true`.
- Before committing the generated projection, `pack-status` exited 0 with
  provenance and boundary PASS (log SHA-256
  `6dfead5e9ffb41f8a52d930554e3db5ba710ec78dc87266a9b3d7e5b304bc41d`);
  `validate` exited 0 and reported PASS
  (`8f29206e28139058f06530d39e09125c3e12d8a962b4034cb1309e15bf34a8a4`);
  `doctor` exited 0 and reported PASS
  (`fb45d4dced82b6048379b3e312071343c31700223ae72e3110082aaab7603887`).
- `git diff --check` passed; exactly 38 tracked generated paths changed, all
  under `.aide/changelog/**`, `.aide/export/**`, or `.aide/release/**`.

## Extracted artifact consumer

The previously independently reviewed external canary script SHA-256
`70c2e9dce144bf3bd3212dd5df3b20fb56726d5fe8249f7f135bfe38595fc0e4`
ran against those exact ZIP/tar hashes and source CLI bytes. Its first
invocation refused an output path outside its required `run-*` prep directory
before consumer execution; the corrected new path run exited 0 and reported
PASS. Run directory:
`D:/Projects/AIDE/_review_scratch/three-way-update-consumer-prep/run-stable-contract-8365aa61-20260925`.
`summary.json` SHA-256:
`047092b4695bbf72353ad8b5d4b30511c77c7cef6c312bc0b2101026853188fc`.
It observed 833 archive members and 25 delivered CLI commands: 20 exits 0,
five expected refusal exits 2. It covered fresh and brownfield imports,
direct edits, explicit conflict resolutions, successive synthetic updates,
disabled example preservation, read-only repair-health classification and no
feedback by default. The synthetic V2/V3 fixture packs are **not published
predecessor releases**. This is local preview evidence, not final downloaded
release qualification.

## Remaining gates

Commit the exact generated files, prove post-commit release metadata replay
and canonical checks, obtain independent exact artifact/dev-effect review,
and observe the qualified `dev` effect. Final version, support profile,
main/tag/publication and downloaded consumers remain separate.
