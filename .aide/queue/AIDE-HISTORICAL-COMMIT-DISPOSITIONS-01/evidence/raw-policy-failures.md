# Raw Historical Commit-Message Failures

Date: 2026-09-22

These results were reproduced with dispositions disabled. They are immutable
input to the proposed decisions, not passing validation evidence.

## `bfb86c12b9e6d2970024d29c57ba629994ec43cc`

- Subject: `chore(git): synchronize accepted worker foundation ancestry`
- Tree: `54ab832eafa0ed0be3282858fd44f344e560732b`
- Ordered parents:
  - `02e99d267b14dc7dfedbd42262d390a93eac354f`
  - `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`
- Canonical message SHA-256: `24d6d65e72424b7fca5dac30ebe638b2f7a16266d2c4e8e114dbb9bd6e0c380c`
- Raw result: `FAIL`
- Exact failed check:
  - `validation section records PASS/WARN/FAIL/NOT RUN outcome`
- Command:
  - `py -3 -B .aide/scripts/aide_lite.py commit check --range bfb86c12b9e6d2970024d29c57ba629994ec43cc^! --no-dispositions`

## `486e81cd3a918729f28e4b452a9dcff017238a04`

- Subject: `feat(pack): add receipt-backed removal planning`
- Tree: `796f5aafc0d350e8cef599cacb9b3f703f8b2bb1`
- Ordered parent:
  - `ea98dc1c004e2a1cdf83fee69b63976825dc175e`
- Canonical message SHA-256: `71bcd1ba685a049c535e20244f65b29a1fef4299d4a0811f0c43031bd3b4dca0`
- Raw result: `FAIL`
- Exact failed checks:
  - `commit body heading has bullet content: ## Summary`
  - `commit body heading has bullet content: ## Why`
  - `commit body heading has bullet content: ## Validation`
  - `commit body heading has bullet content: ## Changelog`
  - `commit body heading has bullet content: ## Risks`
  - `commit body heading has bullet content: ## Follow-up`
  - `changelog section uses a machine-readable category prefix`
  - `commit trailer present: AIDE-Task`
  - `commit trailer present: AIDE-Phase`
  - `commit trailer present: AIDE-Result`
  - `commit trailer present: AIDE-Scope`
  - `commit trailer present: AIDE-Token-Impact`
  - `commit trailer present: AIDE-Quality-Gate`
- Command:
  - `py -3 -B .aide/scripts/aide_lite.py commit check --range 486e81cd3a918729f28e4b452a9dcff017238a04^! --no-dispositions`

## Interpretation

- Neither historical commit message passes the current standard.
- No commit was amended, replaced, or rewritten.
- Any accepted disposition must preserve these exact failures in range output.
- The disposition mechanism cannot establish product, runtime, or release
  qualification; those claims require their own evidence.

