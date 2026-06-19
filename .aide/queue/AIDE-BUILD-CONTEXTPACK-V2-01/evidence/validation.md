# Validation

Validation is recorded after materializing this blocked build packet.

Planned command set:

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-ADAPTER-MANIFEST-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTEXTPACK-V2-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONTEXTPACK-V2-01`
- JSON parsing for `.aide/reports/context-pack-v2/blocked-report.json`
- secret-like value scan over changed files
- `py -3 .aide/scripts/aide_lite.py validate`

ContextPack v2 implementation, compile, unit test, projection, and CLI
commands were not run because no implementation slice is authorized while the
precondition is blocked.

Observed results:

- `git status --short --branch`: PASS, expected authorized changes only.
- `git diff --check`: PASS; emitted the existing line-ending warning that `.aide/queue/index.yaml` will be normalized from CRLF to LF when Git touches it.
- `git diff --cached --check`: PASS with no staged changes at the time.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-ADAPTER-MANIFEST-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-ADAPTER-MANIFEST-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTEXTPACK-V2-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONTEXTPACK-V2-01`: PASS, no missing evidence listed.
- JSON parsing for `.aide/reports/context-pack-v2/blocked-report.json`: PASS.
- Secret-like value scan over changed files: PASS, no matches.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
