# AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01
# Independent Check of A2A Agent Card Standards Repair

Use `.aide/queue/index.yaml` as canonical queue truth.

Check `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` without modifying the A2A contract implementation.
Verify explicit A2A version pins, standards-clean AgentCard shape, supportedInterfaces, fixture-only endpoint metadata, provider omission, legacy-field removal, candidate skill metadata separation, validator hardening, deterministic projection, source immutability, and explicit non-capabilities.

If no material issue exists, recommend `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.
If a material defect exists, recommend one bounded repair task.
