# Validation

Validation run before final task inspect:

- `git status --short --branch`: clean baseline, `## main...origin/main`
- `git diff --check`: pass
- `git diff --cached --check`: pass
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py conformance-profile validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py conformance-result validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py event-record validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py okf validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py okf lint`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reconciler status`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reconciler validate`: `PASS_WITH_WARNINGS`
- `py -3 -m json.tool .aide/reports/self-management/report-index.json`: pass
- `py -3 -m json.tool .aide/reports/self-management/generated-output-ledger.json`: pass
- `py -3 -m json.tool .aide/reports/self-management/track-b-b1-barrier.json`: pass

Unavailable command groups:

- `py -3 .aide/scripts/aide_lite.py generated-output --help`: unavailable
- `py -3 .aide/scripts/aide_lite.py report-index --help`: unavailable

Final task-local validation is recorded after the packet is materialized.

First task inspect result after materialization was `partial` with one missing
standard evidence file, `remaining-risks.md`. That file was added and task
inspect/evidence were rerun.

Final task-local validation:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-OPERATIONAL-HEALTH-PAUSE-01`: complete, `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-OPERATIONAL-HEALTH-PAUSE-01`: 11 evidence files available, no missing files
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`
- secret-like value scan over changed files: pass, no matches

`git diff --check` passed with the known line-ending warning that
`.aide/queue/index.yaml` will normalize from CRLF to LF when Git touches it.
