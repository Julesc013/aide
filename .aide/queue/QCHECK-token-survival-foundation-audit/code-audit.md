# Code Audit

## Command Surfaces

- `scripts/aide`: Harness v0 validate/doctor/self-check, still structural.
- `.aide/scripts/aide_lite.py`: Q09-Q20 local control plane.
- `core/gateway`: Q19 local/report-only Gateway skeleton.
- `core/providers`: Q20 offline provider metadata contracts.

## What Works

- AIDE Lite command surface runs end-to-end with no external dependencies.
- Gateway skeleton tests pass.
- Provider contract tests pass.
- AIDE Lite direct tests pass.
- Syntax compile passes for 55 key Python files.
- Provider/model/network calls are not present in implemented behavior.

## Code Quality Findings

| Finding | Severity | Notes |
| --- | --- | --- |
| `aide_lite.py` is too large | medium | It is successful bootstrap machinery but now owns token, context, verify, review, ledger, eval, controller, route, cache, Gateway, and provider behavior. |
| Hidden test discovery fails | medium | Direct test files pass, but standard `unittest discover -s .aide/scripts/tests -t .` fails before loading tests. |
| Simple text/YAML parsing | medium | Acceptable under stdlib-only constraints; risky as contracts grow. |
| Hardcoded current queue lookup | medium | `current_queue_ref()` is stale and ends at Q17. |
| Generated report side effects | low/medium | Validation commands refresh latest reports; this is expected but noisy. |
| Tests sometimes overfit artifacts | medium | Golden/provider/cache tests prove local contracts, not real task quality or provider capability. |

## Portability

- Windows path behavior is actively exercised.
- Python standard library only keeps portability high.
- Shell wrapper is PowerShell-oriented in this environment; AIDE Lite itself is
  Python and more portable.

## Missing Tests

- Importable `.aide/scripts/tests` discovery.
- Queue status/index contradiction checks.
- Profile/current-focus freshness checks.
- Real coding task golden tasks.
- Cross-repo task-packet/context-packet fixtures.
