# Test Results

## Result

PASS_WITH_WARNINGS

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile core/protocol/event_record.py .aide/scripts/aide_lite.py` | PASS | Helper and CLI compile. |
| `py -3 -m json.tool .aide/protocol/aide-event-record.schema.json` | PASS | Schema parses as JSON. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_event_record_schema.py` | PASS | 20 focused tests passed. |
| `py -3 .aide/scripts/aide_lite.py event-record status` | PASS_WITH_WARNINGS | Projection-only status retained. |
| `py -3 .aide/scripts/aide_lite.py event-record project --source accepted-reference-id` | PASS_WITH_WARNINGS | Projection reports regenerated without source mutation. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | Validation report preserved ReferenceID integration and forbidden-operation boundaries. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad repository validation passed. |

## Coverage Notes

Focused tests cover schema shape, event family vocabulary, event type parsing, fail-closed unknown required event types, optional future event warnings, ReferenceID-backed refs, projection immutability, report generation, CLI dispatch, parser preservation, unsupported runtime-style subcommand rejection, and non-runtime boundary flags.
