# Q20 Capability Metadata Report

## Capability Dimensions

Q20 records these dimensions:

- deterministic_transform
- file_system_local
- structured_output
- json_schema
- tool_use
- long_context
- local_execution
- privacy_sensitive
- cheap_bulk
- reasoning_heavy
- frontier_review
- human_judgement
- test_execution
- code_edit
- unavailable

## Capability Status Model

Allowed statuses are:

- `supported_by_contract`
- `planned`
- `unknown`
- `not_applicable`
- `requires_future_probe`

These statuses are deliberately conservative. They do not claim measured model
quality, speed, pricing, availability, exact long-context behavior, or provider
API compatibility.

## Provider Families By Class

- deterministic: `deterministic_tools`
- human: `human`
- local_model: `local_ollama`, `local_lm_studio`, `local_llama_cpp`, `local_vllm`, `local_sglang`
- remote_model: `openai`, `anthropic`, `google_gemini`, `deepseek`, `other_remote_provider`
- aggregator: `openrouter`

## Privacy Classes

- local: deterministic tools and planned local model families
- human: human review
- remote: remote model families and aggregator family
- unknown: `other_remote_provider`

## Routing Use

Route decisions may mention provider family candidates as metadata only:

- `no_model_tool` -> deterministic tools
- `human_review` -> human
- local route classes -> local provider families
- remote/frontier route classes -> remote provider families or human fallback

Routes remain advisory. Q20 metadata does not execute a route, probe
availability, or demote hard floors.

## What Is Not Measured

Q20 does not measure:

- model quality
- token pricing
- provider availability
- provider latency
- provider-specific JSON schema reliability
- local model installation state
- credential validity
- billing or usage
- exact token counts
