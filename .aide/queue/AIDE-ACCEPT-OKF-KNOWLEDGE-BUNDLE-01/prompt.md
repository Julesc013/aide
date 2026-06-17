# Prompt: AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01

Check-only acceptance review for the deterministic OKF-compatible AIDE knowledge bundle.

Accepted capability, if evidence supports acceptance:

```text
minimal_okf_knowledge_bundle
```

Review chain:

- `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`
- `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`
- `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`

Accept only the deterministic OKF-compatible markdown bundle, reserved `index.md` and `log.md`, required initial concept pages, frontmatter/type rules, concept and link indexes, `okf status/project/validate/lint` CLI dispatch, ReferenceID and EventRecord integration, stale latest-task-packet surfacing, and the protocol/evidence/reference/event authority boundary.

Do not repair implementation files. Do not regenerate and commit OKF source-hash refreshes. Do not implement Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, Runtime, Service, Commander, providers, Gateway, target apply, branch/worktree automation, release, GitHub mutation, or provider/model/network behavior.

If accepted, recommend exactly:

```text
AIDE-BUILD-RECONCILER-REPORTS-01
```

Stop at `needs_review`.
