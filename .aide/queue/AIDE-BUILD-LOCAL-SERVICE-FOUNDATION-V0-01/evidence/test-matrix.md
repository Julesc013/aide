# Test Matrix

Focused tests cover:

- idempotent migrations
- future migration refusal
- object put/get/list
- resource version conflict
- atomic object plus event commit
- transaction rollback on injected failure
- monotonic event reads
- cursor acknowledgment
- idempotency duplicate and conflict handling
- artifact write/read
- content-addressed dedupe
- digest mismatch refusal
- invalid digest/path traversal refusal
- reopen persistence
- corrupt database refusal
- fixture boundary flags
- CLI `local-service init-fixture`
