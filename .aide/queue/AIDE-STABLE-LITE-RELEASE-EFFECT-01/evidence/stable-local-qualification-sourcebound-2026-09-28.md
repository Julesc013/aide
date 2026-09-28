# Source-bound Lite 1.0.0 local qualification

This is a superseding **local candidate**. The previously accepted `719abf66`
effect and the first renewed candidate are retained as historical evidence;
neither verdict applies to these changed bytes. No tag or publication occurred.

## Frozen identities

- Reviewed removal and runner source ancestry: `b95a8f9a`; no implementation
  source changed after that reviewed branch in this candidate.
- Changelog preview source: `aab07569`; only five generated changelog paths
  changed before pack source `d0c8f62ce94465a6c174de4e931db10d1ba451ea`,
  tree `1c19d575ec6e68da9ccbb38b4d97b7306f911639`.
- Current export pack commit: `0d2d31187e64b9f6dc42f982ac3ee338a2711689`;
  `pack-status` passed checksum, provenance and boundary checks.
- Stable asset commit: `3dfb30723e88be89daa346146f37ca3607c214a8`,
  tree `caa9d282e438fafbf207421fc726e3531d8590c0`.
- Local release preview commit: `7ffd1260107d6d17e39a0c9a00b5ccf0e05a05d9`.
  Local no-publish draft commit: `debb409ca4b71007ea6c628a7c923731d3a77be1`.
- Stable ZIP SHA-256: `a762c816295a90e09db97ce7e56443272ce19fd5aa581ffccdb6081e1a75836a`.
  Stable tar.gz SHA-256: `a8e7bd38114e4761257ca0c4514985c39cf651ff4d2ae79d8ed12b86ed9b869f`.
  Exact four asset paths and hashes are in
  `release-effect-manifest-1.0.0-sourcebound.json` (SHA-256
  `6e7a9d4e54cedf1e6eccc000d0e4073a14552586baca302c9444ce6f7b855aa0`).

## Managed D-root qualification

| Scope | Job ID | Result |
| --- | --- | --- |
| Export pack | `4b632d9774e748d8b47c2a5ecc5449c9` | PASS |
| Stable build / postcommit replay / validator | `43c2db82e6b24224a311fa508c873e0b`, `b3b6e45212b040bfa60464d6b47c5884`, `8f09cd9cff0148dc9edd7d6212379317` | PASS; replay changed zero tracked files |
| Local preview bundle / postcommit replay / validation | `a90b8fc2101c441c8c1d9f76a57cf42e`, `8897da4c4de1400db8f2a4450226950b`, `9eca3890b2364a8b861409d68eb36d1f` | PASS; replay changed zero tracked files |
| Local draft / postcommit replay / validation | `b4e1c7f3e8d74384a773caa77a2aba48`, `61352448f67b4f31a4e69611971189a4`, `9c8dfaac5d4c423eaeef237a73f68894` | PASS; replay changed zero tracked files |
| Fresh/brownfield ZIP and tar consumer | `143fc8d4e1b14b4bb77265b2a54fa12e` | PASS |
| Repair, rollback, detach/removal consumer | `15cc213fe559465ba3f4b5baf7cd94a4` | PASS |
| Context and offline consumer | `c88b28d0545942c7b59b4dbb79efe270` | PASS with classified verify warnings |
| Public partial recovery and feedback consumer | `664f96ddba5e470b940d3e6bd529eb3f` | PASS |
| Public validate, task and feedback consumer | `f9e83751edd4488fb0c5766676b02e98` | PASS with two classified validate warnings |
| Forced child-exit recovery consumer | `977daa0b2eac443fb136c72049686386` | PASS |
| Current Q47/Q48 release regression suite | `8fc7369a750343ccb7baefdbbbeea7f1` | PASS, 36 tests |

All 17 successful jobs exited zero, became quiescent, retired scratch and
released their shared reservation. The six consumer jobs operated serially
on these exact asset hashes. The effect manifest binds their receipts and
all 28 declared public CLI forms to 39 retained command files, checking
each file's digest, recorded exit code and expected output marker. The largest
observed consumer scratch peak was 33,745,416 bytes and the largest observed
consumer memory peak was 298,598,400 bytes. These are runner observations,
not claims of OS-native network isolation or atomic crash durability.

The fresh and brownfield `verify` results remain WARN with 15 and 18
classified optional/context warnings; installed `validate` exited zero with
two classified warnings. The prior 110 importer cases remain historical
because repository inputs changed; reviewed changed-scope tests and current
delivered-byte consumers are recorded separately in the effect manifest.

An earlier bundle job `eca5b52ca0c44d53b6d6c80808543d9f` failed the
correct preview source-binding check. Its validation was retained under the
approved D control root. Reordering the preview before the clean pack source
resolved the failure. An initial consumer job
`95e6ae1dd1b543eda516113eb18a696d` failed because the local canary was
given the pack projection commit instead of the pack's clean source commit;
the corrected consumer job above passed. A local driver error before
consumer 3 launched was corrected and no product test was repeated for it.

## Remaining gates

Independent exact release/effect ACCEPT is required before `dev`
integration. Ten historical-message owner dispositions and a passing
`main..dev` commit-message range check are still required before main
promotion. Tag, publication, remote download and installed downloaded-byte
consumer verification have not occurred. Isolated-host, hosted, model-enabled
autonomous and non-Windows lifecycle guarantees remain outside this Lite
profile and separate programme obligations. The wider goal remains active.
