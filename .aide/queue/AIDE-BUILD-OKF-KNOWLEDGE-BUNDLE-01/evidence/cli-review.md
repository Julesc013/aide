# CLI Review

Added thin AIDE Lite dispatch:

```bat
py -3 .aide/scripts/aide_lite.py okf status
py -3 .aide/scripts/aide_lite.py okf project --source current-repo
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
```

The CLI delegates to `core/knowledge/okf_bundle.py` and prints explicit boundary lines:

- `okf_execution_authority: false`
- `protocol_authority_from_markdown: false`
- `evidence_authority_from_markdown: false`
- `runtime_knowledge_service_implemented: false`
- `provider_or_model_calls: none`
- `Gateway calls: none`

No runtime/network commands were added.
