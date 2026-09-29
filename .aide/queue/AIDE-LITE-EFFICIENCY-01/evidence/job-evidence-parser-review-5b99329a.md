# Managed job evidence parser repair, 2026-09-29

- Exact reviewed source: `5b99329a3e56c5fcc9e48835d8f6aab90365cbc2`,
  tree `e6f256af090e12f684ae79f43a8569c5b0a892ec`, parent
  `dev@6795abab31b41963b8aa5ab1b0eedcd997f13a26`.
- Before repair, a receipt containing duplicate `phase` keys returned a false
  terminal `PASS` in the focused regression. After repair, the observer
  reports `EVIDENCE_UNAVAILABLE` for that record. The same parser also rejects
  nonfinite JSON and recursion, bounds the read, and checks file identity.
- D-managed postcommit job `52700025edf04124b78ca15824c69753` ran the
  focused efficiency suite: **27/27 PASS**, exit 0. Retained receipt SHA-256
  `f45f0ec0e7f998ec62cbb30373e99f81e24337d531f837140f277235ef2b36be`.
  Peak memory was 262,926,336 bytes and peak scratch 4,856 bytes. The job
  retired scratch and released its reservation. The receipt binds the source,
  command, Python executable, inputs, environment and configured D roots.
- `git diff --check` and the structured commit check passed.
- Independent `/root/stable_effect_review` returned **ACCEPT for dev source
  integration** of the exact commit and tree. The reviewer checked the diff,
  malformed input behavior and managed receipt; no live model turn or release
  regeneration was performed. File identity checks are best-effort race
  detection, not a filesystem transaction.

The current frozen Lite ZIP and technical release verdict bind older CLI bytes.
This source verdict does not qualify those assets or publication; changed
delivered bytes require their own generation, consumer checks and acceptance.
