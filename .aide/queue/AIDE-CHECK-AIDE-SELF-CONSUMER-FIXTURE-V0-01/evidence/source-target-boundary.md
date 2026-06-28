# Source Target Boundary

The self-consumer fixture distinguishes:

- AIDE source repository truth.
- A synthetic installed AIDE Lite consumer target.

Verified boundary properties:

- `source_repo_is_target: false`
- `source_repo_identity_excluded: true`
- `source_generated_state_is_target_truth: false`
- source pack excludes raw prompts, raw responses, and secrets.
- installed target states do not claim source repo identity.
- `source-repo-confusion-refusal` expects `BLOCKED` with refusal code `aide_self_consumer_fixture.source_repo_target_confusion_refused`.

No source repo self-apply authority is accepted by this check.
