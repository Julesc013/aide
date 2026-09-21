# Validation

## Admission And Contract Checkpoint

| Command or check | Result |
|---|---|
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 353 queue tasks and objects validated |
| `git diff --check` | PASS |
| Requirement disposition | PASS; only `UR-INT-06` and `UR-INT-07` adopted as `AIDE-INT-001` and `AIDE-INT-002` |
| Imported draft preservation | PASS; imported draft and manifest bytes unchanged |

## Source And Regression Validation

| Command | Result |
|---|---|
| `py -3 -B .aide/scripts/tests/test_continuous_worker_pr_observation.py -v` | PASS; 21 tests in 68.792 seconds |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_provider_bridge.py -v` | PASS; 12 tests in 77.821 seconds |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_integration_broker.py -v` | PASS; 37 tests in 190.701 seconds, with one symlink-privilege skip |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_broker_authority.py -v` | PASS; 5 tests in 19.429 seconds |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_github_observation.py -v` | PASS; 26 tests in 0.208 seconds |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_github_http.py -v` | PASS; 19 tests in 2.093 seconds |

The 120 executed tests passed. The single skipped case attempts to create a
disposable symlink and was not runnable because this Windows process lacks the
required privilege. The new adversarial bridge test proves that a missing,
wrong-digest, changed-actor, wrong-stage, or stale observation refuses before a
provider-call directory or child exists. The stale case uses a correctly formed
earlier observation after a newer durable observation selects the same stage,
reaching the ledger's exact-latest comparison. The complete staged test proves
that every mutation envelope matches its durable intent and a recorded
observation, while each submitted acknowledgement remains pending until the
next authoritative read.

## Repository Validation

| Command | Result |
|---|---|
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 353 queue tasks and objects validated, no source task mutation |
| `py -3 -B .aide/scripts/aide_lite.py validate` | PASS |
| `git diff --check` | PASS |

The validation helpers refreshed four tracked workunit reports as generated
output. Those helper-only changes were restored and are excluded from this
bounded source checkpoint.

No provider, credential, external network, protected-host, target, or release
operation ran during this checkpoint.
