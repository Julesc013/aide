# AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

Create and process `AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

Repo truth outranks this prompt. This is a check-only task.

Independently review commit `1206980e8897ba6031d2d142743d9cac53be1817` and
`AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

Verify:

- the real Dominium CLI process was entered exactly once;
- the accepted fixture callable was not used as the executor;
- the result originated from Dominium stdout JSON;
- the typed refusal is genuine and does not claim successful aggregate
  validation;
- the service-adapter boundary is established from Dominium evidence, not only
  from an AIDE boolean;
- unsupported or invalid AIDE requests remain pre-process refusals according to
  tests and build evidence;
- Dominium revision, clean status, tracked tree digest, and command
  implementation digests are unchanged;
- committed reports contain no local absolute paths or secret-like values;
- EvidencePacket and EventRecord references resolve;
- all false-boundary fields remain false;
- no arbitrary shell, private tool, broad dispatch, provider/model/network,
  worker, Workbench, Service, preview/apply/rollback, PatchTransaction apply,
  repository mutation, branch/worktree, GitHub, release, or promotion behavior
  occurred.

Pay special attention to the proposed capability label:

```text
live_dominium_validation_command_readonly_v0
```

If that label overclaims successful live validation instead of the actually
proven command-boundary typed-result/refusal capability, recommend a bounded
relabel repair before acceptance. The precise acceptance label should be:

```text
dominium_registered_validation_command_boundary_readonly_v0
```

Do not repair implementation in this check task.

If all material checks pass, recommend exactly:

```text
AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```

If a material relabel or evidence issue remains, recommend exactly:

```text
AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
```
