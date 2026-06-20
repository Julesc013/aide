# Failure And Recovery Review

Accepted recovery posture:

- fail closed on authority
- fail forward on throughput
- preserve failed evidence
- bounded repair
- independent repair check
- explicit resume
- quarantine after retry exhaustion
- continue unrelated read-only work when safe

No repair loop or runtime recovery service is implemented here.
