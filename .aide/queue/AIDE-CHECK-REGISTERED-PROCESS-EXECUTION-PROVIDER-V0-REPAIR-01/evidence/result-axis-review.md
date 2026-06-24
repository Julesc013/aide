# Result Axis Review

The check verified the provider keeps these axes separate:

- transport outcome;
- process outcome;
- decoder outcome;
- domain outcome;
- validation outcome;
- evidence completeness.

Relevant observations:

- Valid typed refusal kept `domain_outcome: typed_refusal`.
- Decoder exception kept `decoder_outcome: exception`, `domain_outcome: none`,
  and incomplete validation/evidence.
- Timeout kept `process_outcome: timed_out`, `decoder_outcome: not_decoded`,
  `domain_outcome: none`, and incomplete validation/evidence.
- State-probe failure kept `reason_code: state_probe_failure`,
  `domain_outcome: none`, and incomplete validation/evidence for the after-probe
  path.
- Before-state probe failure launched zero processes and did not report complete
  validation.

No generic `PASS` field was used as proof that all axes succeeded.
