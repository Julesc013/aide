# Token Survival Audit

## Current Measured Surfaces

| Surface | Approx Tokens | Budget Status | Baseline | Reduction |
| --- | ---: | --- | ---: | ---: |
| latest task packet | 914 | within_budget | 60,922 | 98.5% |
| latest context packet | 482 | within_budget | 64,915 | 99.3% |
| latest review packet | 1,630 | within_budget | 6,995 | 76.7% |
| latest verification report | 1,156 | within_budget | n/a | n/a |

## Direct Token-Saving Layers

- Q09: compact task packet discipline and no-history guidance.
- Q10: deterministic AIDE Lite packet/estimate/validate behavior.
- Q11: compact context refs instead of whole-repo dumps.
- Q13: compact evidence review packet.
- Q14: token ledger and baseline comparisons.
- Q17: advisory no-model/tool routing.

## Supporting Quality/Safety Layers

- Q12 verifier.
- Q15 golden tasks.
- Q16 outcome controller.
- Q18 local-state/cache boundary.
- Q19 Gateway skeleton no-call boundary.
- Q20 provider metadata no-call boundary.

## Real Value

The current repo can already avoid sending whole history or broad repo context
for AIDE queue review. It has enough evidence to support compact GPT-5.5/human
review packets.

## Measurement Limits

- chars/4 is not provider tokenization.
- no billing ledger exists.
- no hidden reasoning-token accounting exists.
- no cached-token accounting exists.
- quality preservation is only local/deterministic.
- no external workload has proven savings.

## Verdict

The token-saving claim is plausible and partially evidenced for AIDE's own queue
work. It is not yet a general product claim.
