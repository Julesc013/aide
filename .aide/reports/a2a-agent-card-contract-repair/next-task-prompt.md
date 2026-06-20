# AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01
# Independent Check of A2A Agent Card Standards Repair

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live repository before writing anything.

Check `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` without modifying A2A implementation, schema, tests, fixtures, generated reports, or failed-check evidence.

Verify the eight material findings remain repaired: external A2A pins, standards-clean AgentCard, required supportedInterfaces, provider omission, legacy field removal, capability field repair, AgentSkill metadata separation, and no advertised unimplemented skills.

If the repair passes, recommend `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`. If a material defect remains, recommend one bounded repair task.
