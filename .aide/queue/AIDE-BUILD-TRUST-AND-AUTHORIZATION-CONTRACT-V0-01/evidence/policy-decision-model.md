# Policy Decision Model

`PolicyDecision` records:

- principal
- capability or action
- workspace and target resources
- requested mode
- input and policy bundle digests
- evaluator identity/version
- decision value
- reason codes, constraints, obligations, and evidence refs

Policy decisions do not create grants by themselves. A later enforcement slice
must still bind an active grant before executing anything.
