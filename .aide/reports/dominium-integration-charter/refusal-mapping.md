# Refusal Mapping

Refusals remain typed outcomes, not generic exceptions.

| Source | Owner | Stable reason code | Retryable | Human action | Mapping |
| --- | --- | --- | --- | --- | --- |
| AIDE task blocked | AIDE | `AIDE_TASK_BLOCKED` | no | yes | stop before bridge |
| AIDE missing hard dependency | AIDE | `AIDE_MISSING_HARD_DEPENDENCY` | yes | no | dependency refusal |
| AIDE unsupported operation | AIDE | `AIDE_UNSUPPORTED_OPERATION` | no | yes | unsupported refusal |
| AIDE missing capability | AIDE | `AIDE_MISSING_CAPABILITY` | yes | no | capability unavailable |
| AIDE missing conformance result | AIDE | `AIDE_MISSING_CONFORMANCE_RESULT` | yes | no | admission blocked |
| future missing admission/grant | AIDE | `AIDE_MISSING_ADMISSION_OR_GRANT` | yes | yes | invocation not authorized |
| stale ContextPack | AIDE | `AIDE_STALE_CONTEXTPACK` | yes | no | refresh context |
| invalid PatchTransaction | AIDE | `AIDE_INVALID_PATCH_TRANSACTION` | no | yes | proposal invalid |
| unknown command | Dominium | `DOMINIUM_UNKNOWN_COMMAND` | no | yes | command refusal |
| unavailable capability | Dominium | `DOMINIUM_UNAVAILABLE_CAPABILITY` | yes | no | capability refusal |
| invalid document | Dominium | `DOMINIUM_INVALID_DOCUMENT` | no | yes | document refusal |
| validation refusal | Dominium | `DOMINIUM_VALIDATION_REFUSAL` | yes | no | typed validation result |
| process refusal | Domino | `DOMINO_PROCESS_REFUSAL` | no | yes | no mutation |
| unavailable action | Workbench | `WORKBENCH_UNAVAILABLE_ACTION` | yes | no | unavailable view/action |
| stale context | Workbench | `WORKBENCH_STALE_CONTEXT` | yes | no | refresh request |
