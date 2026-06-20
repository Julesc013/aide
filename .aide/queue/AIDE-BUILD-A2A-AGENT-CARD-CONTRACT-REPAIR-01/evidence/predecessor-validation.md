# Predecessor Validation

Predecessor validation commands run:

- `py -3 .aide/scripts/aide_lite.py mcp-server-contract validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py context-pack-v2 status`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py adapter-manifest validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py patch-transaction validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py event-record validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py conformance-profile validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py conformance-result validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py okf validate`
  - Result: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reconciler validate`
  - Result: PASS_WITH_WARNINGS.

The retained warning posture is expected and relates to intentionally absent runtime, admission, trust, policy, server, worker, provider, network, and mutation behavior.
