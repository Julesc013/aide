# X-TEST-00 Test Telemetry Contracts

Status: implemented for review.

Added compact summary, failure-family, slow-test, test-run, test-plan, impact-map, full-discovery handoff, and validation-tier report schemas under `.aide/tests/`.

Telemetry policy requires repo, commit, branch, dirty state, command, tier, timing, status, totals, failure families, artifacts, warnings, stale checks, and generator identity. Raw logs remain external artifacts.

The handoff status for long full discovery is `WAITING_FOR_EXTERNAL_FULL_DISCOVERY`.

