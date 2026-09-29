# API-set loader alternate-output replay regression

- Changed file: `evidence/h2_api_loader_effect_tests.py` only.
- Exact test commit: `81ddce079fc667e839ddebc2ea0adf5983b03428`,
  tree `c9e4101da712763273b898c5a8ee99e0d1a311d2`.
- New injected test: complete one request, retry the same request ID with a
  distinct empty output directory and confirm no backend call, alternate
  result or journal change. The original result remains byte-identical and
  reconcilable.
- Precommit D-managed command: `job run --config .aide.local/execution.json
  --manifest .aide.local/api-loader-effect-tests-job.json`; job
  `4a9051aebd0b464ab924da04e7d33cc1`, 10/10 PASS, receipt SHA-256
  `de2f4ce73602df3b6b82321d5ac658b756fcc61af16ac37cafaa86311bf9d0f9`.
- Postcommit same bounded command: job
  `49b237eaa0984b02bf7b3110bc1b2ede`, 10/10 PASS, receipt SHA-256
  `1c0e03bf45545135d264ad90b7f95c030b433641fb2872362c27d6a312f0e800`.
  Peak memory 30,044,160 bytes and peak scratch 254 bytes. Receipt reports
  exit zero, retired scratch and released reservation.
- `commit check --latest` and `git diff --check`: PASS.

Both runs used the injected `FakeLoader`; no native API-set load, restricted
principal, worker activation or effect admission occurred. The reviewed
driver/adapter source remains unchanged. Independent review of this regression
and an exact finite effect packet remain before any native call.
