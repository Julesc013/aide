# Q11 Remaining Risks

## Deferred By Design

- No embeddings, vector search, semantic search, or LLM file summaries are implemented in Q11.
- No exact tokenizer is implemented; all token reports still use `ceil(chars / 4)`.
- No provider billing integration exists; savings reports are approximate and repo-local only.
- No Gateway, model router, provider adapter, cache, Runtime, Service, Commander, UI, Mobile, MCP/A2A, or autonomous loop work is authorized by Q11.
- No full verifier is implemented; Q12 remains responsible for evidence packets, diff scope, file-ref checks, and mechanical review gates.
- No formal token ledger is implemented; Q14 remains responsible for durable token accounting and regression reports.
- No golden task quality proof is implemented; Q15 remains responsible for deterministic quality preservation checks.

## Known Technical Limits

- Repo roles are deterministic path/extension heuristics, not semantic certainty.
- Test-map relationships are heuristic and can miss real coverage or include broad structural checks where no direct test exists.
- Exact reference support validates `path#Lstart-Lend` syntax, but full excerpt extraction remains deferred.
- Generated context artifacts intentionally contain refs and hashes, not raw source contents; future workers may need to open exact files when a packet is insufficient.
- Context artifacts can become stale when evidence or docs change after generation; rerun `py -3 .aide/scripts/aide_lite.py index` and `context` before using them as a fresh packet source.

## Carried Forward

- `.aide/profile.yaml` still names Q09 as the current focus; Q11 did not edit it because the Q11 allowlist did not include profile changes. Treat `.aide/queue/` and the Q11 evidence as the live queue-state source until a later reconciliation phase updates the profile.
- `.aide/generated/manifest.yaml` may still report generated-artifact source fingerprint drift after Q11 queue/catalog/context changes. Q11 did not refresh the generated manifest because `.aide/generated/manifest.yaml` was only allowed through the existing Harness compile/write path and manifest refresh was not necessary for context compilation.
- Q09 and Q10 remain `needs_review`, which is intentional review-gate nuance rather than a Q11 blocker.
- Direct unittest discovery with `-s .aide/scripts/tests -t .` remains blocked by Python's hidden-directory importability behavior; direct discovery without `-t .` and the Harness mirror test path are the supported validation paths for AIDE Lite tests.
