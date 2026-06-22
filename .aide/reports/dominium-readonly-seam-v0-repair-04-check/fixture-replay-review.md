# Fixture Replay Review

| Assertion | Outcome | Severity | Source Finding |
| --- | --- | --- | --- |
| `fixture.value_presence` | PASS | MATERIAL | `fixture.production_requires_value` |
| `fixture.ascii_canonical_indexes` | PASS | MATERIAL | `fixture.production_rejects_unicode_decimal_indexes` |
| `fixture.forbidden_key_set` | PASS | MATERIAL | `fixture.production_forbidden_key_set_complete` |
| `fixture.boundary_failures` | PASS | WARNING | `None` |
| `fixture.negative_fixture_digests` | PASS | WARNING | `None` |
