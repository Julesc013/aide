# Remaining Risks

- The slice is deterministic and local only.
- It does not implement external identity, credential storage, secret access,
  OIDC/IAM, remote policy engines, distributed authorization, worker execution,
  transaction approval, or provider/model/network behavior.
- It does not accept `local_trust_enforcement_v0`; independent check and
  acceptance remain required.
