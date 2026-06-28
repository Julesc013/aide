# Validation Results

Passed:

- Python compile checks
- focused DistributionApplyEngine tests
- `distribution-apply status`
- `distribution-apply plan --scenario managed-file-update`
- `distribution-apply run --scenario managed-file-update --mode apply-temp`
- `distribution-apply verify`
- predecessor regression validation
- Q43-Q48 no-apply/no-publish validators
- broad `aide_lite.py validate`

Failed semantic check:

- isolated adversarial binding probes found six probe failures grouped into four material findings.

Notes:

- The Q43-Q48 validation command exited successfully. A broken-pipe style message was observed only after output truncation in the shell pipeline and is not treated as a validator failure.
- No implementation repair was performed.
