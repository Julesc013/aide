# Dev review packet

Governing prompt: [prompt.md](../prompt.md); bounded contract: [task.yaml](../task.yaml).
Review [changed-files.md](changed-files.md), [validation.md](validation.md) and
[remaining-risks.md](remaining-risks.md). Exact source is commit498eb2c0;
recovery/pack preparation is45f29220, with actual input identities in retained receipts.
The original failed attempt, reviewed fixture repair and passing source/pack attempt
must all remain visible. No current claims rely on historical parent passes alone.

Approve only the frozen promotion-source map and integration-effect. Preview allocation3
must pass and retire before terminal closure review; actual dev/main effects require
fresh exact refs, source, controls and post-dev validation. Existing Git defaults apply:
local short-lived task branch, nonforce dev/main sync, no protection change or unrelated
remote cleanup. Retire only this local task after both remotes contain the accepted head.

Review rubric: [AIDE evidence review](../../../prompts/evidence-review.md).
Decision/gate policy: [review gates](../../../policies/review-gates.yaml).
These explicit links satisfy the preview reviewer's terminal-packet request.
