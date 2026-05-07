# Latest Gateway Status

- schema_version: `aide.gateway-status.v0`
- generated_by: `q19.gateway-skeleton.v0`
- service: `aide-gateway-skeleton`
- mode: `local_skeleton_report_only`
- provider_calls_enabled: `false`
- model_calls_enabled: `false`
- outbound_network_enabled: `false`
- raw_prompt_storage: `false`
- raw_response_storage: `false`

## Readiness

- cache_boundary: ready (missing: 0)
- context_compiler: ready (missing: 0)
- evidence_review: ready (missing: 0)
- gateway_skeleton: ready (missing: 0)
- golden_tasks: ready (missing: 0)
- outcome_controller: ready (missing: 0)
- provider_adapters: ready (missing: 0)
- router_profile: ready (missing: 0)
- token_ledger: ready (missing: 0)
- token_survival: ready (missing: 0)
- verifier: ready (missing: 0)

## Signals

- verifier_status: PASS
- golden_task_status: PASS
- route_class: frontier
- route_blocked: false
- token_budget_status: within_budget
- cache_key_count: 8
- provider_adapter_status: PASS
- provider_family_count: 13

## Endpoint Policy

- `/health`: local liveness metadata only
- `/status`: compact readiness metadata only
- `/route/explain`: latest advisory route decision only
- `/summaries`: repo-relative refs and short file stats only
- `/version`: schema/policy/profile metadata only

## Limits

- No provider calls, model calls, outbound network calls, or proxy forwarding.
- No raw prompt bodies, raw response bodies, secrets, or `.aide.local/` contents are stored or returned.
- Q19 is not a production Gateway.
