# Test Results

## Focused Tests

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile core/protocol/event_record.py .aide/scripts/aide_lite.py` | PASS | New helper and CLI compile. |
| `py -3 -m json.tool .aide/protocol/aide-event-record.schema.json > $null` | PASS | Schema parses as JSON. |
| `py -3 -m unittest .aide.scripts.tests.test_aide_event_record_schema` | FAILED_INVOCATION | Import-style invocation through `.aide` is not supported by Python's unittest loader for this path. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_event_record_schema.py` | PASS | 20 tests passed. |

## Coverage Notes

The focused tests cover schema shape, event type validation, unknown required/optional event types, ReferenceID-backed refs, event family vocabulary, projection immutability, report JSON generation, CLI dispatch, unsupported runtime-style subcommand rejection, parser preservation, and non-runtime boundary flags.
