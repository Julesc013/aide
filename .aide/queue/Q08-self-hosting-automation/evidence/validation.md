# Q08 Validation

## Baseline Before Edits

All baseline commands were run before implementation changes.

| Command | Result |
| --- | --- |
| `py -3 scripts/aide validate` | Pass with warnings: 142 info, 7 warning, 0 error |
| `py -3 scripts/aide doctor` | Pass with warnings; confirmed stale `next_recommended_step: Q07 review...` |
| `py -3 scripts/aide compile --dry-run` | Pass; `.aide/generated/manifest.yaml` reported `would_replace` |
| `py -3 scripts/aide migrate` | Pass; no-op Compatibility baseline |
| `py -3 scripts/aide bakeoff` | Pass; metadata/readiness only |
| `py -3 scripts/aide-queue-status` | Pass; Q08 was pending/planning_complete |
| `py -3 scripts/aide-queue-next` | Pass; reported Q08 pending |

## Post-Change Harness Commands

| Command | Result |
| --- | --- |
| `py -3 scripts/aide validate` | Pass with warnings: 148 info, 8 warning, 0 error |
| `py -3 scripts/aide doctor` | Pass with warnings; next step now reports Q08 review |
| `py -3 scripts/aide compile --dry-run` | Pass; deterministic dry-run, no generated artifacts written |
| `py -3 scripts/aide migrate` | Pass; no-op Compatibility baseline |
| `py -3 scripts/aide bakeoff` | Pass; no external calls |
| `py -3 scripts/aide self-check` | Pass; report-only output |
| `py -3 scripts/aide self-check --write-report` | Pass; wrote `.aide/runs/self-check/latest.md` |
| `py -3 scripts/aide --help` | Pass; includes `self-check` |
| `py -3 scripts/aide import` | Pass; report-only |

## Queue Helper Commands

| Command | Result |
| --- | --- |
| `py -3 scripts/aide-queue-status` | Pass; Q08 is `needs_review` / `implemented` |
| `py -3 scripts/aide-queue-next` | Pass; reports Q08 review gate and does not invoke workers |
| `py -3 scripts/aide-queue-run --help` | Pass |
| `py -3 scripts/aide-queue-run --no-prompt` | Pass; reports review gates and `automatic_worker_invocation: false` |

## Tests And Syntax

| Command | Result |
| --- | --- |
| `py -3 -m unittest discover -s core/harness/tests -t .` | Pass: 10 tests |
| `py -3 -m unittest discover -s core/compat/tests -t .` | Pass: 5 tests |
| `py -3 -m py_compile core/harness/*.py core/compat/*.py scripts/aide scripts/aide-queue-run scripts/aide-queue-next scripts/aide-queue-status` | Failed on Windows because `py_compile` receives literal wildcard arguments |
| PowerShell-expanded `py -3 -m py_compile` over the same file set | Pass |
| `git diff --check` | Pass; Git printed line-ending normalization warnings only |

## Scope Checks

- `CLAUDE.md`: absent.
- `.claude/`: absent.
- Generated artifact refresh: not run.
- `.aide/generated/manifest.yaml`: still stale by source fingerprint and intentionally not refreshed.
- External model/provider/network calls: none added.
- Automatic Codex or external worker invocation: none added.
- Runtime/Service/Commander/Host/Mobile/release automation: none added.
