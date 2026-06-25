# Event Stream Matrix

The parser now validates enough event structure to distinguish:

- duplicate terminal event: `duplicate_terminal_event`;
- nonterminal event after terminal: `event_after_terminal`.

Focused tests cover:

- empty output;
- malformed JSON line;
- non-object JSON;
- missing/wrong schema;
- missing/wrong run ref;
- missing/noninteger/duplicate/decreasing/gapped sequence;
- missing/unsupported event kind;
- missing/nonobject payload;
- missing terminal event;
- duplicate and mixed terminal events;
- nonterminal event after terminal;
- truncated final JSON;
- invalid artifact declarations;
- nonzero process return with `run_completed`;
- `run_failed`, `run_timed_out`, `run_cancelled`, and
  `reconciliation_required` outcomes.

Failed streams remain typed refusals and do not preserve a successful domain
result.
