# Concurrency And Idempotency

The same idempotency key returns a duplicate result without appending another
event or consuming the grant again.

A different idempotency key after the one-use grant is consumed fails closed
with `grant_exhausted`.

This is a local deterministic fixture proof only. It does not claim distributed
authorization, cross-process locking, external IAM, or remote policy behavior.
