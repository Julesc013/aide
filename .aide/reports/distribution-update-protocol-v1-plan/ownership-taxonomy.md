# Ownership Taxonomy

V1 ownership classes:

| Class | Meaning | Automatic apply behavior |
| --- | --- | --- |
| `vendor_managed_file` | AIDE-owned portable file with known preimage and ledger entry. | May be created/replaced only under exact plan and preimage rules. |
| `vendor_managed_section` | AIDE-owned managed section inside a project file. | May be updated only with exact managed-section identity and preimage. |
| `project_owned` | Project authority owns content. | Never overwritten or deleted automatically. |
| `project_overlay` | Project-specific AIDE overlay or policy. | Preserve unless exact project approval exists. |
| `project_generated` | Target-local generated output. | Regenerate locally; do not copy from source as truth. |
| `runtime_generated` | Runtime/cache/output state. | Preserve or ignore; never ship as portable truth. |
| `local_only` | Local state such as `.aide.local` or secrets-adjacent storage. | Never package or mutate automatically. |
| `evidence_only` | Evidence/report material. | Preserve unless explicitly target-regenerated. |
| `preserved_legacy` | Legacy target content retained for review. | Preserve by default. |
| `unknown` | Ownership cannot be proven. | Blocks automatic apply. |
| `never_touch` | Explicitly protected paths or sections. | Always refused for apply. |

Existing Q43 ownership records map into this taxonomy through explicit migration
rules. Unknown or ambiguous classes do not become vendor-managed by inference.
