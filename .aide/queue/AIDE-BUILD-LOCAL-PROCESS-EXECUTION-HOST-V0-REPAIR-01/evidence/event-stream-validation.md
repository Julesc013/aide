# Event Stream Validation

The fixture worker now emits NDJSON events with schema `aide.fixture-worker.events.v0`.

The parser fails closed on:

- empty output;
- malformed JSON;
- unsupported schema or event kind;
- wrong run ref;
- non-integer sequence;
- duplicate sequence;
- decreasing sequence;
- sequence gaps;
- missing terminal event;
- events after terminal;
- failed or timed-out terminal events.

The live run persisted the raw event stream as:

`.aide/reports/local-process-execution-host/raw-events/sha256/d8da259d5171782860263ae5e11185f24bfd3ec468dda8fbea87667409323e26.ndjson`
