# AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01

# Independent Check For Deterministic OKF-Compatible AIDE Knowledge Bundle

Create and process `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Independently review `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`.

Scope:

- Check only.
- No implementation except minimal evidence/report generation if queue policy requires it.
- No runtime.
- No LLM-authored broad wiki.
- No network.
- No provider/model calls.
- No Reconciler.
- No CapabilityManifest.
- No ConformanceProfile.
- No PatchTransaction.
- No AdapterManifest.
- No ContextPack v2.
- No Service.
- No Commander.
- No branch/worktree automation.
- No target apply.
- No active apply.
- No release.
- No GitHub mutation.
- No Gateway/network/model/provider calls.

Verify:

- `.aide/knowledge/okf` exists.
- `index.md` and `log.md` exist.
- Required initial pages exist.
- Non-reserved concept pages have parseable frontmatter.
- Every concept page has non-empty `type`.
- `index.md` and `log.md` are treated as reserved files.
- OKF reports parse.
- Concept index and link index parse.
- Broken links are warnings, not fatal.
- Orphan pages are warning-classified.
- `source_refs` and `evidence_refs` exist or are warning-classified.
- `aide://` refs parse where present.
- event refs parse where present.
- EventRecord is classified according to its accepted-with-warnings projection-only state.
- stale latest-task-packet ambiguity is surfaced.
- OKF pages do not become protocol/evidence/execution authority.
- Pages do not overclaim accepted capabilities.
- Existing protocol commands remain compatible.
- Focused tests pass.
- Validation evidence exists.
- No secrets are emitted.
- No forbidden operations were introduced.

Expected result:

```text
PASS, PASS_WITH_WARNINGS, FAILED_VALIDATION, BLOCKED, or PARTIAL
```

Recommended next task if PASS or PASS_WITH_WARNINGS:

```text
AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01
```

Recommended next task after acceptance:

```text
AIDE-BUILD-RECONCILER-REPORTS-01
```
