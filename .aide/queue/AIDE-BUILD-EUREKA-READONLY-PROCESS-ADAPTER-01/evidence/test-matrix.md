# Test Matrix

Focused fake-runner tests cover:

- exact argv, environment, working directory, and `shell=false`;
- exactly one process call on valid preconditions;
- zero calls for unsupported capability, wrong revision, wrong digest, wrong remote, and dirty checkout;
- timeout refusal;
- malformed JSON refusal;
- inconsistent return-code refusal;
- typed failed Eureka status refusal;
- deterministic projection and shared receipt/outcome models;
- local path and secret-like stream scrubbing;
- unexpected repository mutation detection after process launch.
