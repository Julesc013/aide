# Remaining Risks

- Q46 has no apply mode. Real rollback and uninstall remain future reviewed
  phases.
- No real target repo rollback or uninstall has been exercised.
- Rollback quality depends on ownership ledger, install plan, upgrade plan, and
  repair plan quality; missing evidence remains conservative.
- Uninstall remains intentionally conservative for unknown ownership.
- Generated current AIDE rollback/uninstall plans are evidence only, not target
  truth.
- `core/gateway/tests` discovery timed out after 900 seconds during final
  validation; Q46 did not edit Gateway code.
- Harness validate/doctor/self-check retain the pre-existing stale generated
  manifest fingerprint warning.
- `repo validate` retains pre-existing unknown file classification warnings.
- Q47 is still needed to define the AIDE Lite Release Bundle v0; Q46 only
  provides rollback/uninstall planning support.
