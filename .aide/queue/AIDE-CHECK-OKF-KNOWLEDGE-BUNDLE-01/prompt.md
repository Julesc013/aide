# Prompt: AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01

Check-only review of `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`.

Required behavior:

- Review the OKF knowledge bundle build independently.
- Do not repair implementation files.
- Do not implement Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, Runtime, providers, Gateway, Commander, Service, target apply, branch/worktree automation, release, or GitHub behavior.
- Confirm generated OKF pages remain projection-only knowledge, not protocol, evidence, queue, or execution authority.
- If the check passes with warnings, recommend exactly `AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01`.
- Do not recommend Reconciler directly from this check.
- Stop at `needs_review`.

Live-state note:

- The prompt reported HEAD `c51859006e8cf4ac429bbaf9663917d0fdbe904b` and unrelated `.aide/intake` dirt.
- Live repository truth at check start had clean worktree on HEAD `744503c56d37c132410485aacee3c26347cd96c4`; `c51859006e8cf4ac429bbaf9663917d0fdbe904b` was an ancestor of HEAD.
