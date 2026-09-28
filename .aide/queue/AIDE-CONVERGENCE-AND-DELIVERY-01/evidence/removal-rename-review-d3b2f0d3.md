# Independent removal rename-gap source review

Reviewer: `/root/stable_effect_review`
Decision: **REQUEST_CHANGES** for source integration
Reviewed commit: `d3b2f0d36e929714af80852c381c43017cbbd9ed`

The reviewer found that `load_portable_removal_intent` permits a legacy managed-`AGENTS.md` operation without `preimage_file_identity`, while the new `portable_removal_restore_agents_preimage` directly indexed that key. A legacy rename-gap retry could raise an uncaught `KeyError` instead of returning `RECOVERY_REQUIRED`. The reviewer requested the already proposed `isinstance(item.get(...), str)` guard, a focused missing-identity case, and a superseding exact candidate.

The reviewer found the remaining source path coherent at this scope: pinned parent, digest and single-link backup identity verification, non-replacing handle rename, postrename identity check, and refusal tests for changed backup, same-byte substitution and rival target. This is not an ACCEPT. The frozen 1.0.0 assets do not include this task candidate; any pre-publication integration needs a new release artifact/effect delta.
