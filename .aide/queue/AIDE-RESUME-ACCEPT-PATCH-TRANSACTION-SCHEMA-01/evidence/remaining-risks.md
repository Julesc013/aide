# Remaining Risks

PatchTransaction is still not an apply-capable mutation system.

Remaining risks:

- future apply work must enforce the accepted path-scope semantics;
- case-folding behavior is not yet specified;
- artifact resolution and VCS reachability are absent;
- approval, policy, rollback, admission, trust, runtime, and adapter execution
  remain unimplemented.
