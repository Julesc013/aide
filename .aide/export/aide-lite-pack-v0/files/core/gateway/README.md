# Core Gateway Skeleton

`core/gateway/` is the Q19 local Gateway skeleton. It is standard-library only
and exposes health, status, route explanation, summaries, and version payloads
from committed repo-local AIDE artifacts.

It does not call providers, execute models, perform outbound network calls,
forward OpenAI/Anthropic-compatible requests, read secrets, read `.aide.local/`,
or store raw prompt/response bodies.
