# Historical Failure Review

The original independent A2A check remains `FAILED_VALIDATION` with eight material findings:

- `A2A-CHECK-001`: external A2A protocol version not pinned
- `A2A-CHECK-002`: `supportedInterfaces` omitted
- `A2A-CHECK-003`: legacy top-level `url`
- `A2A-CHECK-004`: provider object with null URL
- `A2A-CHECK-005`: legacy extended-card placement
- `A2A-CHECK-006`: unsupported `stateTransitionHistory`
- `A2A-CHECK-007`: AIDE governance fields embedded in AgentSkill objects
- `A2A-CHECK-008`: unimplemented skills advertised in an official-looking skills array

The acceptance did not rewrite that failure. It accepts the repaired projection only after the independent repair check verified zero remaining material findings.
