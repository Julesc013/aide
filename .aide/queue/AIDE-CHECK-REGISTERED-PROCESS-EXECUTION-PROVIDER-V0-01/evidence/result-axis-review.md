# Result Axis Review

The receipt/outcome model keeps transport, process, decoder, domain, validation, and evidence axes as separate fields.

- decoder_failure_validation_outcome: `complete`
- decoder_failure_evidence_completeness: `complete`
- probe_failure_validation_outcome: `complete`
- probe_failure_domain_outcome: `typed_result`

Findings: decoder and probe failures are represented, but failure axes are still marked as complete or typed result.
