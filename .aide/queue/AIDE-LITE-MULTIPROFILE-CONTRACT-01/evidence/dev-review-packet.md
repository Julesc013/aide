### Dev and main review packet

This child requires exact independent source/effect acceptance under [.aide/policies/review-gates.yaml](../../../policies/review-gates.yaml), [.aide/policies/promotion-rules.yaml](../../../policies/promotion-rules.yaml) and [the review decision policy](../../../verification/review-decision-policy.yaml). See [evidence review](../../../../docs/reference/evidence-review-workflow.md) and [promotion validation](../../../../docs/reference/promotion-validation-gates.md).

The current source checkpoint and fixture/export allocation are separate from final acceptance and integration. [Changed files](changed-files.md), [validation](validation.md) and [remaining risks](remaining-risks.md) record the required promotion subjects. Final review must bind actual results, exact commit/tree, unchanged portable inputs after refresh, fresh local/remote refs and shared ownership state. No dev/main effect is authorized by the source allocation alone.
