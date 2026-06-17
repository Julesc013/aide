# ReferenceID Integration Review

The OKF bundle consumes the accepted ReferenceID scheme:

- protocol pages use `aide://schema/...`
- capability pages use `aide://capability/...`
- queue-derived pages use `aide://queue-task/...` where applicable
- decision pages use `aide://decision/...`
- event refs use `aide://event/...`

Validation checks `aide://` references through `core/protocol/reference_id.py`.

Result: `aide_refs_parse: true`.

No runtime reference registry or resolver service was implemented.
