# Command Selection

Requested command:

```text
scripts/validate_public_alpha_readonly.py --json
```

Live local Eureka checkout at the pinned revision does not contain that script.

Selected existing Eureka-owned command:

```text
scripts/public_alpha_smoke.py --json
```

Reason: it is an existing deterministic JSON command in the local Eureka
checkout that exercises Public Alpha safe-mode behavior and blocked unsafe
surfaces without mutating the checkout.
