# Diagnostic Mapping

Dominium Diagnostic owns native domain diagnostic meaning. AIDE finding owns generic queue/report finding shape. Reconciler finding owns drift-detection report shape. TestJob failure owns generic validation-attempt failure shape. EvidencePacket claim/result owns proof aggregation shape. Workbench diagnostic projection owns presentation shape.

Severity translation:

- Dominium blocking diagnostic can map to AIDE blocked only when it prevents the intended operation.
- AIDE warning can remain a warning when evidence is complete and authority is not at risk.
- Reconciler finding is advisory until a queue task makes it actionable.
- TestJob failure is execution evidence, not a domain law rewrite.
- Workbench projection must preserve owner, severity, source ref, freshness, and evidence refs.

Not every warning is an execution blocker.
