# Token And Quality State

## AIDE Token Evidence

Current AIDE token-saving evidence comes from `.aide/reports/token-savings-summary.md`.

| Surface | Chars | Approx Tokens | Baseline | Baseline Tokens | Reduction |
| --- | ---: | ---: | --- | ---: | ---: |
| latest task packet | 3,716 | 929 | root history | 64,761 | 98.6% |
| latest review packet | 6,658 | 1,665 | review baseline | 7,015 | 76.3% |
| latest context packet | 1,943 | 486 | repo context | 69,217 | 99.3% |

Method: chars/4, rounded up. This is useful for trend and budget control, not
exact tokenizer or provider billing proof.

## Cross-Repo Token Evidence

| Repo | Evidence | Result |
| --- | --- | --- |
| AIDE fixture target | Q21 temporary fixture import | task packet 3,789 chars / 948 approximate tokens |
| Eureka | missing | no Q22 packet or report found |
| Dominium | missing | no Q23 packet or report found |

## Quality Gates

Current AIDE quality gates:

- verifier: PASS
- golden tasks: PASS, 6/6
- review-pack generation: PASS
- test suites: PASS
- gateway smoke: PASS, no-call
- provider validate/probe offline: PASS, no-call
- adapter validate/drift: PASS

## Claims AIDE Can Make Now

Supported:

- AIDE reduces prompt surface size inside the AIDE repo.
- AIDE preserves required packet structure for its own substrate.
- AIDE Lite validation is repeatable.
- Export pack excludes source-specific and secret/local state.
- Adapter previews are compact, non-destructive, and no-call.

Not yet supported:

- AIDE reduces prompt size in Eureka.
- AIDE reduces prompt size in Dominium.
- AIDE preserves arbitrary coding-task quality.
- Adapter outputs improve real target-tool behavior.
- Gateway/provider work is ready for live execution.

## Quality Caveat

The current quality evidence is real but narrow. It protects the AIDE workflow
from obvious structural decay and prompt bloat. It does not replace human review
or target-specific tests for real implementation work.
