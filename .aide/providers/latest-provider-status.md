# Latest Provider Status

- schema_version: `aide.provider-status.v0`
- generated_by: `q20.provider-adapter.v0`
- provider_adapter_contract: `implemented_metadata_only`
- provider_family_count: 13
- live_provider_calls: `false`
- live_model_calls: `false`
- network_calls: `false`
- provider_probe_calls: `false`
- credentials_configured: `false`
- gateway_forwarding: `false`
- raw_prompt_storage: `false`
- raw_response_storage: `false`

## Provider Classes

- aggregator: 1
- deterministic: 1
- human: 1
- local_model: 5
- remote_model: 5

## Privacy Classes

- human: 1
- local: 6
- remote: 5
- unknown: 1

## Validation

- result: PASS
- warnings: 0
- errors: 0

## Boundary

- live_calls_allowed_in_q20: false
- credentials_location: future `.aide.local/` only
- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false
- gateway_forwarding: false
