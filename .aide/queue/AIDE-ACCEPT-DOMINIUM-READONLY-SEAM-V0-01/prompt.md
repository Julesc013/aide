# AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01

Acceptance-only task for the Dominium read-only seam v0.

Accept only:

```text
dominium_readonly_seam_v0
```

Accepted meaning:

```text
AIDE can deterministically inspect a pinned, already-present Dominium
repository through an offline read-only seam and project validated host,
capability, workspace, context, artifact, diagnostic, refusal, evidence, event,
and bridge records without invoking Dominium commands or mutating Dominium.
```

Forbidden interpretations:

```text
AIDE and Dominium have a live runtime bridge.
AIDE can invoke Dominium commands.
Workbench integration exists.
AIDE can apply mutations.
```

Preserve all failed historical checks, record `ACCEPTED_WITH_WARNINGS`, stop at
`needs_review`, and recommend exactly:

```text
AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

Generate the next task prompt only. Do not begin that task.
