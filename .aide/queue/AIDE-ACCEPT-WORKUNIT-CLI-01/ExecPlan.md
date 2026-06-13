# ExecPlan: AIDE-ACCEPT-WORKUNIT-CLI-01

Objective: perform a check-only acceptance review for the read-only WorkUnit CLI chain.

Scope:
- Verify BUILD and CHECK commits, reports, command behavior, path safety, source queue traceability, compatibility, and no-forbidden-ops boundaries.
- Create acceptance report/evidence only.
- If accepted, update reviewed task statuses according to existing queue convention.

Validation intent:
- Run direct PowerShell `py -3` commands required by the acceptance prompt.
- Parse generated JSON reports.
- Compare representative source queue hashes before and after command probes.
- Restore generated report churn outside the acceptance deliverables before committing.

Stop state: `needs_review`.
