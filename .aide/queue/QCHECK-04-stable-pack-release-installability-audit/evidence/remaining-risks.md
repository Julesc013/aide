# Remaining Risks

## Non-Blocking for Q49 Preflight

- Q36-Q48 remain `needs_review`; they are implemented but not formally accepted.
- `origin/main` is behind local `main`; remote handoff needs explicit sync/push authorization outside QCHECK.
- Release bundle provenance records dirty source state from local generated artifacts.
- `scripts/aide` reports an inherited generated manifest freshness warning.
- Repo intelligence still has unknown classifications and quality warnings.
- Historical malformed commits remain in changelog/commit-range evidence.
- Broad unittest discovery under `.aide/scripts/tests` times out; canonical test runner passes.
- Safe import adds an AIDE managed section to `AGENTS.md`; manual content is preserved, but target preflight must review it.

## Blocking for Publication or Broad Stable Claims

- Q36-Q48 review gates must be resolved before claiming official public release readiness.
- Remote `origin/main` is not up to date.
- No GitHub Release is published.
- No final tag naming decision exists.
- Dominium and Eureka target preflights have not yet completed.

## Deferred by Policy

- install apply mode
- repair apply mode
- upgrade apply mode
- rollback/uninstall apply mode
- GitHub release publication
- target repo mutation
- CI/branch protection application
- Gateway/provider/model work
