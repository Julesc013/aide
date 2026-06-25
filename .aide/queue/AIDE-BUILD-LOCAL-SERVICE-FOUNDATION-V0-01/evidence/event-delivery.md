# Event Delivery

- event sequence numbers are SQLite autoincrement integers
- reads use `read_events_after(sequence)`
- cursors record acknowledged sequence numbers
- delivery semantics are `at_least_once`

Exactly-once delivery is explicitly not claimed.
