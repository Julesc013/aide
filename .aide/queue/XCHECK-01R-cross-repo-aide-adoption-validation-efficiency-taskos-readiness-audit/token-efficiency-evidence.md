# Token Efficiency Evidence

## Available Evidence

- AIDE Lite `doctor` reports token ledger records: 83.
- AIDE Lite `validate` reports latest task packet tokens: 1029.
- AIDE Lite `validate` reports latest context packet tokens: 486.
- AIDE Lite `validate` reports latest review packet tokens: 2423 and warns it is slightly over the 2400 hard limit.
- AIDE export report records raw prompt/response storage as false.

## Interpretation

The current AIDE machinery supports compact task/context/review packets and
source-pack exclusion of raw prompts and raw responses. This supports lower
reconstruction cost for future work.

## Limit

This audit did not produce exact tokenizer or billing telemetry. Any token
savings claim is approximate and evidence-based only at packet-size level.
