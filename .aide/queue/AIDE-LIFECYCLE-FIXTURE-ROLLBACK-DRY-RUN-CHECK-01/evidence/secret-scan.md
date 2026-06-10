# Secret Scan

## Scope

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`

## Command

`rg -n --pcre2 "(SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY)" .aide\queue\AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01 .aide\queue\index.yaml .aide\context\latest-task-packet.md`

## Result

`PASS_WITH_FALSE_POSITIVES`

Hits:

- `.aide/context/latest-task-packet.md:145` contains `TOKEN_ESTIMATE`, which is task packet metadata and not a secret.
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/evidence/secret-scan.md:11` contains the literal scanner pattern.

No real secrets were found.
