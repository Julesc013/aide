# Failure And Recovery Policy

Rules:

- fail closed on authority;
- fail forward on throughput only for disjoint read-only work;
- preserve failed evidence;
- use bounded repair;
- require independent repair check;
- use explicit resume task;
- quarantine after retry budget exhaustion;
- continue unrelated read-only work only when paths and queue ownership are disjoint.

Hard dependency failure blocks the dependent task. Soft dependency warning is recorded and may allow read-only planning if authority is not at risk.
