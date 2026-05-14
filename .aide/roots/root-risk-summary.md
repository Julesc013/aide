# Root Risk Summary

- no_apply: true
- deletion_approval: false

## Risks

- `.agents`: risk=high status=review_required reasons=authority_sensitive_hint, generated_sensitive_content, unknown_kind_or_owner
- `.aide`: risk=high status=mixed reasons=identity_sensitive_hint, build_sensitive_file_hint, authority_sensitive_hint, generated_sensitive_content
- `.aide.local.example`: risk=high status=review_required reasons=unknown_kind_or_owner
- `.codex`: risk=high status=review_required reasons=unknown_kind_or_owner
- `bridges`: risk=low status=canonical reasons=unknown_kind_or_owner
- `core`: risk=high status=mixed reasons=identity_sensitive_hint, build_sensitive_file_hint, authority_sensitive_hint, generated_sensitive_content
- `docs`: risk=medium status=canonical reasons=generated_sensitive_content, unknown_kind_or_owner
- `environments`: risk=high status=review_required reasons=unknown_kind_or_owner
- `evals`: risk=high status=review_required reasons=unknown_kind_or_owner
- `fixtures`: risk=low status=canonical reasons=unknown_kind_or_owner
- `governance`: risk=high status=review_required reasons=authority_sensitive_hint, unknown_kind_or_owner
- `hosts`: risk=high status=review_required reasons=build_sensitive_file_hint, unknown_kind_or_owner
- `inventory`: risk=low status=canonical reasons=unknown_kind_or_owner
- `labs`: risk=high status=review_required reasons=unknown_kind_or_owner
- `matrices`: risk=low status=canonical reasons=unknown_kind_or_owner
- `packaging`: risk=high status=review_required reasons=identity_sensitive_hint, unknown_kind_or_owner
- `platforms`: risk=high status=review_required reasons=unknown_kind_or_owner
- `repo-root`: risk=high status=review_required reasons=authority_sensitive_hint, unknown_kind_or_owner
- `research`: risk=high status=review_required reasons=unknown_kind_or_owner
- `scripts`: risk=low status=canonical reasons=unknown_kind_or_owner
- `shared`: risk=high status=mixed reasons=build_sensitive_file_hint, unknown_kind_or_owner, multiple_file_kinds
- `specs`: risk=low status=canonical reasons=unknown_kind_or_owner
