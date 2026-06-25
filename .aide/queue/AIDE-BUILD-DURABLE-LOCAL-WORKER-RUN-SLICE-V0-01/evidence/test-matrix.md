# Test Matrix

Focused tests cover:

- authorization, one host call, persistence, restart readback, artifact metadata, and false boundaries;
- validation failure when durable objects, events, or artifact metadata are missing;
- deterministic fake-runner output;
- safe `durable-worker-run status` CLI behavior without launching a fixture.

Regression validation also covers local trust enforcement, local Service
foundation, and LocalProcessExecutionHost fixture behavior.
