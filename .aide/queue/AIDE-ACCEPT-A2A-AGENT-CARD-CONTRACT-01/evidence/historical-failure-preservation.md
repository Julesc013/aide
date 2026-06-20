# Historical Failure Preservation

The original independent check remains `FAILED_VALIDATION` with eight material findings:

1. missing external A2A protocol version pinning
2. missing `supportedInterfaces`
3. legacy top-level `url`
4. null provider URL
5. legacy extended-card placement
6. unsupported `stateTransitionHistory`
7. AIDE governance fields inside official AgentSkill objects
8. unimplemented skills advertised in an official-looking `skills` array

Acceptance did not rewrite failed-check evidence. The accepted result depends on the later bounded repair and independent repair check.
