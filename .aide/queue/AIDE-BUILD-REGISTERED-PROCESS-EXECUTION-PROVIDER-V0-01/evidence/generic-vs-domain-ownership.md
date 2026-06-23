# Generic vs Domain Ownership

Generic provider owns:

- immutable registered spec validation;
- exact argv construction from typed argument tokens;
- `shell=False` process launch through an injected runner;
- one-launch call accounting;
- timeout capture;
- sanitized environment use from the spec;
- stream summary and scrubber invocation;
- state probe before/after capture and declared coverage;
- neutral `ProcessExecutionReceipt` and `CapabilityOutcome`.

Dominium adapter owns:

- Dominium repository identity and revision checks;
- expected command source/digest checks;
- exact Dominium argument plan;
- Dominium JSON decoder and refusal mapping;
- typed result/refusal semantics;
- Dominium-specific state probe;
- Dominium evidence, report, and event projection.
