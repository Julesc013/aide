# Validation

PASS_WITH_WARNINGS. `worker-run status/project/validate`, `aide_lite.py validate`, `aide_lite.py test`, build task inspect/evidence, and commit check all passed. Unsupported `worker-run run/start/claim/lease` and `workunit claim/run/finish/repair` fail closed with exit code 2. Non-blocking warnings: minimal schema subset, stale latest task packet, restored generated report churn, and corrected harness probe predicates.
