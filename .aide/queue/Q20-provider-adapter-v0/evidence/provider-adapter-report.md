# Q20 Provider Adapter Report

## Policy Summary

Q20 adds `.aide/policies/provider-adapters.yaml` with:

- operating mode: `offline_contracts_only`, `metadata_validation_only`, `no_provider_calls`
- adapter classes: deterministic tool, human review, local model, remote model, aggregator, unknown
- credential policy: credentials must be declared, never committed, and future live values belong only under `.aide.local/`
- call policy: live provider calls, model calls, network calls, and provider probes are disabled in Q20
- quality policy: provider selection must respect Router Profile hard floors, verifier output, and golden tasks

## Metadata Artifacts

`.aide/providers/provider-catalog.yaml` lists 13 provider families:

- deterministic_tools
- human
- local_ollama
- local_lm_studio
- local_llama_cpp
- local_vllm
- local_sglang
- openai
- anthropic
- google_gemini
- deepseek
- openrouter
- other_remote_provider

`.aide/providers/capability-matrix.yaml` records conservative capability
metadata. `.aide/providers/adapter-contract.yaml` records the future adapter
metadata shape. `.aide/providers/status.yaml` records Q20 as metadata-only with
live provider calls, model calls, credentials, Gateway forwarding, and local
model setup disabled.

## Core Provider Helpers

`core/providers/**` provides standard-library-only helpers:

- `contracts.py`: dataclasses/enums for provider classes, adapter classes, privacy classes, capability statuses, provider metadata, provider status, and adapter contracts.
- `registry.py`: simple committed-metadata parsing, provider catalog loading, capability-anchor extraction, no-secret scanning, and no-call validation.
- `status.py`: deterministic status rendering, Markdown rendering, contract summary, and offline probe.

There is no function that calls a provider, calls a model, probes a network, or
reads credentials.

## AIDE Lite Commands

Q20 adds:

- `provider list`: lists provider family metadata.
- `provider status`: writes latest provider status JSON/Markdown.
- `provider validate`: validates provider policy/catalog/capability/contract/status and no-secret/no-call anchors.
- `provider contract`: prints compact adapter contract fields.
- `provider probe --offline`: reports metadata readiness and explicitly performs no live probe.

`validate`, `doctor`, `verify`, `review-pack`, `route explain`, `cache report`,
`gateway status`, and `selftest` now understand provider metadata where useful,
without adding execution or forwarding.

## Latest Provider Status

- JSON: `.aide/providers/latest-provider-status.json`
- Markdown: `.aide/providers/latest-provider-status.md`
- provider_family_count: 13
- validation_result: PASS
- credential_required_count: 6
- credentials_configured: false
- live_provider_calls: false
- live_model_calls: false
- network_calls: false
- gateway_forwarding: false
- raw_prompt_storage: false
- raw_response_storage: false

## Limitations

- Metadata is conservative and not a performance claim.
- Remote/local model capabilities that require measurement use
  `requires_future_probe` or `planned`.
- Q20 does not configure credentials, local models, provider probes, pricing,
  billing, exact tokenizer behavior, Gateway forwarding, or provider response
  caching.
